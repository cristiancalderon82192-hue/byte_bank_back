from pydantic import BaseModel, Field
from typing import Optional


class TipoSucursalBase(BaseModel):
    TipoSucursal: str = Field(..., min_length=1, max_length=50, description="Nombre del tipo de sucursal")


class TipoSucursalCreate(TipoSucursalBase):
    pass


class TipoSucursalUpdate(BaseModel):
    TipoSucursal: Optional[str] = Field(None, min_length=1, max_length=50)


class TipoSucursalResponse(TipoSucursalBase):
    IdTipoSucursal: int = Field(..., description="ID único del tipo de sucursal")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdTipoSucursal": 1,
                "TipoSucursal": "Sucursal Principal"
            }
        }