"""
Operaciones CRUD (Create, Read, Update, Delete) para cada entidad.
"""

from app.crud import ciudad
from app.crud import tipo_cuenta
from app.crud import cuentahabiente
from app.crud import sucursal
from app.crud import cuenta
from app.crud import titular
from app.crud import movimiento
from app.crud import prestamo

__all__ = [
    "ciudad",
    "tipo_cuenta",
    "cuentahabiente",
    "sucursal",
    "cuenta",
    "titular",
    "movimiento",
    "prestamo",
]