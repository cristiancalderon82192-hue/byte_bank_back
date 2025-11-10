from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.prestamo import (
    PrestamoCreate, PrestamoUpdate, PrestamoResponse,
    CalculoCuota, CalculoCuotaResponse
)
from app.crud import prestamo as crud

router = APIRouter()


@router.get("/", response_model=List[PrestamoResponse])
def listar_prestamos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todos los préstamos"""
    return crud.get_prestamos(db, skip=skip, limit=limit)


@router.get("/{prestamo_id}", response_model=PrestamoResponse)
def obtener_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    """Obtener un préstamo por ID"""
    prestamo = crud.get_prestamo(db, prestamo_id=prestamo_id)
    if prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


@router.get("/numero/{numero}", response_model=PrestamoResponse)
def obtener_prestamo_por_numero(numero: str, db: Session = Depends(get_db)):
    """Buscar préstamo por número"""
    prestamo = crud.get_prestamo_by_numero(db, numero=numero)
    if prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


@router.get("/cuenta/{cuenta_id}", response_model=List[PrestamoResponse])
def listar_prestamos_por_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    """Obtener préstamos de una cuenta específica"""
    return crud.get_prestamos_by_cuenta(db, cuenta_id=cuenta_id)


@router.post("/calcular-cuota", response_model=CalculoCuotaResponse)
def calcular_cuota_prestamo(datos: CalculoCuota):
    """
    Calcular la cuota mensual de un préstamo.
    
    Utiliza la fórmula de amortización francesa para calcular:
    - Cuota mensual
    - Total a pagar
    - Total de intereses
    """
    return crud.calcular_cuota(datos)


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def crear_prestamo(prestamo: PrestamoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo préstamo.
    
    Si no se proporciona la cuota, se calcula automáticamente.
    """
    # Verificar si el número ya existe
    db_prestamo = crud.get_prestamo_by_numero(db, numero=prestamo.Numero)
    if db_prestamo:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un préstamo con el número {prestamo.Numero}"
        )
    return crud.create_prestamo(db=db, prestamo=prestamo)


@router.put("/{prestamo_id}", response_model=PrestamoResponse)
def actualizar_prestamo(
    prestamo_id: int,
    prestamo: PrestamoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un préstamo existente.
    
    Si se actualizan los parámetros (tasa, plazo, seguro),
    la cuota se recalcula automáticamente.
    """
    db_prestamo = crud.update_prestamo(db, prestamo_id=prestamo_id, prestamo=prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return db_prestamo


@router.delete("/{prestamo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    """Eliminar un préstamo"""
    success = crud.delete_prestamo(db, prestamo_id=prestamo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return None