-- ======================================
-- CREACIÓN Y SELECCIÓN DE BASE DE DATOS
-- (NO USAR SI USAS CLEVER CLOUD)
-- ======================================
DROP DATABASE IF EXISTS BancoDB;
CREATE DATABASE BancoDB;
USE BancoDB;

-- ======================================
-- ELIMINAR TABLAS (ORDEN CORRECTO)
-- ======================================
-- Se eliminan primero las tablas con FOREIGN KEY hacia otras.
DROP TABLE IF EXISTS movimiento;
DROP TABLE IF EXISTS titular;
DROP TABLE IF EXISTS prestamo;
DROP TABLE IF EXISTS cuenta;
DROP TABLE IF EXISTS sucursal;
DROP TABLE IF EXISTS cuentahabiente;

-- Tablas maestras
DROP TABLE IF EXISTS tipocuenta;
DROP TABLE IF EXISTS tipodocumento;
DROP TABLE IF EXISTS tipomovimiento;
DROP TABLE IF EXISTS tiposucursal;
DROP TABLE IF EXISTS ciudad;

-- ======================================
-- TABLAS MAESTRAS
-- ======================================
CREATE TABLE tipocuenta (
    IdTipoCuenta INT AUTO_INCREMENT PRIMARY KEY,
    TipoCuenta VARCHAR(50),
    Sobregiro DECIMAL(10,2)
);

CREATE TABLE tipodocumento (
    IdTipoDocumento INT AUTO_INCREMENT PRIMARY KEY,
    TipoDocumento VARCHAR(50),
    Sigla VARCHAR(10)
);

CREATE TABLE tipomovimiento (
    IdTipoMovimiento INT AUTO_INCREMENT PRIMARY KEY,
    TipoMovimiento VARCHAR(50)
);

CREATE TABLE tiposucursal (
    IdTipoSucursal INT AUTO_INCREMENT PRIMARY KEY,
    TipoSucursal VARCHAR(50)
);

CREATE TABLE ciudad (
    IdCiudad INT AUTO_INCREMENT PRIMARY KEY,
    Ciudad VARCHAR(50)
);

-- ======================================
-- TABLAS PRINCIPALES
-- ======================================
CREATE TABLE cuentahabiente (
    IdCuentahabiente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    IdTipoDocumento INT,
    Documento VARCHAR(50),
    Direccion VARCHAR(100),
    Telefono VARCHAR(20),
    IdCiudad INT,
    Clave VARCHAR(20),
    FOREIGN KEY (IdTipoDocumento) REFERENCES tipodocumento(IdTipoDocumento),
    FOREIGN KEY (IdCiudad) REFERENCES ciudad(IdCiudad)
);

CREATE TABLE sucursal (
    IdSucursal INT AUTO_INCREMENT PRIMARY KEY,
    Sucursal VARCHAR(50),
    IdCiudad INT,
    IdTipoSucursal INT,
    Direccion VARCHAR(100),
    Telefono VARCHAR(20),
    Horario VARCHAR(50),
    FOREIGN KEY (IdCiudad) REFERENCES ciudad(IdCiudad),
    FOREIGN KEY (IdTipoSucursal) REFERENCES tiposucursal(IdTipoSucursal)
);

CREATE TABLE cuenta (
    IdCuenta INT AUTO_INCREMENT PRIMARY KEY,
    Numero VARCHAR(20),
    FechaApertura DATE,
    IdTipoCuenta INT,
    IdSucursal INT,
    Saldo DECIMAL(15,2),
    Sobregiro DECIMAL(15,2),
    GranMovimiento BOOLEAN,
    SobregiroNoAutorizado BOOLEAN,
    FOREIGN KEY (IdTipoCuenta) REFERENCES tipocuenta(IdTipoCuenta),
    FOREIGN KEY (IdSucursal) REFERENCES sucursal(IdSucursal)
);

CREATE TABLE titular (
    IdCuenta INT,
    IdCuentahabiente INT,
    PRIMARY KEY (IdCuenta, IdCuentahabiente),
    FOREIGN KEY (IdCuenta) REFERENCES cuenta(IdCuenta),
    FOREIGN KEY (IdCuentahabiente) REFERENCES cuentahabiente(IdCuentahabiente)
);

CREATE TABLE movimiento (
    IdMovimiento INT AUTO_INCREMENT PRIMARY KEY,
    IdCuenta INT,
    IdSucursal INT,
    Fecha DATE,
    Valor DECIMAL(15,2),
    IdTipoMovimiento INT,
    Descripcion VARCHAR(200),
    FOREIGN KEY (IdCuenta) REFERENCES cuenta(IdCuenta),
    FOREIGN KEY (IdSucursal) REFERENCES sucursal(IdSucursal),
    FOREIGN KEY (IdTipoMovimiento) REFERENCES tipomovimiento(IdTipoMovimiento)
);

CREATE TABLE Prestamo (
    IdPrestamo INT AUTO_INCREMENT PRIMARY KEY,
    IdCuenta INT,
    Numero VARCHAR(20),
    Fecha DATE,
    Valor DECIMAL(15,2),
    Interes DECIMAL(5,2),
    Plazo INT,
    Seguro DECIMAL(10,2),
    Cuota DECIMAL(15,2),
    FOREIGN KEY (IdCuenta) REFERENCES cuenta(IdCuenta)
);