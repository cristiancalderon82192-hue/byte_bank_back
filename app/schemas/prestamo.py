from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from datetime import date


class PrestamoBase(BaseModel):
    IdCuenta: int = Field(..., gt=0, description="ID de la cuenta asociada")
    Numero: str = Field(..., min_length=1, max_length=20, description="Número de préstamo único")
    Fecha: date = Field(..., description="Fecha de otorgamiento del préstamo")
    Valor: Decimal = Field(..., gt=0, description="Monto del préstamo")
    Interes: Decimal = Field(..., ge=0, le=100, description="Tasa de interés anual (%)")
    Plazo: int = Field(..., gt=0, description="Plazo en meses")
    Seguro: Optional[Decimal] = Field(default=Decimal("0.00"), ge=0, description="Valor del seguro")
    Cuota: Decimal = Field(..., gt=0, description="Valor de la cuota mensual")


class PrestamoCreate(BaseModel):
    IdCuenta: int = Field(..., gt=0)
    Numero: str = Field(..., min_length=1, max_length=20)
    Fecha: date
    Valor: Decimal = Field(..., gt=0)
    Interes: Decimal = Field(..., ge=0, le=100)
    Plazo: int = Field(..., gt=0, le=360, description="Plazo máximo 360 meses (30 años)")
    Seguro: Optional[Decimal] = Field(default=Decimal("0.00"), ge=0)
    Cuota: Optional[Decimal] = None  # Se puede calcular automáticamente
    
    @validator('Numero')
    def validate_numero(cls, v):
        if not v.isalnum():
            raise ValueError('El número de préstamo solo puede contener letras y números')
        return v


class PrestamoUpdate(BaseModel):
    Interes: Optional[Decimal] = Field(None, ge=0, le=100)
    Plazo: Optional[int] = Field(None, gt=0, le=360)
    Seguro: Optional[Decimal] = Field(None, ge=0)
    Cuota: Optional[Decimal] = Field(None, gt=0)


class PrestamoResponse(PrestamoBase):
    IdPrestamo: int = Field(..., description="ID único del préstamo")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdPrestamo": 1,
                "IdCuenta": 1,
                "Numero": "PRE-20240001",
                "Fecha": "2024-01-15",
                "Valor": "10000000.00",
                "Interes": "12.50",
                "Plazo": 36,
                "Seguro": "50000.00",
                "Cuota": "335847.00"
            }
        }


# Schema para calcular cuota
class CalculoCuota(BaseModel):
    Valor: Decimal = Field(..., gt=0, description="Monto del préstamo")
    Interes: Decimal = Field(..., ge=0, le=100, description="Tasa de interés anual (%)")
    Plazo: int = Field(..., gt=0, description="Plazo en meses")
    Seguro: Optional[Decimal] = Field(default=Decimal("0.00"), ge=0)


class CalculoCuotaResponse(BaseModel):
    CuotaMensual: Decimal = Field(..., description="Cuota mensual calculada")
    TotalAPagar: Decimal = Field(..., description="Total a pagar durante el plazo")
    TotalIntereses: Decimal = Field(..., description="Total de intereses a pagar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "CuotaMensual": "335847.00",
                "TotalAPagar": "12090492.00",
                "TotalIntereses": "2090492.00"
            }
        }