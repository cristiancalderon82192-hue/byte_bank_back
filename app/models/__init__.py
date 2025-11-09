"""
Modelos SQLAlchemy para el sistema bancario ByteBank.
Importar todos los modelos en orden de dependencias.
"""

# Tablas maestras (sin dependencias)
from app.models.ciudad import Ciudad
from app.models.tipo_cuenta import TipoCuenta
from app.models.tipo_documento import TipoDocumento
from app.models.tipo_movimiento import TipoMovimiento
from app.models.tipo_sucursal import TipoSucursal

# Tablas principales (con dependencias)
from app.models.cuentahabiente import Cuentahabiente
from app.models.sucursal import Sucursal
from app.models.cuenta import Cuenta
from app.models.titular import Titular
from app.models.movimiento import Movimiento
from app.models.prestamo import Prestamo

__all__ = [
    # Tablas maestras
    "Ciudad",
    "TipoCuenta",
    "TipoDocumento",
    "TipoMovimiento",
    "TipoSucursal",
    # Tablas principales
    "Cuentahabiente",
    "Sucursal",
    "Cuenta",
    "Titular",
    "Movimiento",
    "Prestamo",
]