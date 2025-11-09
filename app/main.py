from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="API Bancaria",
    description="API REST para sistema bancario con FastAPI y MySQL",
    version="1.0.0"
)

# Configurar CORS para Blazor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar todos los modelos para que SQLAlchemy los reconozca
from app.models import *

# Crear tablas (temporal, luego usaremos Alembic)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Endpoint de prueba
@app.get("/")
def read_root():
    return {
        "message": "API Bancaria funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Endpoint para verificar conexión a BD
@app.get("/health")
def health_check():
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Aquí se registrarán los routers en fases posteriores
# app.include_router(clientes.router, prefix="/api/clientes", tags=["clientes"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )