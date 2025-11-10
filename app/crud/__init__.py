"""
Operaciones CRUD (Create, Read, Update, Delete) para cada entidad.
"""

from app.crud import ciudad
from app.crud import cuentahabiente
from app.crud import cuenta

__all__ = [
    "ciudad",
    "cuentahabiente",
    "cuenta",
]