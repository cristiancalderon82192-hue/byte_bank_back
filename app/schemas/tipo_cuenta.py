from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class TipoCuentaBase(BaseModel):
    TipoCuenta: str = Field(..., min_length=1, max_length=50, description="Nombre del tipo de cuenta")
    Sobregiro: Optional[Decimal] = Field(None, ge=0, description="Monto de sobregiro permitido")


class TipoCuentaCreate(TipoCuentaBase):
    pass


class TipoCuentaUpdate(BaseModel):
    TipoCuenta: Optional[str] = Field(None, min_length=1, max_length=50)
    Sobregiro: Optional[Decimal] = Field(None, ge=0)


class TipoCuentaResponse(TipoCuentaBase):
    IdTipoCuenta: int = Field(..., description="ID único del tipo de cuenta")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdTipoCuenta": 1,
                "TipoCuenta": "Cuenta de Ahorros",
                "Sobregiro": "0.00"
            }
        }