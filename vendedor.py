import streamlit as st
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
st.markdown("<h1 style='color:#1E3A8A; text-align:center;'>📋 Registro de venta - Vendedor</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

# Sección: Boletos
cantidad_boletos = st.number_input("🎟️ Ingrese la cantidad de boletos vendidos:", min_value=1, step=1)

if st.button("Generar transacción"):
    id_transaccion = generar_id_transaccion()
    url_unico = f"https://tuapp.streamlit.app/?transaccion={id_transaccion}"

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
        st.markdown(f"<p style='font-size:18px; color:purple;'>🔗 URL único:</p>", unsafe_allow_html=True)
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
