from sqlalchemy.orm import Session
from app.models.titular import Titular
from app.models.cuenta import Cuenta
from app.models.cuentahabiente import Cuentahabiente
from app.schemas.titular import TitularCreate
from typing import List


def get_titular(db: Session, cuenta_id: int, cuentahabiente_id: int) -> Titular:
    return db.query(Titular).filter(
        Titular.IdCuenta == cuenta_id,
        Titular.IdCuentahabiente == cuentahabiente_id
    ).first()


def get_titulares_by_cuenta(db: Session, cuenta_id: int) -> List[dict]:
    """Obtener todos los titulares de una cuenta con información detallada"""
    return db.query(
        Titular.IdCuenta,
        Titular.IdCuentahabiente,
        Cuentahabiente.Nombre,
        Cuentahabiente.Documento,
        Cuenta.Numero
    ).join(
        Cuentahabiente, Titular.IdCuentahabiente == Cuentahabiente.IdCuentahabiente
    ).join(
        Cuenta, Titular.IdCuenta == Cuenta.IdCuenta
    ).filter(
        Titular.IdCuenta == cuenta_id
    ).all()


def get_cuentas_by_cuentahabiente(db: Session, cuentahabiente_id: int) -> List[dict]:
    """Obtener todas las cuentas de un cuentahabiente"""
    return db.query(
        Titular.IdCuenta,
        Titular.IdCuentahabiente,
        Cuenta.Numero,
        Cuenta.Saldo,
        Cuentahabiente.Nombre
    ).join(
        Cuenta, Titular.IdCuenta == Cuenta.IdCuenta
    ).join(
        Cuentahabiente, Titular.IdCuentahabiente == Cuentahabiente.IdCuentahabiente
    ).filter(
        Titular.IdCuentahabiente == cuentahabiente_id
    ).all()


def create_titular(db: Session, titular: TitularCreate) -> Titular:
    """Asociar un cuentahabiente como titular de una cuenta"""
    # Verificar que la cuenta existe
    cuenta = db.query(Cuenta).filter(Cuenta.IdCuenta == titular.IdCuenta).first()
    if not cuenta:
        raise ValueError(f"Cuenta con ID {titular.IdCuenta} no encontrada")
    
    # Verificar que el cuentahabiente existe
    cuentahabiente = db.query(Cuentahabiente).filter(
        Cuentahabiente.IdCuentahabiente == titular.IdCuentahabiente
    ).first()
    if not cuentahabiente:
        raise ValueError(f"Cuentahabiente con ID {titular.IdCuentahabiente} no encontrado")
    
    # Verificar que no existe ya esta relación
    existing = get_titular(db, titular.IdCuenta, titular.IdCuentahabiente)
    if existing:
        raise ValueError(f"El cuentahabiente ya es titular de esta cuenta")
    
    db_titular = Titular(**titular.dict())
    db.add(db_titular)
    db.commit()
    db.refresh(db_titular)
    return db_titular


def delete_titular(db: Session, cuenta_id: int, cuentahabiente_id: int) -> bool:
    """Remover un titular de una cuenta"""
    db_titular = get_titular(db, cuenta_id, cuentahabiente_id)
    if db_titular:
        # Verificar que no sea el único titular
        count = db.query(Titular).filter(Titular.IdCuenta == cuenta_id).count()
        if count <= 1:
            raise ValueError("No se puede eliminar el único titular de la cuenta")
        
        db.delete(db_titular)
        db.commit()
        return True
    return False