import mysql.connector
import os
from dotenv import load_dotenv

# 📌 Cargar variables del archivo .env
load_dotenv()

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),   # 👈 usar el puerto correcto
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

try:
    # 🔗 Conexión
    conexion = conectar()
    cursor = conexion.cursor()

    # 🧹 Vaciar la tabla antes de repoblar
    cursor.execute("TRUNCATE TABLE boletos")

    # 🚀 Insertar boletos del 0001 al 1000
    for i in range(1, 1001):
        numero = str(i).zfill(4)
        cursor.execute(
            """
            INSERT INTO boletos (numero, comprador, telefono, estado, fecha_compra, id_transaccion)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (numero, "", "", "Disponible", None, None)
        )

    # 💾 Guardar cambios
    conexion.commit()
    print("✅ Tabla reiniciada y repoblada con 1000 boletos disponibles")

    # 📊 Verificación
    cursor.execute("SELECT COUNT(*) FROM boletos")
    print(f"📊 Total de boletos: {cursor.fetchone()[0]}")

    cursor.execute("SELECT numero, estado FROM boletos LIMIT 10")
    print("🔎 Ejemplo de boletos cargados:", cursor.fetchall())

    # 🔒 Cerrar cursor y conexión
    cursor.close()
    conexion.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
