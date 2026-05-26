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
        database="railway",
        autocommit=True,          # 👈 fuerza commit automático
        connection_timeout=60     # 👈 evita que se corte rápido
    )

# Función para generar PDF con QR y botón de descarga
from fpdf.enums import XPos, YPos

def generar_pdf_compra(lista_boletos, comprador, fecha_compra):
    pdf = FPDF()
    pdf.add_page()

    # Logo superior
    try:
        pdf.image("logo.png", x=10, y=8, w=30)
    except:
        pass

    # Generar QR y ponerlo arriba a la derecha
    url_qr = f"https://rifasolidaria-rdqf8fs99yzxm7kwkbqp3k.streamlit.app/?boleto={lista_boletos[0]}"
    qr_img = qrcode.make(url_qr)
    qr_path = "qr_compra.png"
    qr_img.save(qr_path)
    pdf.image(qr_path, x=150, y=20, w=40, h=40)

    # Título centrado
    pdf.set_font("Helvetica", 'B', 18)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, text="Tu Aporte Vale Oro - Comprobante",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(20)

    # Datos del comprador
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, text="Comprador:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(100, 8, text=comprador,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, text="Fecha:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(100, 8, text=fecha_compra,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # --- Tabla de boletos centrada y ajustada ---
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_fill_color(200, 230, 255)
    ancho_tabla = 50
    x_centro = (210 - ancho_tabla) / 2
    pdf.set_x(x_centro)
    pdf.cell(ancho_tabla, 6, text="Boletos", border=1,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)

    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(0, 102, 204)
    for numero_boleto in lista_boletos:
        pdf.set_x(x_centro)
        pdf.cell(ancho_tabla, 7, text=str(numero_boleto), border=1,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # --- Tabla de premios ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_fill_color(200, 200, 200)
    ancho_premios = 160
    x_centro = (210 - ancho_premios) / 2
    pdf.set_x(x_centro)
    pdf.cell(ancho_premios, 7, text="Premios en juego", border=1,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)

    pdf.set_font("Helvetica", '', 11)
    premios = [
        "Set de vajilla para 4 personas",
        "Cafetera eléctrica",
        "Juego de sábanas",
        "Dos premios sorpresa",
        "Clase demostrativa de guitarra"
    ]
    for premio in premios:
        pdf.set_x(x_centro)
        pdf.cell(ancho_premios, 8, text=premio, border=1,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # --- Pie de página ---
    pdf.set_font("Helvetica", 'I', 9)
    pdf.set_text_color(0, 0, 0)
    try:
        pdf.image("logo1.png", x=80, y=pdf.get_y(), w=50)
    except:
        pass
    pdf.ln(40)
    pdf.cell(200, 6, text="Fecha del Sorteo: Sábado 27/06/2026",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(200, 6, text="El sorteo se realizará de manera virtual, el enlace será compartido vía redes sociales",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Exportar PDF a memoria
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

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

params = st.query_params
boleto_id = params.get("boleto", [None])[0]

# --- Mostrar solo la compra si NO viene del QR ---
if not boleto_id:
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
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

            except Exception as e:
                st.error(f"Error en la base de datos: {e}")
            finally:
                cursor.close()
                conexion.close()

# --- VALIDACIÓN + INFORMACIÓN DE LA RIFA ---
params = st.query_params
boleto_id = params.get("boleto", [None])[0]

if boleto_id:
    # 👇 abrir nueva conexión aquí
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM boletos WHERE numero = %s", (boleto_id,))
    resultado = cursor.fetchone()


    if resultado:
        st.header("🎟️ Validación de Boleto")
        st.success("✅ Boleto encontrado")

        st.write(f"**Número de boleto:** {resultado['numero']}")
        st.write(f"**Comprador:** {resultado['comprador']}")
        st.write(f"**Fecha de compra:** {resultado['fecha_compra']}")
        st.write(f"**Estado:** {resultado['estado']}")

    # Traer todos los boletos de la misma compra (mismo comprador y misma fecha)
        cursor.execute("""
        SELECT numero FROM boletos 
        WHERE comprador = %s AND fecha_compra = %s
        """, (resultado['comprador'], resultado['fecha_compra']))
        boletos_comprador = [row['numero'] for row in cursor.fetchall()]
    if boletos_comprador:
        boletos_str = ", ".join(str(b) for b in boletos_comprador)
        st.write(f"**Boletos comprados en esta transacción:** {boletos_str}")

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

    else:
        st.error("❌ Boleto no encontrado")

    # 👇 cerrar conexión aquí
    cursor.close()
    conexion.close()
else:
    st.info("Escanee el QR de su boleto para ver validación e información de la rifa.")
