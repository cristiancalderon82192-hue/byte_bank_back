from sqlalchemy.orm import Session
from app.models.cuenta import Cuenta
from app.schemas.cuenta import CuentaCreate, CuentaUpdate
from typing import List, Optional


def get_cuenta(db: Session, cuenta_id: int) -> Optional[Cuenta]:
    """Obtener una cuenta por ID"""
    return db.query(Cuenta).filter(Cuenta.IdCuenta == cuenta_id).first()


def get_cuenta_by_numero(db: Session, numero: str) -> Optional[Cuenta]:
    """Obtener una cuenta por número"""
    return db.query(Cuenta).filter(Cuenta.Numero == numero).first()


def get_cuentas(db: Session, skip: int = 0, limit: int = 100) -> List[Cuenta]:
    """Obtener lista de cuentas con paginación"""
    return db.query(Cuenta).offset(skip).limit(limit).all()


def get_cuentas_by_sucursal(db: Session, sucursal_id: int) -> List[Cuenta]:
    """Obtener cuentas de una sucursal específica"""
    return db.query(Cuenta).filter(Cuenta.IdSucursal == sucursal_id).all()


def create_cuenta(db: Session, cuenta: CuentaCreate) -> Cuenta:
    """Crear una nueva cuenta"""
    db_cuenta = Cuenta(**cuenta.dict())
    db.add(db_cuenta)
    db.commit()
    db.refresh(db_cuenta)
    return db_cuenta


def update_cuenta(db: Session, cuenta_id: int, cuenta: CuentaUpdate) -> Optional[Cuenta]:
    """Actualizar una cuenta existente"""
    db_cuenta = get_cuenta(db, cuenta_id)
    if db_cuenta:
        update_data = cuenta.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cuenta, key, value)
        db.commit()
        db.refresh(db_cuenta)
    return db_cuenta


def delete_cuenta(db: Session, cuenta_id: int) -> bool:
    """Eliminar una cuenta"""
    db_cuenta = get_cuenta(db, cuenta_id)
    if db_cuenta:
        db.delete(db_cuenta)
        db.commit()
        return True
    return False


def get_saldo_cuenta(db: Session, cuenta_id: int) -> Optional[dict]:
    """Consultar el saldo de una cuenta"""
    cuenta = get_cuenta(db, cuenta_id)
    if cuenta:
        return {
            "IdCuenta": cuenta.IdCuenta,
            "Numero": cuenta.Numero,
            "Saldo": cuenta.Saldo,
            "Sobregiro": cuenta.Sobregiro,
            "SaldoDisponible": cuenta.Saldo + (cuenta.Sobregiro or 0)
        }
    return None