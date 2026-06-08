# 📘 Requerimientos Funcionales - Sistema de Rifa

## 1. Introducción
Este documento detalla los requerimientos funcionales del sistema de rifa.  
Su propósito es definir las funciones que el sistema debe cumplir para satisfacer las necesidades del usuario y garantizar la correcta operación del proceso de compra, reserva y validación de boletos.

---

## 2. Alcance del sistema
El sistema permite gestionar boletos de rifa mediante operaciones de compra, reserva, validación y generación de reportes.  
Los actores principales son:
- **Comprador:** realiza la compra o reserva de boletos.  
- **Administrador:** valida boletos y genera reportes de control.

---

## 3. Requerimientos funcionales

| Código | Requerimiento | Descripción |
|---------|----------------|-------------|
| RF01 | Registro de compra de boletos | El sistema debe permitir al comprador adquirir boletos disponibles y registrar la transacción correspondiente. |
| RF02 | Reserva de boletos | El sistema debe permitir reservar boletos para compra futura, cambiando su estado a “Reservado”. |
| RF03 | Validación de boletos | El sistema debe permitir al administrador verificar la validez de un boleto mediante su número y estado. |
| RF04 | Generación de reportes | El sistema debe permitir generar reportes de boletos vendidos, reservados y disponibles. |
| RF05 | Control de estados | El sistema debe actualizar automáticamente el estado de los boletos según las operaciones realizadas. |
| RF06 | Registro de transacciones | El sistema debe almacenar cada operación (compra o reserva) en la tabla `transacciones` con fecha y cantidad. |
| RF07 | Confirmación al usuario | El sistema debe mostrar mensajes de confirmación o error según el resultado de la operación. |

---

## 4. Requerimientos no funcionales
| Código | Requerimiento | Descripción |
|---------|----------------|-------------|
| RNF01 | Usabilidad | La interfaz debe ser intuitiva y fácil de usar para compradores y administradores. |
| RNF02 | Seguridad | Los datos de las transacciones y boletos deben protegerse contra accesos no autorizados. |
| RNF03 | Disponibilidad | El sistema debe estar disponible en todo momento para realizar operaciones. |
| RNF04 | Rendimiento | Las operaciones de compra y validación deben ejecutarse en menos de 2 segundos. |
| RNF05 | Mantenibilidad | El código y la base de datos deben estar documentados para facilitar futuras mejoras. |

---

## 5. Relación con los Casos de Uso
Cada requerimiento funcional se vincula con uno o más casos de uso:
- **RF01, RF02 → CU01 y CU02 (Comprar y Reservar boleto)**  
- **RF03 → CU03 (Validar boleto)**  
- **RF04 → CU04 (Generar reportes)**  

---

## 6. Observaciones
- Este documento refleja la versión actual del sistema en producción.  
- Los requerimientos podrán ampliarse conforme se agreguen nuevas funcionalidades.  
