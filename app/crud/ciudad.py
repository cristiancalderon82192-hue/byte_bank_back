from sqlalchemy.orm import Session
from app.models.ciudad import Ciudad
from app.schemas.ciudad import CiudadCreate, CiudadUpdate
from typing import List, Optional


def get_ciudad(db: Session, ciudad_id: int) -> Optional[Ciudad]:
    """Obtener una ciudad por ID"""
    return db.query(Ciudad).filter(Ciudad.IdCiudad == ciudad_id).first()


def get_ciudades(db: Session, skip: int = 0, limit: int = 100) -> List[Ciudad]:
    """Obtener lista de ciudades con paginación"""
    return db.query(Ciudad).offset(skip).limit(limit).all()


def create_ciudad(db: Session, ciudad: CiudadCreate) -> Ciudad:
    """Crear una nueva ciudad"""
    db_ciudad = Ciudad(**ciudad.dict())
    db.add(db_ciudad)
    db.commit()
    db.refresh(db_ciudad)
    return db_ciudad


def update_ciudad(db: Session, ciudad_id: int, ciudad: CiudadUpdate) -> Optional[Ciudad]:
    """Actualizar una ciudad existente"""
    db_ciudad = get_ciudad(db, ciudad_id)
    if db_ciudad:
        update_data = ciudad.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ciudad, key, value)
        db.commit()
        db.refresh(db_ciudad)
    return db_ciudad


def delete_ciudad(db: Session, ciudad_id: int) -> bool:
    """Eliminar una ciudad"""
    db_ciudad = get_ciudad(db, ciudad_id)
    if db_ciudad:
        db.delete(db_ciudad)
        db.commit()
        return True
    return False