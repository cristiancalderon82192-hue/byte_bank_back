from pydantic import BaseModel, Field
from typing import Optional


class TipoMovimientoBase(BaseModel):
    TipoMovimiento: str = Field(..., min_length=1, max_length=50, description="Nombre del tipo de movimiento")


class TipoMovimientoCreate(TipoMovimientoBase):
    pass


class TipoMovimientoUpdate(BaseModel):
    TipoMovimiento: Optional[str] = Field(None, min_length=1, max_length=50)


class TipoMovimientoResponse(TipoMovimientoBase):
    IdTipoMovimiento: int = Field(..., description="ID único del tipo de movimiento")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdTipoMovimiento": 1,
                "TipoMovimiento": "Depósito"
            }
        }