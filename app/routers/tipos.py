from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.tipo_cuenta import TipoCuentaCreate, TipoCuentaUpdate, TipoCuentaResponse
from app.schemas.tipo_documento import TipoDocumentoCreate, TipoDocumentoUpdate, TipoDocumentoResponse
from app.schemas.tipo_movimiento import TipoMovimientoCreate, TipoMovimientoUpdate, TipoMovimientoResponse
from app.schemas.tipo_sucursal import TipoSucursalCreate, TipoSucursalUpdate, TipoSucursalResponse

from app.crud import tipo_cuenta as crud_tipo_cuenta
from app.crud import tipo_documento as crud_tipo_documento
from app.crud import tipo_movimiento as crud_tipo_movimiento
from app.crud import tipo_sucursal as crud_tipo_sucursal

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


@router.put("/cuenta/{tipo_cuenta_id}", response_model=TipoCuentaResponse, tags=["Tipos de Cuenta"])
def actualizar_tipo_cuenta(tipo_cuenta_id: int, tipo_cuenta: TipoCuentaUpdate, db: Session = Depends(get_db)):
    """Actualizar un tipo de cuenta"""
    tipo = crud_tipo_cuenta.update_tipo_cuenta(db, tipo_cuenta_id=tipo_cuenta_id, tipo_cuenta=tipo_cuenta)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.delete("/cuenta/{tipo_cuenta_id}", status_code=204, tags=["Tipos de Cuenta"])
def eliminar_tipo_cuenta(tipo_cuenta_id: int, db: Session = Depends(get_db)):
    """Eliminar un tipo de cuenta"""
    success = crud_tipo_cuenta.delete_tipo_cuenta(db, tipo_cuenta_id=tipo_cuenta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return None


# ============================================
# TIPOS DE DOCUMENTO
# ============================================

@router.get("/documento", response_model=List[TipoDocumentoResponse], tags=["Tipos de Documento"])
def listar_tipos_documento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de documento"""
    return crud_tipo_documento.get_tipos_documento(db, skip=skip, limit=limit)


@router.get("/documento/{tipo_documento_id}", response_model=TipoDocumentoResponse, tags=["Tipos de Documento"])
def obtener_tipo_documento(tipo_documento_id: int, db: Session = Depends(get_db)):
    """Obtener un tipo de documento por ID"""
    tipo = crud_tipo_documento.get_tipo_documento(db, tipo_documento_id=tipo_documento_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo


@router.post("/documento", response_model=TipoDocumentoResponse, status_code=201, tags=["Tipos de Documento"])
def crear_tipo_documento(tipo: TipoDocumentoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de documento"""
    return crud_tipo_documento.create_tipo_documento(db=db, tipo_documento=tipo)


@router.put("/documento/{tipo_documento_id}", response_model=TipoDocumentoResponse, tags=["Tipos de Documento"])
def actualizar_tipo_documento(tipo_documento_id: int, tipo: TipoDocumentoUpdate, db: Session = Depends(get_db)):
    """Actualizar un tipo de documento"""
    tipo_actualizado = crud_tipo_documento.update_tipo_documento(db, tipo_documento_id=tipo_documento_id, tipo_documento=tipo)
    if tipo_actualizado is None:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo_actualizado


@router.delete("/documento/{tipo_documento_id}", status_code=204, tags=["Tipos de Documento"])
def eliminar_tipo_documento(tipo_documento_id: int, db: Session = Depends(get_db)):
    """Eliminar un tipo de documento"""
    success = crud_tipo_documento.delete_tipo_documento(db, tipo_documento_id=tipo_documento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return None


# ============================================
# TIPOS DE MOVIMIENTO
# ============================================

@router.get("/movimiento", response_model=List[TipoMovimientoResponse], tags=["Tipos de Movimiento"])
def listar_tipos_movimiento(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de movimiento"""
    return crud_tipo_movimiento.get_tipos_movimiento(db, skip=skip, limit=limit)


@router.get("/movimiento/{tipo_movimiento_id}", response_model=TipoMovimientoResponse, tags=["Tipos de Movimiento"])
def obtener_tipo_movimiento(tipo_movimiento_id: int, db: Session = Depends(get_db)):
    """Obtener un tipo de movimiento por ID"""
    tipo = crud_tipo_movimiento.get_tipo_movimiento(db, tipo_movimiento_id=tipo_movimiento_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    return tipo


@router.post("/movimiento", response_model=TipoMovimientoResponse, status_code=201, tags=["Tipos de Movimiento"])
def crear_tipo_movimiento(tipo: TipoMovimientoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de movimiento"""
    return crud_tipo_movimiento.create_tipo_movimiento(db=db, tipo_movimiento=tipo)


@router.put("/movimiento/{tipo_movimiento_id}", response_model=TipoMovimientoResponse, tags=["Tipos de Movimiento"])
def actualizar_tipo_movimiento(tipo_movimiento_id: int, tipo: TipoMovimientoUpdate, db: Session = Depends(get_db)):
    """Actualizar un tipo de movimiento"""
    tipo_actualizado = crud_tipo_movimiento.update_tipo_movimiento(db, tipo_movimiento_id=tipo_movimiento_id, tipo_movimiento=tipo)
    if tipo_actualizado is None:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    return tipo_actualizado


@router.delete("/movimiento/{tipo_movimiento_id}", status_code=204, tags=["Tipos de Movimiento"])
def eliminar_tipo_movimiento(tipo_movimiento_id: int, db: Session = Depends(get_db)):
    """Eliminar un tipo de movimiento"""
    success = crud_tipo_movimiento.delete_tipo_movimiento(db, tipo_movimiento_id=tipo_movimiento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    return None


# ============================================
# TIPOS DE SUCURSAL
# ============================================

@router.get("/sucursal", response_model=List[TipoSucursalResponse], tags=["Tipos de Sucursal"])
def listar_tipos_sucursal(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de sucursal"""
    return crud_tipo_sucursal.get_tipos_sucursal(db, skip=skip, limit=limit)


@router.get("/sucursal/{tipo_sucursal_id}", response_model=TipoSucursalResponse, tags=["Tipos de Sucursal"])
def obtener_tipo_sucursal(tipo_sucursal_id: int, db: Session = Depends(get_db)):
    """Obtener un tipo de sucursal por ID"""
    tipo = crud_tipo_sucursal.get_tipo_sucursal(db, tipo_sucursal_id=tipo_sucursal_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de sucursal no encontrado")
    return tipo


@router.post("/sucursal", response_model=TipoSucursalResponse, status_code=201, tags=["Tipos de Sucursal"])
def crear_tipo_sucursal(tipo: TipoSucursalCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de sucursal"""
    return crud_tipo_sucursal.create_tipo_sucursal(db=db, tipo_sucursal=tipo)


@router.put("/sucursal/{tipo_sucursal_id}", response_model=TipoSucursalResponse, tags=["Tipos de Sucursal"])
def actualizar_tipo_sucursal(tipo_sucursal_id: int, tipo: TipoSucursalUpdate, db: Session = Depends(get_db)):
    """Actualizar un tipo de sucursal"""
    tipo_actualizado = crud_tipo_sucursal.update_tipo_sucursal(db, tipo_sucursal_id=tipo_sucursal_id, tipo_sucursal=tipo)
    if tipo_actualizado is None:
        raise HTTPException(status_code=404, detail="Tipo de sucursal no encontrado")
    return tipo_actualizado


@router.delete("/sucursal/{tipo_sucursal_id}", status_code=204, tags=["Tipos de Sucursal"])
def eliminar_tipo_sucursal(tipo_sucursal_id: int, db: Session = Depends(get_db)):
    """Eliminar un tipo de sucursal"""
    success = crud_tipo_sucursal.delete_tipo_sucursal(db, tipo_sucursal_id=tipo_sucursal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo de sucursal no encontrado")
    return None