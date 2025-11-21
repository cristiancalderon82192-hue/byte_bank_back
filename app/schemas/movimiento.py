from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from datetime import date


class MovimientoBase(BaseModel):
    IdCuenta: int = Field(..., gt=0, description="ID de la cuenta")
    IdSucursal: int = Field(..., gt=0, description="ID de la sucursal")
    Fecha: date = Field(..., description="Fecha del movimiento")
    Valor: Decimal = Field(..., description="Valor del movimiento (positivo o negativo)")
    IdTipoMovimiento: int = Field(..., gt=0, description="ID del tipo de movimiento")
    Descripcion: Optional[str] = Field(None, max_length=200, description="Descripción del movimiento")


class MovimientoCreate(MovimientoBase):
    @validator('Valor')
    def validate_valor(cls, v):
        if v == 0:
            raise ValueError('El valor del movimiento no puede ser cero')
        return v


class MovimientoUpdate(BaseModel):
    Descripcion: Optional[str] = Field(None, max_length=200)
    # Los demás campos no deberían modificarse después de crear el movimiento


class MovimientoResponse(BaseModel):
    IdMovimiento: int = Field(..., description="ID único del movimiento")
    IdCuenta: Optional[int] = Field(None, description="ID de la cuenta")
    IdSucursal: Optional[int] = Field(None, description="ID de la sucursal")
    Fecha: Optional[date] = Field(None, description="Fecha del movimiento")
    Valor: Optional[Decimal] = Field(None, description="Valor del movimiento (positivo o negativo)")
    IdTipoMovimiento: Optional[int] = Field(None, description="ID del tipo de movimiento")
    Descripcion: Optional[str] = Field(None, max_length=200, description="Descripción del movimiento")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdMovimiento": 1,
                "IdCuenta": 1,
                "IdSucursal": 1,
                "Fecha": "2024-11-09",
                "Valor": "500000.00",
                "IdTipoMovimiento": 1,
                "Descripcion": "Depósito inicial"
            }
        }


# Schemas para operaciones específicas
class DepositoCreate(BaseModel):
    IdCuenta: int = Field(..., gt=0)
    IdSucursal: int = Field(..., gt=0)
    Valor: Decimal = Field(..., gt=0, description="Monto a depositar")
    Descripcion: Optional[str] = Field(None, max_length=200)


class RetiroCreate(BaseModel):
    IdCuenta: int = Field(..., gt=0)
    IdSucursal: int = Field(..., gt=0)
    Valor: Decimal = Field(..., gt=0, description="Monto a retirar")
    Descripcion: Optional[str] = Field(None, max_length=200)


class TransferenciaCreate(BaseModel):
    IdCuentaOrigen: int = Field(..., gt=0, description="Cuenta que envía el dinero")
    IdCuentaDestino: int = Field(..., gt=0, description="Cuenta que recibe el dinero")
    IdSucursal: int = Field(..., gt=0)
    Valor: Decimal = Field(..., gt=0, description="Monto a transferir")
    Descripcion: Optional[str] = Field(None, max_length=200)
    
    @validator('IdCuentaDestino')
    def validate_cuentas_diferentes(cls, v, values):
        if 'IdCuentaOrigen' in values and v == values['IdCuentaOrigen']:
            raise ValueError('La cuenta origen y destino no pueden ser la misma')
        return v