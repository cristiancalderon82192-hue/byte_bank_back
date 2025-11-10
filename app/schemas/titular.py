from pydantic import BaseModel, Field


class TitularBase(BaseModel):
    IdCuenta: int = Field(..., gt=0, description="ID de la cuenta")
    IdCuentahabiente: int = Field(..., gt=0, description="ID del cuentahabiente")


class TitularCreate(TitularBase):
    pass


class TitularResponse(TitularBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "IdCuenta": 1,
                "IdCuentahabiente": 1
            }
        }


# Schema para listar titulares con información relacionada
class TitularDetalle(BaseModel):
    IdCuenta: int
    IdCuentahabiente: int
    NombreCuentahabiente: str
    DocumentoCuentahabiente: str
    NumeroCuenta: str
    
    class Config:
        from_attributes = True