import streamlit as st
import mysql.connector
from datetime import datetime
from fpdf import FPDF
import io

# Función para conectar con la base de datos MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TU PASSWORD AQUÍ",
        database="rifa_db"
    )

# Título principal de la app
st.title("🎟️ Sistema de Rifa Solidaria")

# Inicializar variables en session_state (persisten entre interacciones)
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []
if "mostrar_confirmacion" not in st.session_state:
    st.session_state.mostrar_confirmacion = False
if "comprador" not in st.session_state:
    st.session_state.comprador = ""

# Traer boletos disponibles desde la base
conexion = conectar()
cursor = conexion.cursor()
cursor.execute("SELECT numero FROM boletos WHERE estado = 'Disponible' ORDER BY numero ASC")
boletos_disponibles = [row[0] for row in cursor.fetchall()]
cursor.close()
conexion.close()

# Paginación: mostrar de 50 en 50
pagina = st.number_input("Página", min_value=1, max_value=(len(boletos_disponibles)//50)+1, value=1)
inicio = (pagina-1)*50
fin = inicio+50
boletos_pagina = boletos_disponibles[inicio:fin]

# Mostrar boletos en grilla de 10 columnas
cols = st.columns(10)

# CSS para hacer los checkboxes más pequeños y chips verdes
st.markdown("""
    <style>
    div[data-testid="stCheckbox"] label {
        font-size: 8px !important;
        line-height: 1 !important;
        text-align: center;
        white-space: nowrap;
    }
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

# Renderizar los checkboxes de boletos
for i, numero in enumerate(boletos_pagina):
    numero_sin_ceros = numero
    col = cols[i % 10]
    checked = col.checkbox(numero_sin_ceros,
                           key=f"{pagina}-{numero}",
                           value=(numero in st.session_state.seleccionados))
    if checked and numero not in st.session_state.seleccionados:
        st.session_state.seleccionados.append(numero)
    elif not checked and numero in st.session_state.seleccionados:
        st.session_state.seleccionados.remove(numero)

# Mostrar boletos seleccionados como chips
st.markdown("### 🎯 Boletos seleccionados:")
if st.session_state.seleccionados:
    chips_html = "".join([f"<span class='chip'>{n}</span>" for n in st.session_state.seleccionados])
    st.markdown(f"{len(st.session_state.seleccionados)} boletos seleccionados:<br>{chips_html}", unsafe_allow_html=True)
else:
    st.write("Ninguno todavía")

# Campo para nombre del comprador
input_comprador = st.text_input("Nombre del comprador", value=st.session_state.comprador)
if input_comprador:
    st.session_state.comprador = input_comprador.capitalize()

# Botón para registrar venta
if st.button("Registrar venta"):
    if not st.session_state.seleccionados:
        st.warning("⚠️ Debes seleccionar al menos un boleto.")
    elif not st.session_state.comprador.strip():
        st.warning("⚠️ Debes ingresar el nombre del comprador.")
    else:
        st.session_state.mostrar_confirmacion = True

# Mostrar confirmación
if st.session_state.mostrar_confirmacion:
    st.markdown("### ⚠️ Confirmación de venta")
    st.write(f"Total: {len(st.session_state.seleccionados)} boletos")
    chips_html = "".join([f"<span class='chip'>{n}</span>" for n in st.session_state.seleccionados])
    st.markdown(f"Boletos a vender:<br>{chips_html}", unsafe_allow_html=True)

    if st.button("✅ Confirmar venta"):
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

            # Generar PDF
            pdf = FPDF()
            pdf.add_page()

            # Logo superior
            try:
                pdf.image("logo.png", x=10, y=8, w=30)
            except:
                pass

            # Título centrado
            pdf.set_font("Helvetica", 'B', 18)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(200, 10, "Rifa Solidaria - Comprobante de Venta", ln=True, align="C")

            pdf.ln(20)

            # Datos del comprador
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(40, 8, "Comprador:", ln=0)
            pdf.set_font("Helvetica", '', 12)
            pdf.cell(100, 8, st.session_state.comprador, ln=1)

            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(40, 8, "Fecha:", ln=0)
            pdf.set_font("Helvetica", '', 12)
            pdf.cell(100, 8, fecha_actual, ln=1)

            pdf.ln(10)

            # --- Tabla de boletos centrada y ajustada ---
            pdf.set_font("Helvetica", 'B', 11)
            pdf.set_fill_color(200, 230, 255)

            # Definir ancho de tabla (más pequeño)
            ancho_tabla = 50
            x_centro = (210 - ancho_tabla) / 2  # 210 = ancho de página A4

            pdf.set_x(x_centro)
            pdf.cell(ancho_tabla, 6, "Boletos", 1, 1, 'C', fill=True)

            pdf.set_font("Helvetica", '', 10)
            pdf.set_text_color(0, 102, 204)
            for numero_boleto in st.session_state.seleccionados:
                pdf.set_x(x_centro)
                pdf.cell(ancho_tabla, 7, numero_boleto, 1, 1, 'C')

            pdf.set_text_color(0, 0, 0)
            pdf.ln(10)


            # --- Tabla de premios centrada y más corta ---
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_fill_color(200, 200, 200)

            ancho_premios = 160
            x_centro = (210 - ancho_premios) / 2

            pdf.set_x(x_centro)
            pdf.cell(ancho_premios, 7, "Premios en juego", 1, 1, 'C', fill=True)

            pdf.set_font("Helvetica", '', 11)
            premios = [
                "Smart TV 56 pulgadas",
                "Juego de sala",
                "Lavado de auto",
                "Dos clases demostrativas de guitarra o piano"
            ]
            for premio in premios:
                pdf.set_x(x_centro)
                pdf.cell(ancho_premios, 8, premio, 1, 1, 'C')


            # --- Pie de página con logo y texto ---
            pdf.set_font("Helvetica", 'I', 10)              # Fuente cursiva para el texto
            pdf.set_text_color(0, 0, 0)                     # Color negro (puedes cambiarlo abajo)

            # Logo centrado dentro del pie de página
            try:
                pdf.image("logo1.png", x=80, y=pdf.get_y(), w=50)  # Centrado (x=80) y tamaño moderado
            except:
                pass

            pdf.ln(40)                                      # Salto de línea debajo del logo

            # Texto profesional del pie de página
            pdf.cell(200, 6, "Fecha del Sorteo el 15/06/2026", ln=True, align="C")
            pdf.cell(200, 6, "El sorteo se realizará mediante la aplicación Microsoft Teams", ln=True, align="C")


            # Exportar PDF a memoria
            pdf_output = io.BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)

            # Botón de descarga
            st.download_button(
                label="⬇️ Descargar comprobante PDF",
                data=pdf_output,
                file_name=f"venta_{fecha_actual.replace(':','-')}.pdf",
                mime="application/pdf"
            )

            # Limpiar estados
            st.session_state.seleccionados = []
            st.session_state.comprador = ""
            st.session_state.mostrar_confirmacion = False

        cursor.close()
        conexion.close()


