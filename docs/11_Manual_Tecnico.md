# 📘 Manual Técnico / Instalación - Sistema de Rifa

## 1. Introducción
Este manual describe los pasos técnicos necesarios para instalar, configurar y desplegar el sistema de rifa.  
Está dirigido a administradores y desarrolladores con conocimientos básicos de Python y bases de datos.

---

## 2. Requisitos previos
- **Sistema operativo:** Windows, Linux o macOS  
- **Lenguaje:** Python 3.10 o superior  
- **Base de datos:** MySQL (local o en la nube)  
- **Dependencias:** definidas en `requirements.txt`  
- **Conexión a Internet:** necesaria para despliegue en Streamlit Cloud o Railway  

---

## 3. Instalación

### 3.1 Clonar el repositorio
git clone https://github.com/usuario/rifa_solidaria.git
cd rifa_solidaria
### 3.2 Instalar dependencias
pip install -r requirements.txt

### 3.3 Configuración de la base de datos
Editar credenciales en la función `conectar()` dentro de `app.py`.  
Tablas necesarias:  
- **boletos** → número, estado, comprador, teléfono, fecha_compra  
- **transacciones** → id_transaccion, cantidad_reservada, fecha, estado  

### 4. Ejecución local  

streamlit run app.py

Acceder desde el navegador en http://localhost:8501

---

## 5. Despliegue en la nube  

### 5.1 Railway  
- Crear proyecto en Railway  
- Configurar base de datos MySQL  
- Guardar credenciales en variables de entorno  

### 5.2 Streamlit Cloud  
- Subir repositorio a GitHub  
- Conectar con Streamlit Cloud  
- Configurar archivo `requirements.txt`  
- Ejecutar aplicación en línea  

---

## 6. Mantenimiento  
- Actualizar dependencias periódicamente  
- Respaldar base de datos antes de cada despliegue  
- Revisar logs de Streamlit y Railway para detectar errores  

---

## 7. Notas finales  
- Este manual está orientado a la **instalación y configuración técnica**  
- Para instrucciones de uso, consultar el **Manual de Usuario**
