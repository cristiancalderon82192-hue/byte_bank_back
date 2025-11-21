from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import pytest

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_crud_tipo_cuenta():
    # Create
    response = client.post("/tipos/cuenta", json={"TipoCuenta": "Ahorros Test", "Sobregiro": 100.0})
    assert response.status_code == 201
    data = response.json()
    assert data["TipoCuenta"] == "Ahorros Test"
    id_cuenta = data["IdTipoCuenta"]

    # Read List
    response = client.get("/tipos/cuenta")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Read One
    response = client.get(f"/tipos/cuenta/{id_cuenta}")
    assert response.status_code == 200
    assert response.json()["IdTipoCuenta"] == id_cuenta

    # Update
    response = client.put(f"/tipos/cuenta/{id_cuenta}", json={"TipoCuenta": "Ahorros Updated"})
    assert response.status_code == 200
    assert response.json()["TipoCuenta"] == "Ahorros Updated"

    # Delete
    response = client.delete(f"/tipos/cuenta/{id_cuenta}")
    assert response.status_code == 204
    
    # Verify Delete
    response = client.get(f"/tipos/cuenta/{id_cuenta}")
    assert response.status_code == 404

def test_crud_tipo_documento():
    # Create
    response = client.post("/tipos/documento", json={"TipoDocumento": "Cedula Test", "Sigla": "CT"})
    assert response.status_code == 201
    data = response.json()
    assert data["TipoDocumento"] == "Cedula Test"
    id_doc = data["IdTipoDocumento"]

    # Read List
    response = client.get("/tipos/documento")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Read One
    response = client.get(f"/tipos/documento/{id_doc}")
    assert response.status_code == 200
    assert response.json()["IdTipoDocumento"] == id_doc

    # Update
    response = client.put(f"/tipos/documento/{id_doc}", json={"TipoDocumento": "Cedula Updated"})
    assert response.status_code == 200
    assert response.json()["TipoDocumento"] == "Cedula Updated"

    # Delete
    response = client.delete(f"/tipos/documento/{id_doc}")
    assert response.status_code == 204

    # Verify Delete
    response = client.get(f"/tipos/documento/{id_doc}")
    assert response.status_code == 404

def test_crud_tipo_movimiento():
    # Create
    response = client.post("/tipos/movimiento", json={"TipoMovimiento": "Retiro Test"})
    assert response.status_code == 201
    data = response.json()
    assert data["TipoMovimiento"] == "Retiro Test"
    id_mov = data["IdTipoMovimiento"]

    # Read List
    response = client.get("/tipos/movimiento")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Read One
    response = client.get(f"/tipos/movimiento/{id_mov}")
    assert response.status_code == 200
    assert response.json()["IdTipoMovimiento"] == id_mov

    # Update
    response = client.put(f"/tipos/movimiento/{id_mov}", json={"TipoMovimiento": "Retiro Updated"})
    assert response.status_code == 200
    assert response.json()["TipoMovimiento"] == "Retiro Updated"

    # Delete
    response = client.delete(f"/tipos/movimiento/{id_mov}")
    assert response.status_code == 204

    # Verify Delete
    response = client.get(f"/tipos/movimiento/{id_mov}")
    assert response.status_code == 404

def test_crud_tipo_sucursal():
    # Create
    response = client.post("/tipos/sucursal", json={"TipoSucursal": "Norte Test"})
    assert response.status_code == 201
    data = response.json()
    assert data["TipoSucursal"] == "Norte Test"
    id_suc = data["IdTipoSucursal"]

    # Read List
    response = client.get("/tipos/sucursal")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Read One
    response = client.get(f"/tipos/sucursal/{id_suc}")
    assert response.status_code == 200
    assert response.json()["IdTipoSucursal"] == id_suc

    # Update
    response = client.put(f"/tipos/sucursal/{id_suc}", json={"TipoSucursal": "Norte Updated"})
    assert response.status_code == 200
    assert response.json()["TipoSucursal"] == "Norte Updated"

    # Delete
    response = client.delete(f"/tipos/sucursal/{id_suc}")
    assert response.status_code == 204

    # Verify Delete
    response = client.get(f"/tipos/sucursal/{id_suc}")
    assert response.status_code == 404
