from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.titular import TitularCreate, TitularResponse
from app.crud import titular as crud

router = APIRouter()


@router.get("/cuenta/{cuenta_id}")
def listar_titulares_de_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    """Obtener todos los titulares de una cuenta con información detallada"""
    titulares = crud.get_titulares_by_cuenta(db, cuenta_id=cuenta_id)
    return {
        "IdCuenta": cuenta_id,
        "TotalTitulares": len(titulares),
        "Titulares": [
            {
                "IdCuentahabiente": t.IdCuentahabiente,
                "Nombre": t.Nombre,
                "Documento": t.Documento
            }
            for t in titulares
        ]
    }


@router.get("/cuentahabiente/{cuentahabiente_id}")
def listar_cuentas_de_titular(cuentahabiente_id: int, db: Session = Depends(get_db)):
    """Obtener todas las cuentas donde una persona es titular"""
    cuentas = crud.get_cuentas_by_cuentahabiente(db, cuentahabiente_id=cuentahabiente_id)
    return {
        "IdCuentahabiente": cuentahabiente_id,
        "TotalCuentas": len(cuentas),
        "Cuentas": [
            {
                "IdCuenta": c.IdCuenta,
                "Numero": c.Numero,
                "Saldo": c.Saldo
            }
            for c in cuentas
        ]
    }


@router.post("/", response_model=TitularResponse, status_code=status.HTTP_201_CREATED)
def asociar_titular(titular: TitularCreate, db: Session = Depends(get_db)):
    """
    Asociar un cuentahabiente como titular de una cuenta.
    
    Una cuenta puede tener múltiples titulares.
    """
    try:
        return crud.create_titular(db=db, titular=titular)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{cuenta_id}/{cuentahabiente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_titular(cuenta_id: int, cuentahabiente_id: int, db: Session = Depends(get_db)):
    """
    Remover un titular de una cuenta.
    
    No se puede eliminar si es el único titular.
    """
    try:
        success = crud.delete_titular(db, cuenta_id=cuenta_id, cuentahabiente_id=cuentahabiente_id)
        if not success:
            raise HTTPException(status_code=404, detail="Titular no encontrado")
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))