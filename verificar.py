import streamlit as st
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TU PASSWORD AQUÍ",
        database="rifa_db"
    )

st.title("🔎 Verificación rápida de boletos")

conexion = conectar()
cursor = conexion.cursor()

# Resumen general
cursor.execute("SELECT estado, COUNT(*) FROM boletos GROUP BY estado")
resumen = cursor.fetchall()
st.subheader("📊 Resumen general")
for estado, cantidad in resumen:
    st.write(f"{estado}: {cantidad}")

# Últimos boletos vendidos
cursor.execute("SELECT numero, comprador, fecha_Compra FROM boletos WHERE estado='Vendido' ORDER BY fecha_Compra DESC LIMIT 10")
vendidos = cursor.fetchall()
st.subheader("🧾 Últimos 10 boletos vendidos")
if vendidos:
    for num, comp, fecha in vendidos:
        st.write(f"Boleto {num} → {comp} ({fecha})")
else:
    st.write("No hay boletos vendidos todavía.")

# Primeros boletos disponibles
cursor.execute("SELECT numero FROM boletos WHERE estado='Disponible' ORDER BY numero ASC LIMIT 10")
disponibles = cursor.fetchall()
st.subheader("🎟️ Primeros 10 boletos disponibles")
st.write([num for (num,) in disponibles])

cursor.close()
conexion.close()


