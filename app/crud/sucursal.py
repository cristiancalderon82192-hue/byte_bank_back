from sqlalchemy.orm import Session
from app.models.sucursal import Sucursal
from app.schemas.sucursal import SucursalCreate, SucursalUpdate
from typing import List, Optional


def get_sucursal(db: Session, sucursal_id: int) -> Optional[Sucursal]:
    return db.query(Sucursal).filter(Sucursal.IdSucursal == sucursal_id).first()


def get_sucursales(db: Session, skip: int = 0, limit: int = 100) -> List[Sucursal]:
    return db.query(Sucursal).offset(skip).limit(limit).all()


def get_sucursales_by_ciudad(db: Session, ciudad_id: int) -> List[Sucursal]:
    return db.query(Sucursal).filter(Sucursal.IdCiudad == ciudad_id).all()


def create_sucursal(db: Session, sucursal: SucursalCreate) -> Sucursal:
    db_sucursal = Sucursal(**sucursal.dict())
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal


def update_sucursal(db: Session, sucursal_id: int, sucursal: SucursalUpdate) -> Optional[Sucursal]:
    db_sucursal = get_sucursal(db, sucursal_id)
    if db_sucursal:
        update_data = sucursal.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sucursal, key, value)
        db.commit()
        db.refresh(db_sucursal)
    return db_sucursal


def delete_sucursal(db: Session, sucursal_id: int) -> bool:
    db_sucursal = get_sucursal(db, sucursal_id)
    if db_sucursal:
        db.delete(db_sucursal)
        db.commit()
        return True
    return False