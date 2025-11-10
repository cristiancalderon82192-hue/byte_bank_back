from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.tipo_cuenta import TipoCuentaCreate, TipoCuentaUpdate, TipoCuentaResponse
from app.schemas.tipo_documento import TipoDocumentoCreate, TipoDocumentoUpdate, TipoDocumentoResponse
from app.schemas.tipo_movimiento import TipoMovimientoCreate, TipoMovimientoUpdate, TipoMovimientoResponse
from app.schemas.tipo_sucursal import TipoSucursalCreate, TipoSucursalUpdate, TipoSucursalResponse

from app.crud import tipo_cuenta as crud_tipo_cuenta
from app.models.tipo_documento import TipoDocumento
from app.models.tipo_movimiento import TipoMovimiento
from app.models.tipo_sucursal import TipoSucursal

router = APIRouter()

# ============================================
# TIPOS DE CUENTA
# ============================================

@router.get("/cuenta", response_model=List[TipoCuentaResponse], tags=["Tipos de Cuenta"])
def listar_tipos_cuenta(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de cuenta"""
    return crud_tipo_cuenta.get_tipos_cuenta(db, skip=skip, limit=limit)


@router.get("/cuenta/{tipo_cuenta_id}", response_model=TipoCuentaResponse, tags=["Tipos de Cuenta"])
def obtener_tipo_cuenta(tipo_cuenta_id: int, db: Session = Depends(get_db)):
    """Obtener un tipo de cuenta por ID"""
    tipo = crud_tipo_cuenta.get_tipo_cuenta(db, tipo_cuenta_id=tipo_cuenta_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.post("/cuenta", response_model=TipoCuentaResponse, status_code=201, tags=["Tipos de Cuenta"])
def crear_tipo_cuenta(tipo_cuenta: TipoCuentaCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de cuenta"""
    return crud_tipo_cuenta.create_tipo_cuenta(db=db, tipo_cuenta=tipo_cuenta)


# ============================================
# TIPOS DE DOCUMENTO
# ============================================

@router.get("/documento", response_model=List[TipoDocumentoResponse], tags=["Tipos de Documento"])
def listar_tipos_documento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de documento"""
    return db.query(TipoDocumento).offset(skip).limit(limit).all()


@router.post("/documento", response_model=TipoDocumentoResponse, status_code=201, tags=["Tipos de Documento"])
def crear_tipo_documento(tipo: TipoDocumentoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de documento"""
    db_tipo = TipoDocumento(**tipo.dict())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo


# ============================================
# TIPOS DE MOVIMIENTO
# ============================================

@router.get("/movimiento", response_model=List[TipoMovimientoResponse], tags=["Tipos de Movimiento"])
def listar_tipos_movimiento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de movimiento"""
    return db.query(TipoMovimiento).offset(skip).limit(limit).all()


@router.post("/movimiento", response_model=TipoMovimientoResponse, status_code=201, tags=["Tipos de Movimiento"])
def crear_tipo_movimiento(tipo: TipoMovimientoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de movimiento"""
    db_tipo = TipoMovimiento(**tipo.dict())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo


# ============================================
# TIPOS DE SUCURSAL
# ============================================

@router.get("/sucursal", response_model=List[TipoSucursalResponse], tags=["Tipos de Sucursal"])
def listar_tipos_sucursal(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de sucursal"""
    return db.query(TipoSucursal).offset(skip).limit(limit).all()


@router.post("/sucursal", response_model=TipoSucursalResponse, status_code=201, tags=["Tipos de Sucursal"])
def crear_tipo_sucursal(tipo: TipoSucursalCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de sucursal"""
    db_tipo = TipoSucursal(**tipo.dict())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo