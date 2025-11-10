from sqlalchemy.orm import Session
from app.models.movimiento import Movimiento
from app.models.cuenta import Cuenta
from app.schemas.movimiento import (
    MovimientoCreate, DepositoCreate, RetiroCreate, TransferenciaCreate
)
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal


def get_movimiento(db: Session, movimiento_id: int) -> Optional[Movimiento]:
    return db.query(Movimiento).filter(Movimiento.IdMovimiento == movimiento_id).first()


def get_movimientos(db: Session, skip: int = 0, limit: int = 100) -> List[Movimiento]:
    return db.query(Movimiento).order_by(Movimiento.Fecha.desc()).offset(skip).limit(limit).all()


def get_movimientos_by_cuenta(db: Session, cuenta_id: int, skip: int = 0, limit: int = 100) -> List[Movimiento]:
    return db.query(Movimiento).filter(
        Movimiento.IdCuenta == cuenta_id
    ).order_by(Movimiento.Fecha.desc()).offset(skip).limit(limit).all()


def get_movimientos_by_fecha(db: Session, fecha_inicio: date, fecha_fin: date) -> List[Movimiento]:
    return db.query(Movimiento).filter(
        Movimiento.Fecha >= fecha_inicio,
        Movimiento.Fecha <= fecha_fin
    ).order_by(Movimiento.Fecha.desc()).all()


def create_movimiento(db: Session, movimiento: MovimientoCreate) -> Movimiento:
    db_movimiento = Movimiento(**movimiento.dict())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


def realizar_deposito(db: Session, deposito: DepositoCreate) -> Movimiento:
    """Realizar un depósito en una cuenta"""
    # Obtener la cuenta
    cuenta = db.query(Cuenta).filter(Cuenta.IdCuenta == deposito.IdCuenta).first()
    if not cuenta:
        raise ValueError(f"Cuenta con ID {deposito.IdCuenta} no encontrada")
    
    # Actualizar saldo
    cuenta.Saldo += deposito.Valor
    
    # Crear movimiento (tipo 1 = Depósito)
    movimiento = Movimiento(
        IdCuenta=deposito.IdCuenta,
        IdSucursal=deposito.IdSucursal,
        Fecha=date.today(),
        Valor=deposito.Valor,
        IdTipoMovimiento=1,  # Depósito
        Descripcion=deposito.Descripcion or "Depósito"
    )
    
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    db.refresh(cuenta)
    
    return movimiento


def realizar_retiro(db: Session, retiro: RetiroCreate) -> Movimiento:
    """Realizar un retiro de una cuenta"""
    # Obtener la cuenta
    cuenta = db.query(Cuenta).filter(Cuenta.IdCuenta == retiro.IdCuenta).first()
    if not cuenta:
        raise ValueError(f"Cuenta con ID {retiro.IdCuenta} no encontrada")
    
    # Verificar saldo disponible (saldo + sobregiro)
    saldo_disponible = cuenta.Saldo + (cuenta.Sobregiro or Decimal("0"))
    if retiro.Valor > saldo_disponible:
        raise ValueError(f"Saldo insuficiente. Disponible: {saldo_disponible}, Solicitado: {retiro.Valor}")
    
    # Actualizar saldo
    cuenta.Saldo -= retiro.Valor
    
    # Marcar sobregiro no autorizado si el saldo es negativo
    if cuenta.Saldo < 0:
        cuenta.SobregiroNoAutorizado = True
    
    # Crear movimiento (tipo 2 = Retiro)
    movimiento = Movimiento(
        IdCuenta=retiro.IdCuenta,
        IdSucursal=retiro.IdSucursal,
        Fecha=date.today(),
        Valor=-retiro.Valor,  # Negativo para retiros
        IdTipoMovimiento=2,  # Retiro
        Descripcion=retiro.Descripcion or "Retiro"
    )
    
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    db.refresh(cuenta)
    
    return movimiento


def realizar_transferencia(db: Session, transferencia: TransferenciaCreate) -> tuple[Movimiento, Movimiento]:
    """Realizar una transferencia entre dos cuentas"""
    # Obtener cuentas
    cuenta_origen = db.query(Cuenta).filter(Cuenta.IdCuenta == transferencia.IdCuentaOrigen).first()
    cuenta_destino = db.query(Cuenta).filter(Cuenta.IdCuenta == transferencia.IdCuentaDestino).first()
    
    if not cuenta_origen:
        raise ValueError(f"Cuenta origen con ID {transferencia.IdCuentaOrigen} no encontrada")
    if not cuenta_destino:
        raise ValueError(f"Cuenta destino con ID {transferencia.IdCuentaDestino} no encontrada")
    
    # Verificar saldo disponible
    saldo_disponible = cuenta_origen.Saldo + (cuenta_origen.Sobregiro or Decimal("0"))
    if transferencia.Valor > saldo_disponible:
        raise ValueError(f"Saldo insuficiente. Disponible: {saldo_disponible}, Solicitado: {transferencia.Valor}")
    
    # Actualizar saldos
    cuenta_origen.Saldo -= transferencia.Valor
    cuenta_destino.Saldo += transferencia.Valor
    
    # Marcar sobregiro en cuenta origen si aplica
    if cuenta_origen.Saldo < 0:
        cuenta_origen.SobregiroNoAutorizado = True
    
    # Crear movimiento de salida (tipo 3 = Transferencia Enviada)
    movimiento_salida = Movimiento(
        IdCuenta=transferencia.IdCuentaOrigen,
        IdSucursal=transferencia.IdSucursal,
        Fecha=date.today(),
        Valor=-transferencia.Valor,
        IdTipoMovimiento=3,  # Transferencia Enviada
        Descripcion=transferencia.Descripcion or f"Transferencia a cuenta {cuenta_destino.Numero}"
    )
    
    # Crear movimiento de entrada (tipo 4 = Transferencia Recibida)
    movimiento_entrada = Movimiento(
        IdCuenta=transferencia.IdCuentaDestino,
        IdSucursal=transferencia.IdSucursal,
        Fecha=date.today(),
        Valor=transferencia.Valor,
        IdTipoMovimiento=4,  # Transferencia Recibida
        Descripcion=transferencia.Descripcion or f"Transferencia desde cuenta {cuenta_origen.Numero}"
    )
    
    db.add(movimiento_salida)
    db.add(movimiento_entrada)
    db.commit()
    db.refresh(movimiento_salida)
    db.refresh(movimiento_entrada)
    db.refresh(cuenta_origen)
    db.refresh(cuenta_destino)
    
    return movimiento_salida, movimiento_entrada