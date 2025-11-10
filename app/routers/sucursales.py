from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.sucursal import SucursalCreate, SucursalUpdate, SucursalResponse
from app.crud import sucursal as crud

router = APIRouter()


@router.get("/", response_model=List[SucursalResponse])
def listar_sucursales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las sucursales"""
    return crud.get_sucursales(db, skip=skip, limit=limit)


@router.get("/{sucursal_id}", response_model=SucursalResponse)
def obtener_sucursal(sucursal_id: int, db: Session = Depends(get_db)):
    """Obtener una sucursal por ID"""
    sucursal = crud.get_sucursal(db, sucursal_id=sucursal_id)
    if sucursal is None:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal


@router.get("/ciudad/{ciudad_id}", response_model=List[SucursalResponse])
def listar_sucursales_por_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    """Obtener sucursales de una ciudad específica"""
    return crud.get_sucursales_by_ciudad(db, ciudad_id=ciudad_id)


@router.post("/", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
def crear_sucursal(sucursal: SucursalCreate, db: Session = Depends(get_db)):
    """Crear una nueva sucursal"""
    return crud.create_sucursal(db=db, sucursal=sucursal)


@router.put("/{sucursal_id}", response_model=SucursalResponse)
def actualizar_sucursal(sucursal_id: int, sucursal: SucursalUpdate, db: Session = Depends(get_db)):
    """Actualizar una sucursal existente"""
    db_sucursal = crud.update_sucursal(db, sucursal_id=sucursal_id, sucursal=sucursal)
    if db_sucursal is None:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return db_sucursal


@router.delete("/{sucursal_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sucursal(sucursal_id: int, db: Session = Depends(get_db)):
    """Eliminar una sucursal"""
    success = crud.delete_sucursal(db, sucursal_id=sucursal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return None