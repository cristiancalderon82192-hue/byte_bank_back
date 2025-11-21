from sqlalchemy.orm import Session
from app.models.tipo_documento import TipoDocumento
from app.schemas.tipo_documento import TipoDocumentoCreate, TipoDocumentoUpdate
from typing import List, Optional


def get_tipo_documento(db: Session, tipo_documento_id: int) -> Optional[TipoDocumento]:
    return db.query(TipoDocumento).filter(TipoDocumento.IdTipoDocumento == tipo_documento_id).first()


def get_tipos_documento(db: Session, skip: int = 0, limit: int = 100) -> List[TipoDocumento]:
    return db.query(TipoDocumento).offset(skip).limit(limit).all()


def create_tipo_documento(db: Session, tipo_documento: TipoDocumentoCreate) -> TipoDocumento:
    db_tipo_documento = TipoDocumento(**tipo_documento.dict())
    db.add(db_tipo_documento)
    db.commit()
    db.refresh(db_tipo_documento)
    return db_tipo_documento


def update_tipo_documento(db: Session, tipo_documento_id: int, tipo_documento: TipoDocumentoUpdate) -> Optional[TipoDocumento]:
    db_tipo_documento = get_tipo_documento(db, tipo_documento_id)
    if db_tipo_documento:
        update_data = tipo_documento.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tipo_documento, key, value)
        db.commit()
        db.refresh(db_tipo_documento)
    return db_tipo_documento


def delete_tipo_documento(db: Session, tipo_documento_id: int) -> bool:
    db_tipo_documento = get_tipo_documento(db, tipo_documento_id)
    if db_tipo_documento:
        db.delete(db_tipo_documento)
        db.commit()
        return True
    return False
