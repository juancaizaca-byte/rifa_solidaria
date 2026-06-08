# 📘 Plan de Pruebas - Sistema de Rifa

## 1. Introducción
Este documento describe los casos de prueba diseñados para validar el correcto funcionamiento del sistema de rifa.  
El objetivo es asegurar que cada requerimiento funcional se cumpla y que el sistema sea confiable para compradores y administradores.

---

## 2. Estrategia de pruebas
- **Tipo de pruebas:** Funcionales, de interfaz y de base de datos.  
- **Método:** Pruebas manuales iniciales, con posibilidad de automatización futura.  
- **Referencia:** Basado en los requerimientos funcionales documentados en `/docs/05_Requerimientos_Funcionales.md`.

---

## 3. Casos de Prueba

### CP01 - Comprar boleto
- **Objetivo:** Validar que un comprador pueda adquirir un boleto disponible.  
- **Precondiciones:** El boleto debe estar en estado “Disponible”.  
- **Pasos de prueba:**  
  1. Ingresar al sistema como comprador.  
  2. Seleccionar un boleto disponible.  
  3. Ingresar datos de contacto.  
  4. Confirmar compra.  
- **Resultado esperado:**  
  - El boleto cambia a estado “Vendido”.  
  - Se genera una transacción asociada.  
  - Se muestra comprobante al comprador.

---

### CP02 - Reservar boleto
- **Objetivo:** Validar que un comprador pueda reservar un boleto.  
- **Precondiciones:** El boleto debe estar en estado “Disponible”.  
- **Pasos de prueba:**  
  1. Ingresar al sistema como comprador.  
  2. Seleccionar un boleto disponible.  
  3. Solicitar reserva.  
- **Resultado esperado:**  
  - El boleto cambia a estado “Reservado”.  
  - Se genera transacción de reserva.  
  - Se muestra confirmación al comprador.

---

### CP03 - Generar reporte
- **Objetivo:** Validar que el administrador pueda generar un reporte de boletos.  
- **Precondiciones:** Deben existir boletos en distintos estados.  
- **Pasos de prueba:**  
  1. Ingresar al sistema como administrador.  
  2. Solicitar reporte de boletos.  
- **Resultado esperado:**  
  - El sistema muestra listado por estado (vendidos, reservados, disponibles).  
  - El sistema permite exportar a PDF/Excel.

---

### CP04 - Validar boleto (pendiente de implementación)
- **Objetivo:** Comprobar que el sistema pueda verificar si un boleto es válido.  
- **Precondiciones:** El boleto debe existir en la base de datos.  
- **Pasos de prueba:**  
  1. Ingresar al sistema como administrador.  
  2. Ingresar número de boleto.  
  3. Solicitar validación.  
- **Resultado esperado:**  
  - El sistema muestra estado del boleto (válido, reservado, inválido).  
- **Nota:** Este caso de prueba está planificado para futuras versiones.

---

## 4. Observaciones
- Los casos de prueba se basan en los requerimientos funcionales actuales.  
- Se recomienda ejecutar pruebas cada vez que se actualice el sistema.  
- Los casos pendientes deben marcarse como “por implementar” para mantener transparencia.
