from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.cuenta import CuentaCreate, CuentaUpdate, CuentaResponse
from app.crud import cuenta as crud

router = APIRouter()


@router.get("/", response_model=List[CuentaResponse])
def listar_cuentas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de todas las cuentas"""
    cuentas = crud.get_cuentas(db, skip=skip, limit=limit)
    return cuentas


@router.get("/{cuenta_id}", response_model=CuentaResponse)
def obtener_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una cuenta por ID"""
    cuenta = crud.get_cuenta(db, cuenta_id=cuenta_id)
    if cuenta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {cuenta_id} no encontrada"
        )
    return cuenta


@router.get("/numero/{numero}", response_model=CuentaResponse)
def obtener_cuenta_por_numero(
    numero: str,
    db: Session = Depends(get_db)
):
    """Buscar cuenta por número"""
    cuenta = crud.get_cuenta_by_numero(db, numero=numero)
    if cuenta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con número {numero} no encontrada"
        )
    return cuenta


@router.get("/{cuenta_id}/saldo")
def consultar_saldo(
    cuenta_id: int,
    db: Session = Depends(get_db)
):
    """Consultar saldo de una cuenta"""
    saldo = crud.get_saldo_cuenta(db, cuenta_id=cuenta_id)
    if saldo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {cuenta_id} no encontrada"
        )
    return saldo


@router.post("/", response_model=CuentaResponse, status_code=status.HTTP_201_CREATED)
def crear_cuenta(
    cuenta: CuentaCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva cuenta"""
    # Verificar si el número de cuenta ya existe
    db_cuenta = crud.get_cuenta_by_numero(db, numero=cuenta.Numero)
    if db_cuenta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una cuenta con el número {cuenta.Numero}"
        )
    return crud.create_cuenta(db=db, cuenta=cuenta)


@router.put("/{cuenta_id}", response_model=CuentaResponse)
def actualizar_cuenta(
    cuenta_id: int,
    cuenta: CuentaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una cuenta existente"""
    db_cuenta = crud.update_cuenta(db, cuenta_id=cuenta_id, cuenta=cuenta)
    if db_cuenta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {cuenta_id} no encontrada"
        )
    return db_cuenta


@router.delete("/{cuenta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una cuenta"""
    success = crud.delete_cuenta(db, cuenta_id=cuenta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {cuenta_id} no encontrada"
        )
    return None