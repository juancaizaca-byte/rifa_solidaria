# 📘 Diccionario de Datos - Sistema de Rifa Solidaria

## 1. Introducción
Este documento describe las tablas, campos, tipos de datos y claves del sistema de rifa.  
El objetivo es detallar la estructura actual de la base de datos para garantizar comprensión y mantenimiento.

---

## 2. Tablas y campos

### Tabla: boletos
| Campo          | Tipo de dato   | Clave | Descripción |
|----------------|----------------|-------|-------------|
| numero         | VARCHAR(4)     | PK    | Identificador único del boleto. |
| comprador      | VARCHAR(100)   |       | Nombre del comprador del boleto. |
| telefono       | VARCHAR(20)    |       | Teléfono de contacto del comprador. |
| estado         | ENUM('Disponible','Vendido','Reservado') |       | Estado actual del boleto. |
| fecha_compra   | DATETIME       |       | Fecha en que se realizó la compra. |
| id_transaccion | VARCHAR(50)    | FK    | Relación con la transacción correspondiente. |

---

### Tabla: transacciones
| Campo             | Tipo de dato   | Clave | Descripción |
|-------------------|----------------|-------|-------------|
| id                | INT AUTO_INCREMENT | PK | Identificador interno de la transacción. |
| id_transaccion    | VARCHAR(50)    | UNIQUE | Código único de la transacción. |
| cantidad_reservada| INT            |       | Número de boletos reservados en la transacción. |
| fecha             | DATETIME       |       | Fecha en que se realizó la transacción. |
| estado            | VARCHAR(20)    |       | Estado de la transacción (Activa, Cancelada, Finalizada). |

---

## 3. Relaciones
- **boletos.id_transaccion → transacciones.id_transaccion**  
  Relación de uno a muchos: una transacción puede tener varios boletos, pero cada boleto pertenece a una sola transacción.

---

## 4. Observaciones
- El modelo refleja la versión actual en producción.  
- La clave primaria de `boletos` es el número del boleto.  
- La integridad referencial se asegura mediante la FK `id_transaccion`.  

---

## 5. Mejoras futuras
- Normalizar nombres de columnas para consistencia.  
- Implementar `ON DELETE CASCADE` en relaciones.  
- Agregar campos de trazabilidad (usuario responsable, método de pago).  
