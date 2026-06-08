# 📘 Historias de Usuario - Sistema de Rifa

## 1. Introducción
Este documento presenta las historias de usuario del sistema de rifa.  
Las historias se redactan en formato ágil:  
**Como [rol], quiero [acción], para [beneficio].**

---

## 2. Historias de Usuario

### HU01 - Comprar boleto
- **Como** comprador,  
- **quiero** adquirir un boleto disponible,  
- **para** participar en la rifa de manera válida.  

**Criterios de aceptación:**  
- El sistema debe registrar la compra en la base de datos.  
- El boleto debe cambiar su estado a “Vendido”.  
- El comprador debe recibir confirmación de la compra.  

---

### HU02 - Reservar boleto
- **Como** comprador,  
- **quiero** reservar un boleto,  
- **para** asegurar mi participación futura en la rifa.  

**Criterios de aceptación:**  
- El sistema debe marcar el boleto como “Reservado”.  
- El sistema debe registrar la transacción de reserva.  
- El comprador debe recibir confirmación de la reserva.  

---

### HU03 - Validar boleto
- **Como** administrador,  
- **quiero** validar un boleto mediante su número,  
- **para** confirmar que es válido para participar en la rifa.  

**Criterios de aceptación:**  
- El sistema debe verificar que el boleto existe.  
- El sistema debe comprobar el estado del boleto.  
- El sistema debe mostrar si el boleto es válido o no.  

---

### HU04 - Generar reportes
- **Como** administrador,  
- **quiero** generar reportes de boletos vendidos, reservados y disponibles,  
- **para** tener control y trazabilidad del sistema.  

**Criterios de aceptación:**  
- El sistema debe listar boletos por estado.  
- El sistema debe mostrar cantidad total por categoría.  
- El sistema debe exportar el reporte en formato legible (ej. PDF o Excel).  

---

## 3. Observaciones
- Las historias de usuario están alineadas con los **Casos de Uso** y los **Requerimientos Funcionales**.  
- Cada historia incluye criterios de aceptación que permiten validar si la funcionalidad está correctamente implementada.  
- Este documento sirve como base para pruebas de calidad y planificación de desarrollo ágil.  
