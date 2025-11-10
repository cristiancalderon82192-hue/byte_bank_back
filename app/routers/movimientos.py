from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.schemas.movimiento import (
    MovimientoResponse, DepositoCreate, RetiroCreate, TransferenciaCreate
)
from app.crud import movimiento as crud

router = APIRouter()


@router.get("/", response_model=List[MovimientoResponse])
def listar_movimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de movimientos"""
    return crud.get_movimientos(db, skip=skip, limit=limit)


@router.get("/{movimiento_id}", response_model=MovimientoResponse)
def obtener_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    """Obtener un movimiento por ID"""
    movimiento = crud.get_movimiento(db, movimiento_id=movimiento_id)
    if movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento


@router.get("/cuenta/{cuenta_id}", response_model=List[MovimientoResponse])
def listar_movimientos_por_cuenta(
    cuenta_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener movimientos de una cuenta específica"""
    return crud.get_movimientos_by_cuenta(db, cuenta_id=cuenta_id, skip=skip, limit=limit)


@router.get("/fecha/{fecha_inicio}/{fecha_fin}", response_model=List[MovimientoResponse])
def listar_movimientos_por_fecha(
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    """Obtener movimientos en un rango de fechas"""
    return crud.get_movimientos_by_fecha(db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@router.post("/deposito", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def realizar_deposito(deposito: DepositoCreate, db: Session = Depends(get_db)):
    """
    Realizar un depósito en una cuenta.
    
    Actualiza automáticamente el saldo de la cuenta.
    """
    try:
        return crud.realizar_deposito(db=db, deposito=deposito)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/retiro", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def realizar_retiro(retiro: RetiroCreate, db: Session = Depends(get_db)):
    """
    Realizar un retiro de una cuenta.
    
    Valida el saldo disponible y actualiza el saldo de la cuenta.
    """
    try:
        return crud.realizar_retiro(db=db, retiro=retiro)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transferencia", status_code=status.HTTP_201_CREATED)
def realizar_transferencia(transferencia: TransferenciaCreate, db: Session = Depends(get_db)):
    """
    Realizar una transferencia entre dos cuentas.
    
    Crea dos movimientos: uno de débito en la cuenta origen
    y uno de crédito en la cuenta destino.
    """
    try:
        mov_salida, mov_entrada = crud.realizar_transferencia(db=db, transferencia=transferencia)
        return {
            "mensaje": "Transferencia realizada exitosamente",
            "movimiento_salida": {
                "IdMovimiento": mov_salida.IdMovimiento,
                "IdCuenta": mov_salida.IdCuenta,
                "Valor": mov_salida.Valor
            },
            "movimiento_entrada": {
                "IdMovimiento": mov_entrada.IdMovimiento,
                "IdCuenta": mov_entrada.IdCuenta,
                "Valor": mov_entrada.Valor
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))