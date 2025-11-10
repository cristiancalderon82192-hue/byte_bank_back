from pydantic import BaseModel, Field
from typing import Optional


# Schema Base - Campos comunes
class CiudadBase(BaseModel):
    Ciudad: str = Field(..., min_length=1, max_length=50, description="Nombre de la ciudad")


# Schema para crear ciudad (POST)
class CiudadCreate(CiudadBase):
    pass


# Schema para actualizar ciudad (PUT/PATCH)
class CiudadUpdate(BaseModel):
    Ciudad: Optional[str] = Field(None, min_length=1, max_length=50, description="Nombre de la ciudad")


# Schema para respuesta (GET)
class CiudadResponse(CiudadBase):
    IdCiudad: int = Field(..., description="ID único de la ciudad")
    
    class Config:
        from_attributes = True  # Permite convertir desde modelos SQLAlchemy
        json_schema_extra = {
            "example": {
                "IdCiudad": 1,
                "Ciudad": "Bogotá"
            }
        }