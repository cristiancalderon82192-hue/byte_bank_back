from sqlalchemy.orm import Session
from app.models.tipo_movimiento import TipoMovimiento
from app.schemas.tipo_movimiento import TipoMovimientoCreate, TipoMovimientoUpdate
from typing import List, Optional


def get_tipo_movimiento(db: Session, tipo_movimiento_id: int) -> Optional[TipoMovimiento]:
    return db.query(TipoMovimiento).filter(TipoMovimiento.IdTipoMovimiento == tipo_movimiento_id).first()


def get_tipos_movimiento(db: Session, skip: int = 0, limit: int = 100) -> List[TipoMovimiento]:
    return db.query(TipoMovimiento).offset(skip).limit(limit).all()


def create_tipo_movimiento(db: Session, tipo_movimiento: TipoMovimientoCreate) -> TipoMovimiento:
    db_tipo_movimiento = TipoMovimiento(**tipo_movimiento.dict())
    db.add(db_tipo_movimiento)
    db.commit()
    db.refresh(db_tipo_movimiento)
    return db_tipo_movimiento


def update_tipo_movimiento(db: Session, tipo_movimiento_id: int, tipo_movimiento: TipoMovimientoUpdate) -> Optional[TipoMovimiento]:
    db_tipo_movimiento = get_tipo_movimiento(db, tipo_movimiento_id)
    if db_tipo_movimiento:
        update_data = tipo_movimiento.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tipo_movimiento, key, value)
        db.commit()
        db.refresh(db_tipo_movimiento)
    return db_tipo_movimiento


def delete_tipo_movimiento(db: Session, tipo_movimiento_id: int) -> bool:
    db_tipo_movimiento = get_tipo_movimiento(db, tipo_movimiento_id)
    if db_tipo_movimiento:
        db.delete(db_tipo_movimiento)
        db.commit()
        return True
    return False
