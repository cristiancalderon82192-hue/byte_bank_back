-- USE BancoDB;
-- ======================================
-- DATOS DE CATÁLOGOS
-- ======================================
INSERT INTO tipocuenta (TipoCuenta, Sobregiro) VALUES
('Ahorros', 500),
('Corriente', 2000),
('Nómina', 1000),
('Empresarial', 5000),
('Crédito', 0);

INSERT INTO tipodocumento (TipoDocumento, Sigla) VALUES
('Cédula', 'CC'),
('Pasaporte', 'PA'),
('Tarjeta Identidad', 'TI'),
('NIT', 'NI'),
('Cédula Extranjería', 'CE');

INSERT INTO tipomovimiento (TipoMovimiento) VALUES
('Depósito'),
('Retiro'),
('Transferencia'),
('Pago préstamo'),
('Interés'),
('Comisión');

INSERT INTO tiposucursal (TipoSucursal) VALUES
('Principal'),
('Secundaria'),
('Express'),
('Oficina Central');

INSERT INTO ciudad (Ciudad) VALUES
('Bogotá'),
('Medellín'),
('Cali'),
('Barranquilla'),
('Cartagena'),
('Bucaramanga'),
('Cúcuta'),
('Pereira'),
('Manizales'),
('Villavicencio');

INSERT INTO sucursal (Sucursal, IdCiudad, IdTipoSucursal, Direccion, Telefono, Horario) VALUES
('Sucursal Norte', 1, 1, 'Cra 10 #20-30', '6011234567', '8am-5pm'),
('Sucursal Sur', 2, 2, 'Calle 50 #30-20', '6049876543', '8am-5pm'),
('Sucursal Centro', 3, 1, 'Av 6 #10-45', '6021237890', '8am-4pm'),
('Sucursal Express 1', 4, 3, 'Carrera 45 #33-12', '6051231234', '7am-7pm'),
('Sucursal VIP', 5, 4, 'Calle 5 #44-10', '6055555555', '9am-6pm');

-- ======================================
-- GENERACIÓN DE DATOS COHERENTES
-- ======================================

DELIMITER //

-- === CLIENTES ===
CREATE PROCEDURE poblar_clientes()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 50 DO
        INSERT INTO cuentahabiente (Nombre, IdTipoDocumento, Documento, Direccion, Telefono, IdCiudad, Clave)
        VALUES (
            CONCAT('Cliente ', i),
            FLOOR(1 + RAND() * 5),
            CONCAT('10', LPAD(i, 6, '0')),
            CONCAT('Calle ', i, ' #', i+10, '-', i+5),
            CONCAT('300', LPAD(i, 7, '0')),
            FLOOR(1 + RAND() * 10),
            CONCAT('clave', i)
        );
        SET i = i + 1;
    END WHILE;
END//

-- === CUENTAS + TITULARES ===
DELIMITER //

CREATE PROCEDURE poblar_cuentas_y_titulares()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE cuenta_id INT;
    DECLARE j INT;

    WHILE i <= 50 DO
        SET j = 1 + FLOOR(RAND() * 3);
        WHILE j > 0 DO
            INSERT INTO cuenta (Numero, FechaApertura, IdTipoCuenta, IdSucursal, Saldo, Sobregiro, GranMovimiento, SobregiroNoAutorizado)
            VALUES (
                CONCAT('CU', LPAD(i, 6, '0')),
                DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 1000) DAY),
                FLOOR(1 + RAND() * 5),
                FLOOR(1 + RAND() * 5),
                ROUND(RAND() * 10000000, 2),
                ROUND(RAND() * 1000, 2),
                RAND() > 0.8,
                RAND() > 0.9
            );
            SET cuenta_id = LAST_INSERT_ID();
            INSERT INTO titular (IdCuenta, IdCuentahabiente) VALUES (cuenta_id, i);
            SET j = j - 1;
        END WHILE;
        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;


-- === MOVIMIENTOS ===
DELIMITER //

CREATE PROCEDURE poblar_movimientos()
BEGIN
    DECLARE cuenta INT;
    DECLARE i INT DEFAULT 1;
    DECLARE max_cuenta INT;

    -- obtener el máximo ID de cuentas existentes una sola vez
    SELECT MAX(IdCuenta) INTO max_cuenta FROM cuenta;

    WHILE i <= 100 DO
        -- elegir una cuenta aleatoria existente
        SET cuenta = FLOOR(1 + RAND() * max_cuenta);

        INSERT INTO movimiento (IdCuenta, IdSucursal, Fecha, Valor, IdTipoMovimiento, Descripcion)
        VALUES (
            cuenta,
            FLOOR(1 + RAND() * 5),
            DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 365) DAY),
            ROUND(RAND() * 500000, 2),
            FLOOR(1 + RAND() * 6),
            CONCAT('Movimiento generado ', i)
        );

        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;


DELIMITER //

-- === PRÉSTAMOS ===
CREATE PROCEDURE poblar_prestamos()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE max_cuenta INT;

    -- obtener el máximo ID de cuenta una sola vez
    SELECT MAX(IdCuenta) INTO max_cuenta FROM Cuenta;

    WHILE i <= 50 DO
        INSERT INTO prestamo (IdCuenta, Numero, Fecha, Valor, Interes, Plazo, Seguro, Cuota)
        VALUES (
            FLOOR(1 + RAND() * max_cuenta),
            CONCAT('PR', LPAD(i, 6, '0')),
            DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 1500) DAY),
            ROUND(RAND() * 8000000, 2),
            ROUND(5 + RAND() * 15, 2),
            FLOOR(6 + RAND() * 48),
            ROUND(RAND() * 30000, 2),
            ROUND(RAND() * 400000, 2)
        );
        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;


-- === EJECUCIÓN DE POBLACIÓN ===
CALL poblar_clientes();
CALL poblar_cuentas_y_titulares();
CALL poblar_movimientos();
CALL poblar_prestamos();

-- === LIMPIEZA ===
DROP PROCEDURE poblar_clientes;
DROP PROCEDURE poblar_cuentas_y_titulares;
DROP PROCEDURE poblar_movimientos;
DROP PROCEDURE poblar_prestamos;

-- ======================================
-- VALIDACIÓN
-- ======================================
SELECT 'Datos generados correctamente' AS Mensaje;