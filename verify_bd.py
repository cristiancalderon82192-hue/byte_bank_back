"""
Script para verificar que la base de datos existente
es compatible con los modelos SQLAlchemy
"""

from app.database import SessionLocal, engine
from app.models import *
from sqlalchemy import inspect, text


def verify_database():
    """Verificar tablas existentes y su compatibilidad"""
    
    print("Verificando conexión a base de datos...")
    
    try:
        db = SessionLocal()
        
        # Verificar conexión
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        print("Conexión exitosa a la base de datos\n")
        
        # Obtener inspector
        inspector = inspect(engine)
        
        # Tablas esperadas por los modelos
        expected_tables = [
            'ciudad',
            'tipocuenta',
            'tipodocumento',
            'tipomovimiento',
            'tiposucursal',
            'cuentahabiente',
            'sucursal',
            'cuenta',
            'titular',
            'movimiento',
            'prestamo'
        ]
        
        # Tablas existentes en la BD
        existing_tables = inspector.get_table_names()
        
        print("Tablas en la base de datos:")
        print("=" * 50)
        
        missing_tables = []
        for table in expected_tables:
            if table in existing_tables:
                # Contar registros
                from sqlalchemy import text
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"{table:<20} - {count} registros")
            else:
                print(f"{table:<20} - NO EXISTE")
                missing_tables.append(table)
        
        print("\n" + "=" * 50)
        
        if missing_tables:
            print(f"\nFaltan {len(missing_tables)} tablas:")
            for table in missing_tables:
                print(f"   - {table}")
            print("\nEjecuta el script SQL para crear las tablas faltantes")
        else:
            print("\nTodas las tablas existen correctamente!")
        
        # Verificar datos de ejemplo
        print("\nVerificando datos:")
        print("=" * 50)
        
        ciudades = db.query(Ciudad).count()
        print(f"  Ciudades: {ciudades}")
        
        tipos_cuenta = db.query(TipoCuenta).count()
        print(f"  Tipos de Cuenta: {tipos_cuenta}")
        
        cuentahabientes = db.query(Cuentahabiente).count()
        print(f"  Cuentahabientes: {cuentahabientes}")
        
        cuentas = db.query(Cuenta).count()
        print(f"  Cuentas: {cuentas}")
        
        sucursales = db.query(Sucursal).count()
        print(f"  Sucursales: {sucursales}")
        
        if ciudades == 0 and tipos_cuenta == 0:
            print("\nLa base de datos está vacía.")
            print("   Ejecuta: python init_db.py para poblar con datos de prueba")
        
        db.close()
        
    except Exception as e:
        print(f"Error al conectar con la base de datos:")
        print(f"   {str(e)}\n")
        print("Verifica:")
        print("   1. MySQL está corriendo")
        print("   2. Las credenciales en .env son correctas")
        print("   3. La base de datos 'BancoDB' existe")
        return False
    
    return True


if __name__ == "__main__":
    print("ByteBank - Verificación de Base de Datos")
    print("=" * 50)
    print()
    
    if verify_database():
        print("\n" + "=" * 50)
        print("Base de datos lista para usar con FastAPI")
        print("\nInicia la API con: uvicorn app.main:app --reload")
    else:
        print("\n" + "=" * 50)
        print("Error: Corrige los errores antes de continuar")