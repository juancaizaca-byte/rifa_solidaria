CREATE DATABASE rifa_db;

CREATE TABLE boletos(
    numero			VARCHAR(4) NOT NULL PRIMARY KEY,
    comprador		VARCHAR(100),
    telefono		VARCHAR(20),
    estado			VARCHAR(20) DEFAULT 'Disponible',
    fecha_compra	DATETIME,
    id_transaccion	VARCHAR(50)
);

CREATE TABLE transacciones (
    id					INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_transaccion		VARCHAR(50) NOT NULL,
    cantidad_reservada	INT NOT NULL,
    fecha				DATETIME NOT NULL,
    estado 				VARCHAR(20) NOT NULL
);

-- Crear realcion --
ALTER TABLE boletos
ADD CONSTRAINT fk_transaccion
FOREIGN KEY (id_transaccion) REFERENCES transacciones(id_transaccion);

-- Valores para pruebas --
INSERT INTO boletos (numero, estado)
VALUES ('001', 'Disponible'),
       ('002', 'Disponible'),
       ('003', 'Disponible'),
       ('004', 'Disponible'),
       ('005', 'Disponible'),
       ('006', 'Disponible'),
       ('007', 'Disponible'),
       ('008', 'Disponible'),
       ('009', 'Disponible'),
       ('010', 'Disponible');
	
