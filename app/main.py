from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import os
from dotenv import load_dotenv

# Importar routers
from app.routers import ciudades, cuentahabientes, cuentas, tipos, sucursales, movimientos, prestamos, titulares

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="API Bancaria ByteBank",
    description="API REST para sistema bancario con FastAPI y MySQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para Blazor
origins = [
    "http://localhost:5161",
    "http://localhost:5000",
    "http://localhost:5173",
    "*", # "*" para permitir todos (no recomendado en producción)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar todos los modelos para que SQLAlchemy los reconozca
from app.models import *

# Crear tablas (comentar si usas Alembic)
# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)

# Endpoint raíz
@app.get("/")
def read_root():
    return {
        "message": "API Bancaria ByteBank funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Endpoint para verificar conexión a BD
@app.get("/health")
def health_check():
    try:
        from app.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "API y base de datos funcionando correctamente"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Registrar routers
app.include_router(
    ciudades.router,
    prefix="/api/ciudades",
    tags=["Ciudades"]
)

app.include_router(
    tipos.router,
    prefix="/api/tipos",
    tags=["Catálogos"]
)

app.include_router(
    cuentahabientes.router,
    prefix="/api/cuentahabientes",
    tags=["Cuentahabientes"]
)

app.include_router(
    sucursales.router,
    prefix="/api/sucursales",
    tags=["Sucursales"]
)

app.include_router(
    cuentas.router,
    prefix="/api/cuentas",
    tags=["Cuentas"]
)

app.include_router(
    titulares.router,
    prefix="/api/titulares",
    tags=["Titulares"]
)

app.include_router(
    movimientos.router,
    prefix="/api/movimientos",
    tags=["Movimientos"]
)

app.include_router(
    prestamos.router,
    prefix="/api/prestamos",
    tags=["Préstamos"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )