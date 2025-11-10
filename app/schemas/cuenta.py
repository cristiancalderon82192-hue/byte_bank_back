from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from datetime import date


class CuentaBase(BaseModel):
    Numero: str = Field(..., min_length=1, max_length=20, description="Número de cuenta único")
    FechaApertura: date = Field(..., description="Fecha de apertura de la cuenta")
    IdTipoCuenta: int = Field(..., gt=0, description="ID del tipo de cuenta")
    IdSucursal: int = Field(..., gt=0, description="ID de la sucursal")
    Saldo: Decimal = Field(default=Decimal("0.00"), ge=0, description="Saldo actual de la cuenta")
    Sobregiro: Optional[Decimal] = Field(default=Decimal("0.00"), ge=0, description="Límite de sobregiro")
    GranMovimiento: Optional[bool] = Field(default=False, description="Indica si tiene gran movimiento")
    SobregiroNoAutorizado: Optional[bool] = Field(default=False, description="Indica sobregiro no autorizado")


class CuentaCreate(BaseModel):
    Numero: str = Field(..., min_length=1, max_length=20)
    FechaApertura: date
    IdTipoCuenta: int = Field(..., gt=0)
    IdSucursal: int = Field(..., gt=0)
    Saldo: Optional[Decimal] = Field(default=Decimal("0.00"), ge=0)
    Sobregiro: Optional[Decimal] = Field(default=Decimal("0.00"), ge=0)
    
    @validator('Numero')
    def validate_numero(cls, v):
        if not v.isdigit():
            raise ValueError('El número de cuenta solo puede contener dígitos')
        return v


class CuentaUpdate(BaseModel):
    Numero: Optional[str] = Field(None, min_length=1, max_length=20)
    IdTipoCuenta: Optional[int] = Field(None, gt=0)
    IdSucursal: Optional[int] = Field(None, gt=0)
    Saldo: Optional[Decimal] = Field(None, ge=0)
    Sobregiro: Optional[Decimal] = Field(None, ge=0)
    GranMovimiento: Optional[bool] = None
    SobregiroNoAutorizado: Optional[bool] = None


class CuentaResponse(CuentaBase):
    IdCuenta: int = Field(..., description="ID único de la cuenta")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdCuenta": 1,
                "Numero": "1001234567890",
                "FechaApertura": "2024-01-15",
                "IdTipoCuenta": 1,
                "IdSucursal": 1,
                "Saldo": "1500000.00",
                "Sobregiro": "0.00",
                "GranMovimiento": False,
                "SobregiroNoAutorizado": False
            }
        }