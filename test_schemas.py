from app.schemas import CuentaCreate
from datetime import date
from decimal import Decimal

# Probar validación
cuenta = CuentaCreate(
    Numero="1234567890",
    FechaApertura=date.today(),
    IdTipoCuenta=1,
    IdSucursal=1
)

print(cuenta.model_dump())