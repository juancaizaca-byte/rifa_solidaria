## 🙌👍PARA IMPORTAR LOS BOLETOS ##

import mysql.connector   # Importa la librería para conectar Python con MySQL

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",       
    user="root",            
    password="TU PASSWORD AQUÍ", 
    database="rifa_db"      
)

cursor = conexion.cursor()

# 🚀 Inserción automática de boletos del 0001 al 1000
for i in range(1, 1001):
    numero = str(i).zfill(4)  # Convierte 1 en 0001, 25 en 0025, etc.
    cursor.execute(
        "INSERT INTO boletos (numero, comprador, estado) VALUES (%s, %s, %s)",
        (numero, "", "Disponible")  
    )

conexion.commit()   # Guarda los cambios en la base
print("✅👌 Se insertaron los boletos del 0001 al 1000")

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

cursor.close()
conexion.close()
