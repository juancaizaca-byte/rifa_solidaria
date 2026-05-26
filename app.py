import streamlit as st
import mysql.connector
from datetime import datetime
from fpdf import FPDF
import io
import qrcode

# Función para conectar con la base de datos
def conectar():
    return mysql.connector.connect(
        host="zephyr.proxy.rlwy.net",
        port=54106,
        user="root",
        password="tpsbWYBThxeMPrIyfIZdoQCZkLfnxwgZ",
        database="railway"
    )

# Función para generar PDF con QR y botón de descarga
def generar_pdf_compra(lista_boletos, comprador, fecha_compra):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado
    pdf.cell(200, 10, txt="Comprobante de compra", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Comprador: {comprador}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha: {fecha_compra}", ln=True)

    pdf.ln(10)

    # Listado de boletos comprados
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Boletos comprados:", ln=True)
    for b in lista_boletos:
        pdf.cell(200, 8, txt=f"- Boleto #{b}", ln=True)

    # Generar QR con la URL que apunta a la página unificada
    url_qr = f"https://tuapp.streamlit.app/?boleto={lista_boletos[0]}"
    qr_img = qrcode.make(url_qr)
    qr_path = "qr_compra.png"
    qr_img.save(qr_path)

    # Insertar QR en el PDF
    pdf.image(qr_path, x=150, y=50, w=40, h=40)

    # Exportar PDF a memoria (más limpio que guardarlo en disco)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    # Botón de descarga
    st.download_button(
        label="⬇️ Descargar comprobante PDF",
        data=pdf_output,
        file_name=f"compra_{comprador}.pdf",
        mime="application/pdf"
    )

    # Limpiar estados
    st.session_state.seleccionados = []
    st.session_state.comprador = ""
    st.session_state.mostrar_confirmacion = False

# --- Interfaz principal ---
st.title("🎟️ Sistema de Rifa 🎟️")

# Inicializar variables
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []
if "mostrar_confirmacion" not in st.session_state:
    st.session_state.mostrar_confirmacion = False
if "comprador" not in st.session_state:
    st.session_state.comprador = ""

# Traer boletos disponibles
conexion = conectar()
cursor = conexion.cursor()
cursor.execute("SELECT numero FROM boletos WHERE estado = 'Disponible' ORDER BY numero ASC")
boletos_disponibles = [row[0] for row in cursor.fetchall()]
cursor.close()
conexion.close()

# Paginación
pagina = st.number_input("Página", min_value=1, max_value=(len(boletos_disponibles)//50)+1, value=1)
inicio = (pagina-1)*50
fin = inicio+50
boletos_pagina = boletos_disponibles[inicio:fin]

# Mostrar boletos en grilla
cols = st.columns(10)
for i, numero in enumerate(boletos_pagina):
    numero_sin_ceros = str(numero)
    col = cols[i % 10]
    checked = col.checkbox(numero_sin_ceros,
                           key=f"{pagina}-{numero}",
                           value=(numero in st.session_state.seleccionados))
    if checked and numero not in st.session_state.seleccionados:
        st.session_state.seleccionados.append(numero)
    elif not checked and numero in st.session_state.seleccionados:
        st.session_state.seleccionados.remove(numero)

# Mostrar seleccionados
st.markdown("""
    <style>
    .chip {
        display: inline-block;
        padding: 4px 10px;
        margin: 2px;
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.seleccionados:
    chips_html = "".join([f"<span class='chip'>{n}</span>" for n in st.session_state.seleccionados])
    st.markdown(f"{len(st.session_state.seleccionados)} boletos seleccionados:<br>{chips_html}", unsafe_allow_html=True)
else:
    st.write("Ninguno todavía")

# Campo comprador
input_comprador = st.text_input("Nombre del comprador", value=st.session_state.comprador)
if input_comprador:
    st.session_state.comprador = input_comprador.capitalize()

# Botón registrar venta
if st.button("Registrar venta"):
    if not st.session_state.seleccionados:
        st.warning("⚠️ Debes seleccionar al menos un boleto.")
    elif not st.session_state.comprador.strip():
        st.warning("⚠️ Debes ingresar el nombre del comprador.")
    else:
        st.session_state.mostrar_confirmacion = True

# Confirmación
if st.session_state.mostrar_confirmacion:
    st.markdown("### ⚠️ Confirmación de venta")
    st.write(f"Total: {len(st.session_state.seleccionados)} boletos")
    chips_html = "".join([f"<span class='chip'>{n}</span>" for n in st.session_state.seleccionados])
    st.markdown(f"Boletos a vender:<br>{chips_html}", unsafe_allow_html=True)

if st.button("✅ Confirmar venta"):
    conexion = conectar()
    cursor = conexion.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Validar duplicados
        duplicados = []
        for numero_boleto in st.session_state.seleccionados:
            cursor.execute("SELECT estado FROM boletos WHERE numero = %s", (numero_boleto,))
            estado = cursor.fetchone()
            if not estado or estado[0] != "Disponible":
                duplicados.append(numero_boleto)

        if duplicados:
            st.error(f"⚠️ Los siguientes boletos ya no están disponibles: {', '.join([str(n) for n in duplicados])}")
        else:
            for numero_boleto in st.session_state.seleccionados:
                cursor.execute("""
                    UPDATE boletos
                    SET comprador = %s, estado = 'Vendido', fecha_Compra = %s
                    WHERE numero = %s AND estado = 'Disponible'
                """, (st.session_state.comprador, fecha_actual, numero_boleto))

            conexion.commit()
            st.success(f"✅ Venta registrada: {len(st.session_state.seleccionados)} boletos vendidos a {st.session_state.comprador} el {fecha_actual}")

            generar_pdf_compra(st.session_state.seleccionados, st.session_state.comprador, fecha_actual)

    except Exception as e:
        st.error(f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        conexion.close()

    # Validar duplicados
    duplicados = []
    for numero_boleto in st.session_state.seleccionados:
        cursor.execute("SELECT estado FROM boletos WHERE numero = %s", (numero_boleto,))
        estado = cursor.fetchone()
        if not estado or estado[0] != "Disponible":
            duplicados.append(numero_boleto)

    if duplicados:
        st.error(f"⚠️ Los siguientes boletos ya no están disponibles: {', '.join([str(n) for n in duplicados])}")
    else:
        # Actualizar boletos vendidos
        for numero_boleto in st.session_state.seleccionados:
            cursor.execute("""
                UPDATE boletos
                SET comprador = %s, estado = 'Vendido', fecha_Compra = %s
                WHERE numero = %s AND estado = 'Disponible'
            """, (st.session_state.comprador, fecha_actual, numero_boleto))

        conexion.commit()
        st.success(f"✅ Venta registrada: {len(st.session_state.seleccionados)} boletos vendidos a {st.session_state.comprador} el {fecha_actual}")

        # Generar PDF y mostrar botón
        generar_pdf_compra(st.session_state.seleccionados, st.session_state.comprador, fecha_actual)

    cursor.close()
    conexion.close()

# --- VALIDACIÓN + INFORMACIÓN DE LA RIFA ---
params = st.query_params
boleto_id = params.get("boleto", [None])[0]

if boleto_id:
    # 👇 abrir nueva conexión aquí
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM boletos WHERE id = %s", (boleto_id,))
    resultado = cursor.fetchone()

    if resultado:
        st.header("🎟️ Validación de Boleto")
        st.success("✅ Boleto encontrado")
        st.write(f"**Número de boleto:** {resultado['id']}")
        st.write(f"**Comprador:** {resultado['comprador']}")
        st.write(f"**Fecha de compra:** {resultado['fecha_compra']}")
        st.write(f"**Estado:** {resultado['estado']}")

        st.markdown("---")

        st.header("🎉 Información de la Rifa – Apoyando nuestra causa")
        st.write("📅 **Fecha del sorteo:** 30 de junio de 2026")
        st.write("📍 **Lugar:** Transmisión en vivo por Teams")

        st.subheader("🏆 Premios en juego:")
        st.write("- 🍽️ Set de vajilla para 4 personas")
        st.write("- ☕ Cafetera eléctrica")
        st.write("- 🛏️ Juego de sábanas")
        st.write("- 🎁 Dos premios sorpresa")
        st.write("- 🎸 Clase demostrativa de guitarra")

        st.subheader("📜 Reglas básicas:")
        st.write("- Cada boleto es único y válido solo con su comprobante PDF.")
        st.write("- El sorteo será público y transparente.")
        st.write("- Los premios no son canjeables por dinero.")
        st.write("- El comprador debe conservar su boleto hasta el día del sorteo.")

        st.subheader("📞 Contacto:")
        st.write("WhatsApp del encargado: +593 962 308 005")
        st.write("Correo: rifasolidaria@example.com")

    else:
        st.error("❌ Boleto no encontrado")

    # 👇 cerrar conexión aquí
    cursor.close()
    conexion.close()
else:
    st.info("Escanee el QR de su boleto para ver validación e información de la rifa.")
