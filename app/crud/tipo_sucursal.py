from sqlalchemy.orm import Session
from app.models.tipo_sucursal import TipoSucursal
from app.schemas.tipo_sucursal import TipoSucursalCreate, TipoSucursalUpdate
from typing import List, Optional


def get_tipo_sucursal(db: Session, tipo_sucursal_id: int) -> Optional[TipoSucursal]:
    return db.query(TipoSucursal).filter(TipoSucursal.IdTipoSucursal == tipo_sucursal_id).first()


def get_tipos_sucursal(db: Session, skip: int = 0, limit: int = 100) -> List[TipoSucursal]:
    return db.query(TipoSucursal).offset(skip).limit(limit).all()


def create_tipo_sucursal(db: Session, tipo_sucursal: TipoSucursalCreate) -> TipoSucursal:
    db_tipo_sucursal = TipoSucursal(**tipo_sucursal.dict())
    db.add(db_tipo_sucursal)
    db.commit()
    db.refresh(db_tipo_sucursal)
    return db_tipo_sucursal


def update_tipo_sucursal(db: Session, tipo_sucursal_id: int, tipo_sucursal: TipoSucursalUpdate) -> Optional[TipoSucursal]:
    db_tipo_sucursal = get_tipo_sucursal(db, tipo_sucursal_id)
    if db_tipo_sucursal:
        update_data = tipo_sucursal.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tipo_sucursal, key, value)
        db.commit()
        db.refresh(db_tipo_sucursal)
    return db_tipo_sucursal


def delete_tipo_sucursal(db: Session, tipo_sucursal_id: int) -> bool:
    db_tipo_sucursal = get_tipo_sucursal(db, tipo_sucursal_id)
    if db_tipo_sucursal:
        db.delete(db_tipo_sucursal)
        db.commit()
        return True
    return False
