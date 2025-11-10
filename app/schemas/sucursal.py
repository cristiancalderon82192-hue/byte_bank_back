from pydantic import BaseModel, Field
from typing import Optional


class SucursalBase(BaseModel):
    Sucursal: str = Field(..., min_length=1, max_length=50, description="Nombre de la sucursal")
    IdCiudad: int = Field(..., gt=0, description="ID de la ciudad")
    IdTipoSucursal: int = Field(..., gt=0, description="ID del tipo de sucursal")
    Direccion: Optional[str] = Field(None, max_length=100, description="Dirección de la sucursal")
    Telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    Horario: Optional[str] = Field(None, max_length=50, description="Horario de atención")


class SucursalCreate(SucursalBase):
    pass


class SucursalUpdate(BaseModel):
    Sucursal: Optional[str] = Field(None, min_length=1, max_length=50)
    IdCiudad: Optional[int] = Field(None, gt=0)
    IdTipoSucursal: Optional[int] = Field(None, gt=0)
    Direccion: Optional[str] = Field(None, max_length=100)
    Telefono: Optional[str] = Field(None, max_length=20)
    Horario: Optional[str] = Field(None, max_length=50)


class SucursalResponse(SucursalBase):
    IdSucursal: int = Field(..., description="ID único de la sucursal")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdSucursal": 1,
                "Sucursal": "ByteBank Centro Bogotá",
                "IdCiudad": 1,
                "IdTipoSucursal": 1,
                "Direccion": "Calle 26 # 13-19",
                "Telefono": "601-3456789",
                "Horario": "Lunes a Viernes 8:00-17:00"
            }
        }