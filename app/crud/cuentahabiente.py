from sqlalchemy.orm import Session, joinedload
from app.models.cuentahabiente import Cuentahabiente
from app.models.ciudad import Ciudad
from app.models.tipo_documento import TipoDocumento
from app.schemas.cuentahabiente import CuentahabienteCreate, CuentahabienteUpdate
from typing import List, Optional


def get_cuentahabiente(db: Session, cuentahabiente_id: int) -> Optional[Cuentahabiente]:
    """Obtener un cuentahabiente por ID con información relacionada"""
    return db.query(Cuentahabiente).options(
        joinedload(Cuentahabiente.ciudad),
        joinedload(Cuentahabiente.tipo_documento)
    ).filter(Cuentahabiente.IdCuentahabiente == cuentahabiente_id).first()


def get_cuentahabiente_by_documento(db: Session, documento: str) -> Optional[Cuentahabiente]:
    """Obtener un cuentahabiente por número de documento con información relacionada"""
    return db.query(Cuentahabiente).options(
        joinedload(Cuentahabiente.ciudad),
        joinedload(Cuentahabiente.tipo_documento)
    ).filter(Cuentahabiente.Documento == documento).first()


def get_cuentahabientes(db: Session, skip: int = 0, limit: int = 100) -> List[Cuentahabiente]:
    """Obtener lista de cuentahabientes con paginación e información relacionada"""
    return db.query(Cuentahabiente).options(
        joinedload(Cuentahabiente.ciudad),
        joinedload(Cuentahabiente.tipo_documento)
    ).offset(skip).limit(limit).all()


def create_cuentahabiente(db: Session, cuentahabiente: CuentahabienteCreate) -> Cuentahabiente:
    """Crear un nuevo cuentahabiente"""
    db_cuentahabiente = Cuentahabiente(**cuentahabiente.dict())
    db.add(db_cuentahabiente)
    db.commit()
    db.refresh(db_cuentahabiente)
    return db_cuentahabiente


def update_cuentahabiente(db: Session, cuentahabiente_id: int, cuentahabiente: CuentahabienteUpdate) -> Optional[Cuentahabiente]:
    """Actualizar un cuentahabiente existente"""
    db_cuentahabiente = get_cuentahabiente(db, cuentahabiente_id)
    if db_cuentahabiente:
        update_data = cuentahabiente.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cuentahabiente, key, value)
        db.commit()
        db.refresh(db_cuentahabiente)
    return db_cuentahabiente


def delete_cuentahabiente(db: Session, cuentahabiente_id: int) -> bool:
    """Eliminar un cuentahabiente"""
    db_cuentahabiente = get_cuentahabiente(db, cuentahabiente_id)
    if db_cuentahabiente:
        db.delete(db_cuentahabiente)
        db.commit()
        return True
    return False
