# --- IMPORTS Y FUNCIONES ---
import streamlit as st
import mysql.connector
from datetime import datetime
import random
import string
from fpdf import FPDF
import io
import qrcode
from fpdf.enums import XPos, YPos

# --- Inicializar variables en session_state ---
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

if "comprador" not in st.session_state:
    st.session_state.comprador = ""

if "telefono" not in st.session_state:
    st.session_state.telefono = ""


# Función conectar
def conectar():
    return mysql.connector.connect(
        host="zephyr.proxy.rlwy.net",
        port=54106,
        user="root",
        password="tpsbWYBThxeMPrIyfIZdoQCZkLfnxwgZ",
        database="railway",
        autocommit=True,
        connection_timeout=60
    )

# Función generar PDF
def generar_pdf_compra(lista_boletos, comprador, telefono, fecha_compra):
    # ... (tu función completa de PDF tal como la tienes ahora)
    pass

# Función generar ID transacción
def generar_id_transaccion():
    fecha = datetime.datetime.now().strftime("%Y%m%d")
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TXN_{fecha}_{random_code}"

def generar_pdf_compra(lista_boletos, comprador, telefono, fecha_compra):
    pdf = FPDF()
    pdf.add_page()

    # Logo superior
    try:
        pdf.image("logo3.png", x=10, y=8, w=30)
    except:
        pass

    # Generar QR y ponerlo arriba a la derecha
    url_qr = "https://rifasolidaria-rdqf8fs99yzxm7kwkbqp3k.streamlit.app/?info=rifa"
    qr_img = qrcode.make(url_qr)
    qr_path = "qr_compra.png"
    qr_img.save(qr_path)
    pdf.image(qr_path, x=160, y=20, w=25, h=25)

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
    pdf.cell(40, 8, text="Teléfono:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(100, 8, text=telefono,
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
    st.session_state.telefono = ""
    st.session_state.mostrar_confirmacion = False


# --- PARÁMETROS DE URL ---
params = st.query_params

# Normalizar transaccion_id
transaccion_id = params.get("transaccion")
if isinstance(transaccion_id, list):
    transaccion_id = transaccion_id[0]
if transaccion_id:
    transaccion_id = transaccion_id.strip()

# Normalizar boleto_id
boleto_id = params.get("boleto")
if isinstance(boleto_id, list):
    boleto_id = boleto_id[0]

# Normalizar info_param
info_param = params.get("info")
if isinstance(info_param, list):
    info_param = info_param[0]

# --- ####### Formulario del comprador #######---
if transaccion_id:
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

# Traer datos de la transacción
    cursor.execute("SELECT cantidad_reservada FROM transacciones WHERE id_transaccion = %s", (transaccion_id,))
    transaccion = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not transaccion:
        st.error("❌ Transacción no encontrada")
    else:
        cantidad_reservada = transaccion["cantidad_reservada"]

        st.markdown("<h1 style='color:#1E3A8A; text-align:center;'>🎟️ Selección de boletos </h1>", unsafe_allow_html=True)
        st.write(f"Debes elegir exactamente {cantidad_reservada} boletos disponibles.")

        # Traer boletos disponibles
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT numero FROM boletos WHERE estado = 'Disponible' ORDER BY numero ASC")
        boletos_disponibles = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conexion.close()

        # Número total de páginas
        total_paginas = max(1, (len(boletos_disponibles) // 50) + 1)

        # Control con botones - y +
        pagina = st.number_input(
            "Página",
            min_value=1,
            max_value=total_paginas,
            value=1,
            step=1
        )
        
        # Calcular inicio y fin
        inicio = (pagina - 1) * 50
        fin = inicio + 50
        boletos_pagina = boletos_disponibles[inicio:fin]


        # Mostrar boletos en grilla (5 columnas para mejor adaptación en móvil)
        cols = st.columns(5)
        for i, numero in enumerate(boletos_pagina):
            col = cols[i % 5]

            # 👇 Convertir '0001' → '1' al mostrar
            boleto_sin_ceros = str(int(numero))

            checked = col.checkbox(
                boleto_sin_ceros,
                key=f"{pagina}-{numero}",
                value=(numero in st.session_state.seleccionados))

            if checked:
                if numero not in st.session_state.seleccionados:
                    if len(st.session_state.seleccionados) < cantidad_reservada:
                        st.session_state.seleccionados.append(numero)
                    else:
                        # 👇 revertimos el checkbox si ya alcanzó el límite
                        st.warning(f"Ya seleccionaste {cantidad_reservada} boletos, no puedes elegir más.")
            else:
                if numero in st.session_state.seleccionados:
                    st.session_state.seleccionados.remove(numero)

        # Mostrar seleccionados con chips verdes
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
            st.markdown(f"{len(st.session_state.seleccionados)} / {cantidad_reservada} boletos seleccionados:<br>{chips_html}", unsafe_allow_html=True)
        else:
            st.write("Ninguno todavía")

        # Campos comprador y teléfono
        input_comprador = st.text_input("Nombre del comprador", value=st.session_state.comprador)
        if input_comprador:
            st.session_state.comprador = input_comprador.title()

        input_telefono = st.text_input("Número de teléfono", value=st.session_state.telefono)
        if input_telefono:
            st.session_state.telefono = input_telefono

        # Botón confirmar
        if st.button("✅ Confirmar compra"):
            if len(st.session_state.seleccionados) < cantidad_reservada:
                st.warning(f"⚠️ Debes seleccionar {cantidad_reservada} boletos. Te falta {cantidad_reservada - len(st.session_state.seleccionados)}.")
            elif len(st.session_state.seleccionados) > cantidad_reservada:
                st.warning(f"⚠️ Debes seleccionar exactamente {cantidad_reservada} boletos.")
            elif not st.session_state.comprador.strip():
                st.warning("⚠️ Debes ingresar el nombre del comprador.")
            elif not st.session_state.telefono.strip():
                st.warning("⚠️ Debes ingresar el número de teléfono.")
            else:
                try:
                    conexion = conectar()
                    cursor = conexion.cursor()
                    fecha_actual = datetime.now().strftime("%Y-%m-%d")

                    # Actualizar boletos vendidos
                    for numero_boleto in st.session_state.seleccionados:
                        cursor.execute("""
                            UPDATE boletos
                            SET comprador = %s, telefono = %s, estado = 'Vendido', fecha_compra = %s
                            WHERE numero = %s AND estado = 'Disponible'
                        """, (st.session_state.comprador, st.session_state.telefono, fecha_actual, numero_boleto))

                    conexion.commit()
                    st.success(f"✅ Compra registrada: {len(st.session_state.seleccionados)} boletos vendidos a {st.session_state.comprador} ({st.session_state.telefono})")

                    # Generar PDF
                    generar_pdf_compra(st.session_state.seleccionados, st.session_state.comprador, st.session_state.telefono, fecha_actual)

                except Exception as e:
                    st.error(f"Error en la base de datos: {e}")
                finally:
                    cursor.close()
                    conexion.close()

# --- ####### Formulario del vendedor ####### ---
elif not boleto_id and not info_param and not transaccion_id:
    import datetime
    import random
    import string
    import mysql.connector

    def generar_id_transaccion():
        fecha = datetime.datetime.now().strftime("%Y%m%d")
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TXN_{fecha}_{random_code}"

    db_config = {
        "host": "zephyr.proxy.rlwy.net",
        "port": 54106,
        "user": "root",
        "password": "tpsbWYBThxeMPrIyfIZdoQCZkLfnxwgZ",
        "database": "railway"
    }

    # 🎨 Encabezado con estilo
    st.markdown("<h1 style='color:#1E3A8A; text-align:center;'>📋 Registro de venta </h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

    # Sección: Boletos
    cantidad_boletos = st.number_input("🎟️ Ingrese la cantidad de boletos vendidos:", min_value=1, step=1)

    if st.button("Generar URL"):
        id_transaccion = generar_id_transaccion()
        url_unico = f"https://rifasolidaria-rdqf8fs99yzxm7kwkbqp3k.streamlit.app/?transaccion={id_transaccion}"

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            sql = """
            INSERT INTO transacciones (id_transaccion, cantidad_reservada, fecha, estado)
            VALUES (%s, %s, %s, %s)
            """
            values = (id_transaccion, cantidad_boletos, datetime.datetime.now(), "Reservado")
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            # Sección: Confirmación
            st.success("✅ Transacción creada con éxito. Comparta este enlace con el comprador.")
            st.markdown(f"<p style='font-size:16px; color:purple;'>🔗 URL único:</p>", unsafe_allow_html=True)
            st.code(url_unico, language='text')

            # Sección: Compartir
            st.markdown("<p style='color:#444; font-size:18px;'>🔗 Compartir</p>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style='margin-top:10px;'>
                    <a href="https://wa.me/?text=Participa%20en%20la%20rifa:%20{url_unico}" target="_blank"
                    style='background-color:#25D366;color:white;padding:6px 12px;border-radius:5px;text-decoration:none;margin-right:8px;'>💬 WhatsApp</a>
                    <a href="mailto:?subject=Rifa%20Solidaria&body=Tu%20enlace:%20{url_unico}" target="_blank"
                    style='background-color:#0072C6;color:white;padding:6px 12px;border-radius:5px;text-decoration:none;'>📧 Correo</a>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Error al guardar en la base: {e}")

# --- VALIDACIÓN + INFORMACIÓN DE LA RIFA ---
params = st.query_params
boleto_id = params.get("boleto", [None])[0]

# 👇 Ajuste: normalizar el parámetro "info"
info_param = params.get("info")
if isinstance(info_param, list):   # si viene como lista, tomar el primer valor
    info_param = info_param[0]

if info_param == "rifa":
    # 👇 Bloque con fondo celeste muy claro y Markdown para listas
    st.markdown(
        """
        <div style='background-color:#E6F7FF; padding:15px; border-radius:10px;'>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🎉 Información oficial de la Rifa")
    st.write("📅 **Fecha del sorteo:** 15 de julio de 2026")
    st.write("📍 **Lugar:** Transmisión en vivo por Teams")

    st.markdown("### 🏆 Premios en juego")
    st.markdown("""
    - 🍽️ Set de vajilla para 4 personas  
    - ☕ Cafetera eléctrica  
    - 🛏️ Juego de sábanas  
    - 🎁 Dos premios sorpresa  
    - 🎸 Clase demostrativa de guitarra  
    """)

    st.markdown("### 📜 Reglas básicas")
    st.markdown("""
    - Cada boleto es único y válido solo con su comprobante PDF.  
    - El sorteo será público y transparente.  
    - Los premios no son canjeables por dinero.  
    - El comprador debe conservar su boleto (PDF) hasta el día del sorteo.  
    """)

    st.markdown("### 📞 Contacto")
    st.write("WhatsApp: +593 962 308 005")

elif boleto_id:
    # 👇 Validación interna de boletos (sin mostrar datos sensibles)
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM boletos WHERE numero = %s", (boleto_id,))
    resultado = cursor.fetchone()

    if resultado:
        st.success("✅ Boleto válido para la rifa")
    else:
        st.error("❌ Boleto no encontrado")

    cursor.close()
    conexion.close()
else:
    st.info("Escanee el QR de su boleto para más información de la rifa.")
