"""
Schemas Pydantic para validación y serialización de datos.
Importar todos los schemas para fácil acceso.
"""

# Tablas maestras
from app.schemas.ciudad import (
    CiudadBase, CiudadCreate, CiudadUpdate, CiudadResponse
)
from app.schemas.tipo_cuenta import (
    TipoCuentaBase, TipoCuentaCreate, TipoCuentaUpdate, TipoCuentaResponse
)
from app.schemas.tipo_documento import (
    TipoDocumentoBase, TipoDocumentoCreate, TipoDocumentoUpdate, TipoDocumentoResponse
)
from app.schemas.tipo_movimiento import (
    TipoMovimientoBase, TipoMovimientoCreate, TipoMovimientoUpdate, TipoMovimientoResponse
)
from app.schemas.tipo_sucursal import (
    TipoSucursalBase, TipoSucursalCreate, TipoSucursalUpdate, TipoSucursalResponse
)

# Tablas principales
from app.schemas.cuentahabiente import (
    CuentahabienteBase, CuentahabienteCreate, CuentahabienteUpdate, CuentahabienteResponse
)
from app.schemas.sucursal import (
    SucursalBase, SucursalCreate, SucursalUpdate, SucursalResponse
)
from app.schemas.cuenta import (
    CuentaBase, CuentaCreate, CuentaUpdate, CuentaResponse
)
from app.schemas.titular import (
    TitularBase, TitularCreate, TitularResponse, TitularDetalle
)
from app.schemas.movimiento import (
    MovimientoBase, MovimientoCreate, MovimientoUpdate, MovimientoResponse,
    DepositoCreate, RetiroCreate, TransferenciaCreate
)
from app.schemas.prestamo import (
    PrestamoBase, PrestamoCreate, PrestamoUpdate, PrestamoResponse,
    CalculoCuota, CalculoCuotaResponse
)

__all__ = [
    # Ciudad
    "CiudadBase", "CiudadCreate", "CiudadUpdate", "CiudadResponse",
    # Tipo Cuenta
    "TipoCuentaBase", "TipoCuentaCreate", "TipoCuentaUpdate", "TipoCuentaResponse",
    # Tipo Documento
    "TipoDocumentoBase", "TipoDocumentoCreate", "TipoDocumentoUpdate", "TipoDocumentoResponse",
    # Tipo Movimiento
    "TipoMovimientoBase", "TipoMovimientoCreate", "TipoMovimientoUpdate", "TipoMovimientoResponse",
    # Tipo Sucursal
    "TipoSucursalBase", "TipoSucursalCreate", "TipoSucursalUpdate", "TipoSucursalResponse",
    # Cuentahabiente
    "CuentahabienteBase", "CuentahabienteCreate", "CuentahabienteUpdate", "CuentahabienteResponse",
    # Sucursal
    "SucursalBase", "SucursalCreate", "SucursalUpdate", "SucursalResponse",
    # Cuenta
    "CuentaBase", "CuentaCreate", "CuentaUpdate", "CuentaResponse",
    # Titular
    "TitularBase", "TitularCreate", "TitularResponse", "TitularDetalle",
    # Movimiento
    "MovimientoBase", "MovimientoCreate", "MovimientoUpdate", "MovimientoResponse",
    "DepositoCreate", "RetiroCreate", "TransferenciaCreate",
    # Préstamo
    "PrestamoBase", "PrestamoCreate", "PrestamoUpdate", "PrestamoResponse",
    "CalculoCuota", "CalculoCuotaResponse",
]