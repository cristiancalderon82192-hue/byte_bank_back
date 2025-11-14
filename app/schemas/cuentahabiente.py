from pydantic import BaseModel, Field, validator
from typing import Optional


class CuentahabienteBase(BaseModel):
    Nombre: str = Field(..., min_length=1, max_length=100, description="Nombre completo del cuentahabiente")
    IdTipoDocumento: int = Field(..., gt=0, description="ID del tipo de documento")
    Documento: str = Field(..., min_length=1, max_length=50, description="Número de documento")
    Direccion: Optional[str] = Field(None, max_length=100, description="Dirección de residencia")
    Telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono")
    IdCiudad: int = Field(..., gt=0, description="ID de la ciudad")
    Clave: str = Field(..., min_length=4, max_length=20, description="Clave de acceso")


class CuentahabienteCreate(CuentahabienteBase):
    @validator('Documento')
    def validate_documento(cls, v):
        if not v.isalnum():
            raise ValueError('El documento solo puede contener letras y números')
        return v
    
    @validator('Telefono')
    def validate_telefono(cls, v):
        if v and not v.replace('+', '').replace(' ', '').isdigit():
            raise ValueError('El teléfono solo puede contener números')
        return v


class CuentahabienteUpdate(BaseModel):
    Nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    IdTipoDocumento: Optional[int] = Field(None, gt=0)
    Documento: Optional[str] = Field(None, min_length=1, max_length=50)
    Direccion: Optional[str] = Field(None, max_length=100)
    Telefono: Optional[str] = Field(None, max_length=20)
    IdCiudad: Optional[int] = Field(None, gt=0)
    Clave: Optional[str] = Field(None, min_length=4, max_length=20)


class CuentahabienteResponse(BaseModel):
    IdCuentahabiente: int
    Nombre: str
    IdTipoDocumento: int
    Documento: str
    Direccion: Optional[str]
    Telefono: Optional[str]
    IdCiudad: int
    # NO devolver la clave en las respuestas por seguridad
    
    # Campos anidados con información relacionada
    NombreCiudad: Optional[str] = None
    TipoDocumentoNombre: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdCuentahabiente": 1,
                "Nombre": "Juan Pérez García",
                "IdTipoDocumento": 1,
                "Documento": "1234567890",
                "Direccion": "Calle 45 # 23-12",
                "Telefono": "3001234567",
                "IdCiudad": 1,
                "NombreCiudad": "Bogotá",
                "TipoDocumentoNombre": "Cédula de Ciudadanía"
            }
        }