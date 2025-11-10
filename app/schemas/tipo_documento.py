from pydantic import BaseModel, Field
from typing import Optional


class TipoDocumentoBase(BaseModel):
    TipoDocumento: str = Field(..., min_length=1, max_length=50, description="Nombre del tipo de documento")
    Sigla: Optional[str] = Field(None, max_length=10, description="Sigla del documento (ej: CC, TI)")


class TipoDocumentoCreate(TipoDocumentoBase):
    pass


class TipoDocumentoUpdate(BaseModel):
    TipoDocumento: Optional[str] = Field(None, min_length=1, max_length=50)
    Sigla: Optional[str] = Field(None, max_length=10)


class TipoDocumentoResponse(TipoDocumentoBase):
    IdTipoDocumento: int = Field(..., description="ID único del tipo de documento")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdTipoDocumento": 1,
                "TipoDocumento": "Cédula de Ciudadanía",
                "Sigla": "CC"
            }
        }