import mysql.connector   # Librería para conectar Python con MySQL

# 🔗 Conexión a Railway (usa el host y puerto público)
conexion = mysql.connector.connect(
    host="zephyr.proxy.rlwy.net",       # 👈 host público de Railway
    port=54106,                         # 👈 puerto público
    user="root",                        # 👈 usuario
    password="tpsbWYBThxeMPrIyfIZdoQCZkLfnxwgZ",  # 👈 tu clave
    database="railway"                  # 👈 nombre de la base
)

cursor = conexion.cursor()

# 🚀 Inserción automática de boletos del 0001 al 1000
for i in range(1, 1001):
    numero = str(i).zfill(4)  # Convierte 1 en '0001', 25 en '0025', etc.
    cursor.execute(
        """
        INSERT INTO boletos (numero, comprador, telefono, estado, fecha_compra, id_transaccion)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (numero, "", "", "Disponible", None, None)  
        # comprador vacío, teléfono vacío, estado inicial "Disponible",
        # fecha_compra NULL, id_transaccion NULL
    )

# 💾 Guardar cambios en la base
conexion.commit()
print("✅👌 Se insertaron los boletos del 0001 al 1000 en Railway")

# 📊 Verificación: contar boletos
cursor.execute("SELECT COUNT(*) FROM boletos")
resultado = cursor.fetchone()
print(f"📊 Total de boletos en la base: {resultado[0]}")

# 📋 Verificación: mostrar primeros 10 boletos
cursor.execute("SELECT numero, estado FROM boletos LIMIT 10")
filas = cursor.fetchall()
print("🔎 Ejemplo de boletos cargados:")
for fila in filas:
    print(fila)

# 🔒 Cerrar cursor y conexión
cursor.close()
conexion.close()
