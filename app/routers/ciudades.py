from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.ciudad import CiudadCreate, CiudadUpdate, CiudadResponse
from app.crud import ciudad as crud

router = APIRouter()


@router.get("/", response_model=List[CiudadResponse])
def listar_ciudades(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de todas las ciudades"""
    ciudades = crud.get_ciudades(db, skip=skip, limit=limit)
    return ciudades


@router.get("/{ciudad_id}", response_model=CiudadResponse)
def obtener_ciudad(
    ciudad_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una ciudad por ID"""
    ciudad = crud.get_ciudad(db, ciudad_id=ciudad_id)
    if ciudad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ciudad con ID {ciudad_id} no encontrada"
        )
    return ciudad


@router.post("/", response_model=CiudadResponse, status_code=status.HTTP_201_CREATED)
def crear_ciudad(
    ciudad: CiudadCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva ciudad"""
    return crud.create_ciudad(db=db, ciudad=ciudad)


@router.put("/{ciudad_id}", response_model=CiudadResponse)
def actualizar_ciudad(
    ciudad_id: int,
    ciudad: CiudadUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una ciudad existente"""
    db_ciudad = crud.update_ciudad(db, ciudad_id=ciudad_id, ciudad=ciudad)
    if db_ciudad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ciudad con ID {ciudad_id} no encontrada"
        )
    return db_ciudad


@router.delete("/{ciudad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ciudad(
    ciudad_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una ciudad"""
    success = crud.delete_ciudad(db, ciudad_id=ciudad_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ciudad con ID {ciudad_id} no encontrada"
        )
    return None