"""
Script para inicializar la base de datos con datos de prueba.
Ejecutar después de crear las tablas con Alembic.
"""

from app.database import SessionLocal, engine, Base
from app.models import *
from datetime import date
from decimal import Decimal


def init_db():
    """Inicializar base de datos con datos básicos"""
    db = SessionLocal()
    
    try:
        print("Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente")
        
        # Verificar si ya existen datos
        if db.query(Ciudad).first():
            print("La base de datos ya tiene datos. Abortando inicialización.")
            return
        
        print("\nInsertando datos iniciales...")
        
        # 1. Ciudades
        print("  - Ciudades...")
        ciudades = [
            Ciudad(Ciudad="Bogotá"),
            Ciudad(Ciudad="Medellín"),
            Ciudad(Ciudad="Cali"),
            Ciudad(Ciudad="Barranquilla"),
            Ciudad(Ciudad="Cartagena"),
        ]
        db.add_all(ciudades)
        db.commit()
        
        # 2. Tipos de Documento
        print("  - Tipos de Documento...")
        tipos_documento = [
            TipoDocumento(TipoDocumento="Cédula de Ciudadanía", Sigla="CC"),
            TipoDocumento(TipoDocumento="Tarjeta de Identidad", Sigla="TI"),
            TipoDocumento(TipoDocumento="Cédula de Extranjería", Sigla="CE"),
            TipoDocumento(TipoDocumento="Pasaporte", Sigla="PA"),
            TipoDocumento(TipoDocumento="NIT", Sigla="NIT"),
        ]
        db.add_all(tipos_documento)
        db.commit()
        
        # 3. Tipos de Cuenta
        print("  - Tipos de Cuenta...")
        tipos_cuenta = [
            TipoCuenta(TipoCuenta="Cuenta de Ahorros", Sobregiro=Decimal("0.00")),
            TipoCuenta(TipoCuenta="Cuenta Corriente", Sobregiro=Decimal("5000000.00")),
            TipoCuenta(TipoCuenta="Cuenta Nómina", Sobregiro=Decimal("0.00")),
            TipoCuenta(TipoCuenta="Cuenta Empresarial", Sobregiro=Decimal("10000000.00")),
        ]
        db.add_all(tipos_cuenta)
        db.commit()
        
        # 4. Tipos de Movimiento
        print("  - Tipos de Movimiento...")
        tipos_movimiento = [
            TipoMovimiento(TipoMovimiento="Depósito"),
            TipoMovimiento(TipoMovimiento="Retiro"),
            TipoMovimiento(TipoMovimiento="Transferencia Enviada"),
            TipoMovimiento(TipoMovimiento="Transferencia Recibida"),
            TipoMovimiento(TipoMovimiento="Pago de Servicios"),
            TipoMovimiento(TipoMovimiento="Consignación"),
        ]
        db.add_all(tipos_movimiento)
        db.commit()
        
        # 5. Tipos de Sucursal
        print("  - Tipos de Sucursal...")
        tipos_sucursal = [
            TipoSucursal(TipoSucursal="Sucursal Principal"),
            TipoSucursal(TipoSucursal="Sucursal Comercial"),
            TipoSucursal(TipoSucursal="Punto de Atención"),
            TipoSucursal(TipoSucursal="Cajero Automático"),
        ]
        db.add_all(tipos_sucursal)
        db.commit()
        
        # 6. Sucursales
        print("  - Sucursales...")
        sucursales = [
            Sucursal(
                Sucursal="ByteBank Centro Bogotá",
                IdCiudad=1,
                IdTipoSucursal=1,
                Direccion="Calle 26 # 13-19",
                Telefono="601-3456789",
                Horario="Lunes a Viernes 8:00-17:00"
            ),
            Sucursal(
                Sucursal="ByteBank Medellín",
                IdCiudad=2,
                IdTipoSucursal=2,
                Direccion="Carrera 43A # 1-50",
                Telefono="604-2345678",
                Horario="Lunes a Viernes 8:00-17:00"
            ),
            Sucursal(
                Sucursal="ByteBank Cali",
                IdCiudad=3,
                IdTipoSucursal=2,
                Direccion="Calle 5 # 38-59",
                Telefono="602-8765432",
                Horario="Lunes a Sábado 9:00-18:00"
            ),
        ]
        db.add_all(sucursales)
        db.commit()
        
        # 7. Cuentahabientes
        print("  - Cuentahabientes...")
        cuentahabientes = [
            Cuentahabiente(
                Nombre="Juan Pérez García",
                IdTipoDocumento=1,
                Documento="1234567890",
                Direccion="Calle 45 # 23-12",
                Telefono="3001234567",
                IdCiudad=1,
                Clave="clave123"
            ),
            Cuentahabiente(
                Nombre="María López Rodríguez",
                IdTipoDocumento=1,
                Documento="9876543210",
                Direccion="Carrera 7 # 32-45",
                Telefono="3109876543",
                IdCiudad=1,
                Clave="clave456"
            ),
            Cuentahabiente(
                Nombre="Carlos Martínez Silva",
                IdTipoDocumento=1,
                Documento="5555666677",
                Direccion="Avenida 68 # 45-67",
                Telefono="3205556666",
                IdCiudad=2,
                Clave="clave789"
            ),
        ]
        db.add_all(cuentahabientes)
        db.commit()
        
        # 8. Cuentas
        print("  - Cuentas...")
        cuentas = [
            Cuenta(
                Numero="1001234567890",
                FechaApertura=date(2024, 1, 15),
                IdTipoCuenta=1,
                IdSucursal=1,
                Saldo=Decimal("1500000.00"),
                Sobregiro=Decimal("0.00"),
                GranMovimiento=False,
                SobregiroNoAutorizado=False
            ),
            Cuenta(
                Numero="2009876543210",
                FechaApertura=date(2024, 3, 20),
                IdTipoCuenta=2,
                IdSucursal=1,
                Saldo=Decimal("5000000.00"),
                Sobregiro=Decimal("5000000.00"),
                GranMovimiento=False,
                SobregiroNoAutorizado=False
            ),
            Cuenta(
                Numero="1005555666677",
                FechaApertura=date(2024, 6, 10),
                IdTipoCuenta=1,
                IdSucursal=2,
                Saldo=Decimal("800000.00"),
                Sobregiro=Decimal("0.00"),
                GranMovimiento=False,
                SobregiroNoAutorizado=False
            ),
        ]
        db.add_all(cuentas)
        db.commit()
        
        # 9. Titulares
        print("  - Titulares...")
        titulares = [
            Titular(IdCuenta=1, IdCuentahabiente=1),
            Titular(IdCuenta=2, IdCuentahabiente=2),
            Titular(IdCuenta=3, IdCuentahabiente=3),
        ]
        db.add_all(titulares)
        db.commit()
        
        print("\nBase de datos inicializada exitosamente!")
        print(f"   - {len(ciudades)} ciudades")
        print(f"   - {len(tipos_documento)} tipos de documento")
        print(f"   - {len(tipos_cuenta)} tipos de cuenta")
        print(f"   - {len(tipos_movimiento)} tipos de movimiento")
        print(f"   - {len(tipos_sucursal)} tipos de sucursal")
        print(f"   - {len(sucursales)} sucursales")
        print(f"   - {len(cuentahabientes)} cuentahabientes")
        print(f"   - {len(cuentas)} cuentas")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("ByteBank - Inicialización de Base de Datos")
    print("=" * 50)
    init_db()