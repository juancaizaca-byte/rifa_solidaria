# 📘 Flujo de Procesos - Sistema de Rifa

## 1. Introducción
Este documento describe el flujo de procesos del sistema de rifa.  
El objetivo es representar la secuencia de actividades que realizan los actores y el sistema para cumplir los requerimientos funcionales.

---

## 2. Flujo principal: Compra de boleto
1. El comprador accede al sistema.  
2. Selecciona un boleto disponible.  
3. El sistema valida disponibilidad.  
4. El comprador ingresa sus datos (nombre, teléfono).  
5. El sistema registra la compra en la tabla `boletos`.  
6. El sistema genera una transacción en la tabla `transacciones`.  
7. El sistema confirma la compra y muestra comprobante.  

---

## 3. Flujo alternativo: Reserva de boleto
1. El comprador accede al sistema.  
2. Selecciona un boleto disponible.  
3. El sistema valida disponibilidad.  
4. El comprador solicita reserva.  
5. El sistema marca el boleto como “Reservado”.  
6. El sistema registra la transacción de reserva.  
7. El sistema confirma la reserva al comprador.  

---

## 4. Flujo de validación de boleto
1. El administrador accede al sistema.  
2. Ingresa el número de boleto.  
3. El sistema busca el boleto en la base de datos.  
4. El sistema verifica estado y transacción asociada.  
5. El sistema muestra resultado (válido / no válido).  

> 📝 **Nota:** La funcionalidad de validación de boletos aún no está implementada en el sistema actual.  
> Se encuentra planificada para una futura versión del módulo de administración, donde el encargado podrá verificar la validez de los boletos directamente desde la interfaz.

---

## 5. Flujo de generación de reportes
1. El administrador accede al sistema.  
2. Solicita reporte de boletos.  
3. El sistema consulta la base de datos.  
4. El sistema genera listado por estado (vendidos, reservados, disponibles).  
5. El sistema muestra reporte y permite exportar a PDF/Excel.  

---

## 6. Observaciones
- Los flujos reflejan la versión actual del sistema.  
- Cada flujo está vinculado a un Caso de Uso y a uno o más Requerimientos Funcionales.  
- Se recomienda complementar este documento con diagramas visuales (ej. BPMN o UML Activity Diagram).  


