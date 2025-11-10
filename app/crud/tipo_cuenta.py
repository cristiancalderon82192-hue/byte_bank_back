from sqlalchemy.orm import Session
from app.models.tipo_cuenta import TipoCuenta
from app.schemas.tipo_cuenta import TipoCuentaCreate, TipoCuentaUpdate
from typing import List, Optional


def get_tipo_cuenta(db: Session, tipo_cuenta_id: int) -> Optional[TipoCuenta]:
    return db.query(TipoCuenta).filter(TipoCuenta.IdTipoCuenta == tipo_cuenta_id).first()


def get_tipos_cuenta(db: Session, skip: int = 0, limit: int = 100) -> List[TipoCuenta]:
    return db.query(TipoCuenta).offset(skip).limit(limit).all()


def create_tipo_cuenta(db: Session, tipo_cuenta: TipoCuentaCreate) -> TipoCuenta:
    db_tipo_cuenta = TipoCuenta(**tipo_cuenta.dict())
    db.add(db_tipo_cuenta)
    db.commit()
    db.refresh(db_tipo_cuenta)
    return db_tipo_cuenta


def update_tipo_cuenta(db: Session, tipo_cuenta_id: int, tipo_cuenta: TipoCuentaUpdate) -> Optional[TipoCuenta]:
    db_tipo_cuenta = get_tipo_cuenta(db, tipo_cuenta_id)
    if db_tipo_cuenta:
        update_data = tipo_cuenta.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tipo_cuenta, key, value)
        db.commit()
        db.refresh(db_tipo_cuenta)
    return db_tipo_cuenta


def delete_tipo_cuenta(db: Session, tipo_cuenta_id: int) -> bool:
    db_tipo_cuenta = get_tipo_cuenta(db, tipo_cuenta_id)
    if db_tipo_cuenta:
        db.delete(db_tipo_cuenta)
        db.commit()
        return True
    return False