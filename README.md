# 🎉 Tu Aporte Vale Oro - Rifa

Aplicación web para gestionar una rifa  con boletos digitales, comprobantes PDF y validación por QR.  
Permite a vendedores registrar ventas, compradores seleccionar boletos y generar comprobantes PDF con código QR para validación.

---
## 🚀 Características principales

- 📋 **Formulario del vendedor**: registro de ventas y generación de enlaces únicos para compradores.  
- 🎟️ **Formulario del comprador**: selección de boletos disponibles y confirmación de compra.  
- 📄 **Comprobante PDF**: se genera automáticamente con logo, datos del comprador y QR de validación.  
- 🔍 **Validación de boletos**: escaneo del QR para verificar validez en la base de datos.  
- ℹ️ **Información oficial de la rifa**: accesible desde el QR, con premios, reglas y contacto.

---
## 🛠️ Tecnologías utilizadas

- **Python** + [Streamlit](https://streamlit.io/) → interfaz web.  
- **MySQL** → base de datos para boletos y transacciones.  
- **FPDF2** + [qrcode](https://pypi.org/project/qrcode/) → generación de comprobantes PDF con QR.  
- **Railway** + **Streamlit Cloud** → despliegue y hosting.  

---
## ⚙️ Instalación y ejecución

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/usuario/rifa_solidaria.git
   cd rifa_solidaria
2. **Instalar dependencias**
    pip install -r requirements.txt
3. **Ejecutar la aplicación**
    streamlit run app.py


## 🗄️ Configuración de la base de datos

    Editar credenciales en la función conectar() dentro de app.py.
    Tablas necesarias:
        --boletos → contiene número, estado, comprador, teléfono, fecha_compra.
        --transacciones → contiene id_transaccion, cantidad_reservada, fecha, estado.

## 📸 Ejemplos de uso

- **Formulario del vendedor**: registro de venta y generación de enlace único.
- **Formulario del comprador**: selección de boletos con chips verdes y confirmación.
- **Comprobante PDF**: incluye logo, QR y tabla de premios.
- **Validación QR**: muestra información oficial de la rifa.

## 📅 Información de la rifa
Fecha del sorteo: 15 de julio de 2026
Lugar: Transmisión en vivo por Teams
Premios: vajilla, cafetera, sábanas, premios sorpresa, clase de guitarra

## 📞 Contacto
- WhatsApp: +00 000 000 000

## 📜 Licencia

Este proyecto fue desarrollado con fines solidarios y demostrativos.  
Se permite su uso libre únicamente para fines educativos, personales o comunitarios.  

**Todos los derechos reservados.**  
No está autorizado su uso comercial, distribución con fines de lucro ni modificación para venta sin el consentimiento expreso y por escrito del autor.  
Para acuerdos comerciales, soporte o personalización, por favor contactar directamente al desarrollador.
## 📞 Contacto comercial