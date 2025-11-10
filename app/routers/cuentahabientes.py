from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.cuentahabiente import CuentahabienteCreate, CuentahabienteUpdate, CuentahabienteResponse
from app.crud import cuentahabiente as crud

router = APIRouter()


@router.get("/", response_model=List[CuentahabienteResponse])
def listar_cuentahabientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de todos los cuentahabientes"""
    cuentahabientes = crud.get_cuentahabientes(db, skip=skip, limit=limit)
    return cuentahabientes


@router.get("/{cuentahabiente_id}", response_model=CuentahabienteResponse)
def obtener_cuentahabiente(
    cuentahabiente_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un cuentahabiente por ID"""
    cuentahabiente = crud.get_cuentahabiente(db, cuentahabiente_id=cuentahabiente_id)
    if cuentahabiente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuentahabiente con ID {cuentahabiente_id} no encontrado"
        )
    return cuentahabiente


@router.get("/documento/{documento}", response_model=CuentahabienteResponse)
def obtener_cuentahabiente_por_documento(
    documento: str,
    db: Session = Depends(get_db)
):
    """Buscar cuentahabiente por número de documento"""
    cuentahabiente = crud.get_cuentahabiente_by_documento(db, documento=documento)
    if cuentahabiente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuentahabiente con documento {documento} no encontrado"
        )
    return cuentahabiente


@router.post("/", response_model=CuentahabienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cuentahabiente(
    cuentahabiente: CuentahabienteCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo cuentahabiente"""
    # Verificar si el documento ya existe
    db_cuentahabiente = crud.get_cuentahabiente_by_documento(db, documento=cuentahabiente.Documento)
    if db_cuentahabiente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un cuentahabiente con el documento {cuentahabiente.Documento}"
        )
    return crud.create_cuentahabiente(db=db, cuentahabiente=cuentahabiente)


@router.put("/{cuentahabiente_id}", response_model=CuentahabienteResponse)
def actualizar_cuentahabiente(
    cuentahabiente_id: int,
    cuentahabiente: CuentahabienteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un cuentahabiente existente"""
    db_cuentahabiente = crud.update_cuentahabiente(db, cuentahabiente_id=cuentahabiente_id, cuentahabiente=cuentahabiente)
    if db_cuentahabiente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuentahabiente con ID {cuentahabiente_id} no encontrado"
        )
    return db_cuentahabiente


@router.delete("/{cuentahabiente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cuentahabiente(
    cuentahabiente_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un cuentahabiente"""
    success = crud.delete_cuentahabiente(db, cuentahabiente_id=cuentahabiente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuentahabiente con ID {cuentahabiente_id} no encontrado"
        )
    return None