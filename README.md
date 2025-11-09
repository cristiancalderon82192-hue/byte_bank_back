# 🏦 ByteBank API - FastAPI + MySQL

API REST completa para gestión de sistema bancario construida con FastAPI, SQLAlchemy y MySQL, diseñada para ser consumida desde aplicaciones Blazor.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Modelo de Datos](#modelo-de-datos)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)

## ✨ Características

- ✅ API REST completa con operaciones CRUD
- ✅ Gestión de cuentahabientes, cuentas, sucursales y préstamos
- ✅ Sistema de movimientos bancarios (depósitos, retiros, transferencias)
- ✅ Soporte para múltiples titulares por cuenta
- ✅ Control de sobregiros autorizados y no autorizados
- ✅ Documentación automática con Swagger/OpenAPI
- ✅ Validación de datos con Pydantic
- ✅ Migraciones de base de datos con Alembic
- ✅ CORS configurado para Blazor
- ✅ Pruebas unitarias con pytest
- ✅ Arquitectura modular y escalable

## 🗄️ Modelo de Datos

### Tablas Maestras (Catálogos)
- **tipocuenta**: Tipos de cuenta (Ahorro, Corriente, etc.)
- **tipodocumento**: Tipos de documento de identidad
- **tipomovimiento**: Tipos de movimientos bancarios
- **tiposucursal**: Tipos de sucursales
- **ciudad**: Catálogo de ciudades

### Tablas Principales
- **cuentahabiente**: Información de clientes
- **sucursal**: Sucursales bancarias
- **cuenta**: Cuentas bancarias
- **titular**: Relación muchos a muchos entre cuentas y cuentahabientes
- **movimiento**: Transacciones bancarias
- **prestamo**: Préstamos asociados a cuentas

### Diagrama de Relaciones

```
ciudad ──┬─→ cuentahabiente
         └─→ sucursal
         
tipodocumento ─→ cuentahabiente
tiposucursal ─→ sucursal
tipocuenta ─→ cuenta
tipomovimiento ─→ movimiento

cuentahabiente ←─→ titular ←─→ cuenta
                                  │
                        ┌─────────┼─────────┐
                        ↓         ↓         ↓
                   movimiento  prestamo  sucursal
```

## 🛠️ Tecnologías

- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **Base de Datos**: MySQL 8.0+
- **Validación**: Pydantic 2.5.3
- **Migraciones**: Alembic 1.13.1
- **Testing**: pytest 7.4.4
- **Servidor**: Uvicorn 0.27.0

## 📦 Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)
- Git

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/cristiancalderon82192-hue/byte_bank_back.git
cd byte_bank_back
```

### 2. Crear entorno virtual

**Windows (PowerShell/CMD):**
```bash
python -m venv venv

# PowerShell
venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Crear base de datos MySQL

```sql
DROP DATABASE IF EXISTS BancoDB;
CREATE DATABASE BancoDB;
USE BancoDB;
```

O ejecutar el script completo proporcionado en `database/schema.sql`

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=BancoDB

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Seguridad
SECRET_KEY=tu_clave_secreta_aqui_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Ejecutar migraciones

```bash
# Inicializar Alembic (solo primera vez)
alembic init alembic

# Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

## 🎯 Uso

### Iniciar el servidor de desarrollo

```bash
# Opción 1: Con uvicorn
uvicorn app.main:app --reload

# Opción 2: Ejecutar directamente
python -m app.main
```

El servidor estará disponible en: `http://localhost:8000`

### Acceder a la documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📁 Estructura del Proyecto

```
byte_bank_back/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── database.py                # Configuración de BD
│   │
│   ├── models/                    # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── ciudad.py
│   │   ├── tipo_cuenta.py
│   │   ├── tipo_documento.py
│   │   ├── tipo_movimiento.py
│   │   ├── tipo_sucursal.py
│   │   ├── cuentahabiente.py
│   │   ├── sucursal.py
│   │   ├── cuenta.py
│   │   ├── titular.py
│   │   ├── movimiento.py
│   │   └── prestamo.py
│   │
│   ├── schemas/                   # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── ciudad.py
│   │   ├── tipo_cuenta.py
│   │   ├── tipo_documento.py
│   │   ├── tipo_movimiento.py
│   │   ├── tipo_sucursal.py
│   │   ├── cuentahabiente.py
│   │   ├── sucursal.py
│   │   ├── cuenta.py
│   │   ├── titular.py
│   │   ├── movimiento.py
│   │   └── prestamo.py
│   │
│   ├── routers/                   # Endpoints REST
│   │   ├── __init__.py
│   │   ├── ciudades.py
│   │   ├── tipos.py              # Endpoints para tablas maestras
│   │   ├── cuentahabientes.py
│   │   ├── sucursales.py
│   │   ├── cuentas.py
│   │   ├── titulares.py
│   │   ├── movimientos.py
│   │   └── prestamos.py
│   │
│   ├── crud/                      # Operaciones CRUD
│   │   ├── __init__.py
│   │   ├── ciudad.py
│   │   ├── tipo_cuenta.py
│   │   ├── cuentahabiente.py
│   │   ├── sucursal.py
│   │   ├── cuenta.py
│   │   ├── movimiento.py
│   │   └── prestamo.py
│   │
│   └── utils/                     # Utilidades
│       ├── __init__.py
│       └── security.py
│
├── tests/                         # Pruebas unitarias
│   ├── __init__.py
│   ├── test_cuentahabientes.py
│   ├── test_cuentas.py
│   ├── test_movimientos.py
│   └── test_prestamos.py
│
├── database/                      # Scripts SQL
│   └── schema.sql                # Esquema de BD
│
├── alembic/                       # Migraciones
│   ├── versions/
│   └── env.py
│
├── .env                          # Variables de entorno
├── .gitignore
├── requirements.txt
├── alembic.ini
└── README.md
```

## 🔌 Endpoints

### 📊 Tablas Maestras (Catálogos)

#### Ciudades
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/ciudades` | Listar todas las ciudades |
| GET | `/api/ciudades/{id}` | Obtener ciudad por ID |
| POST | `/api/ciudades` | Crear nueva ciudad |
| PUT | `/api/ciudades/{id}` | Actualizar ciudad |
| DELETE | `/api/ciudades/{id}` | Eliminar ciudad |

#### Tipos de Cuenta
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tipos-cuenta` | Listar tipos de cuenta |
| GET | `/api/tipos-cuenta/{id}` | Obtener tipo por ID |
| POST | `/api/tipos-cuenta` | Crear tipo de cuenta |
| PUT | `/api/tipos-cuenta/{id}` | Actualizar tipo |
| DELETE | `/api/tipos-cuenta/{id}` | Eliminar tipo |

#### Tipos de Documento
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tipos-documento` | Listar tipos de documento |
| GET | `/api/tipos-documento/{id}` | Obtener tipo por ID |
| POST | `/api/tipos-documento` | Crear tipo de documento |
| PUT | `/api/tipos-documento/{id}` | Actualizar tipo |
| DELETE | `/api/tipos-documento/{id}` | Eliminar tipo |

#### Tipos de Movimiento
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tipos-movimiento` | Listar tipos de movimiento |
| GET | `/api/tipos-movimiento/{id}` | Obtener tipo por ID |
| POST | `/api/tipos-movimiento` | Crear tipo de movimiento |
| PUT | `/api/tipos-movimiento/{id}` | Actualizar tipo |
| DELETE | `/api/tipos-movimiento/{id}` | Eliminar tipo |

#### Tipos de Sucursal
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tipos-sucursal` | Listar tipos de sucursal |
| GET | `/api/tipos-sucursal/{id}` | Obtener tipo por ID |
| POST | `/api/tipos-sucursal` | Crear tipo de sucursal |
| PUT | `/api/tipos-sucursal/{id}` | Actualizar tipo |
| DELETE | `/api/tipos-sucursal/{id}` | Eliminar tipo |

### 👥 Cuentahabientes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/cuentahabientes` | Listar todos los cuentahabientes |
| GET | `/api/cuentahabientes/{id}` | Obtener cuentahabiente por ID |
| GET | `/api/cuentahabientes/documento/{documento}` | Buscar por documento |
| POST | `/api/cuentahabientes` | Crear nuevo cuentahabiente |
| PUT | `/api/cuentahabientes/{id}` | Actualizar cuentahabiente |
| DELETE | `/api/cuentahabientes/{id}` | Eliminar cuentahabiente |
| GET | `/api/cuentahabientes/{id}/cuentas` | Obtener cuentas del cliente |

### 🏢 Sucursales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/sucursales` | Listar todas las sucursales |
| GET | `/api/sucursales/{id}` | Obtener sucursal por ID |
| GET | `/api/sucursales/ciudad/{id_ciudad}` | Sucursales por ciudad |
| POST | `/api/sucursales` | Crear nueva sucursal |
| PUT | `/api/sucursales/{id}` | Actualizar sucursal |
| DELETE | `/api/sucursales/{id}` | Eliminar sucursal |

### 💳 Cuentas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/cuentas` | Listar todas las cuentas |
| GET | `/api/cuentas/{id}` | Obtener cuenta por ID |
| GET | `/api/cuentas/numero/{numero}` | Buscar por número de cuenta |
| POST | `/api/cuentas` | Crear nueva cuenta |
| PUT | `/api/cuentas/{id}` | Actualizar cuenta |
| DELETE | `/api/cuentas/{id}` | Eliminar cuenta |
| GET | `/api/cuentas/{id}/titulares` | Obtener titulares de la cuenta |
| GET | `/api/cuentas/{id}/movimientos` | Obtener movimientos de la cuenta |
| GET | `/api/cuentas/{id}/saldo` | Consultar saldo actual |

### 🤝 Titulares

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/titulares` | Asociar titular a cuenta |
| DELETE | `/api/titulares/{id_cuenta}/{id_cuentahabiente}` | Remover titular |
| GET | `/api/titulares/cuenta/{id_cuenta}` | Titulares de una cuenta |
| GET | `/api/titulares/cuentahabiente/{id}` | Cuentas de un titular |

### 💸 Movimientos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/movimientos` | Listar todos los movimientos |
| GET | `/api/movimientos/{id}` | Obtener movimiento por ID |
| GET | `/api/movimientos/cuenta/{id_cuenta}` | Movimientos por cuenta |
| GET | `/api/movimientos/fecha/{fecha_inicio}/{fecha_fin}` | Filtrar por rango de fechas |
| POST | `/api/movimientos/deposito` | Registrar depósito |
| POST | `/api/movimientos/retiro` | Registrar retiro |
| POST | `/api/movimientos/transferencia` | Realizar transferencia |

### 💰 Préstamos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/prestamos` | Listar todos los préstamos |
| GET | `/api/prestamos/{id}` | Obtener préstamo por ID |
| GET | `/api/prestamos/cuenta/{id_cuenta}` | Préstamos por cuenta |
| GET | `/api/prestamos/numero/{numero}` | Buscar por número de préstamo |
| POST | `/api/prestamos` | Crear nuevo préstamo |
| PUT | `/api/prestamos/{id}` | Actualizar préstamo |
| DELETE | `/api/prestamos/{id}` | Eliminar préstamo |
| GET | `/api/prestamos/{id}/cuotas` | Calcular plan de cuotas |

### 🔍 Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado general de la API |
| GET | `/health` | Verificar conexión a BD |

## 🧪 Pruebas

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar con cobertura

```bash
pytest --cov=app tests/
```

### Ejecutar pruebas específicas

```bash
# Pruebas de cuentahabientes
pytest tests/test_cuentahabientes.py

# Pruebas de movimientos
pytest tests/test_movimientos.py -v
```

## 🚢 Despliegue

### Docker

```bash
# Construir imagen
docker build -t bytebank-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 --env-file .env bytebank-api
```

### Docker Compose

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Servicios Cloud

La API puede desplegarse en:
- **Render**: https://render.com (Recomendado - Free tier)
- **Railway**: https://railway.app
- **AWS EC2**: Amazon Web Services
- **Azure App Service**: Microsoft Azure
- **Google Cloud Run**: Google Cloud Platform

## 🔐 Seguridad

- ❌ No versionar el archivo `.env`
- 🔑 Cambiar `SECRET_KEY` en producción
- 🔒 Usar HTTPS en producción
- 🌐 Configurar CORS específicamente (no usar `allow_origins=["*"]`)
- ⏱️ Implementar rate limiting
- ✅ Validar y sanitizar todas las entradas
- 🛡️ Implementar autenticación JWT para endpoints sensibles

## 📝 Variables de Entorno

| Variable | Descripción | Default | Requerido |
|----------|-------------|---------|-----------|
| `DB_HOST` | Host de MySQL | localhost | ✅ |
| `DB_PORT` | Puerto de MySQL | 3306 | ✅ |
| `DB_USER` | Usuario de BD | root | ✅ |
| `DB_PASSWORD` | Contraseña de BD | - | ✅ |
| `DB_NAME` | Nombre de la BD | BancoDB | ✅ |
| `API_HOST` | Host de la API | 0.0.0.0 | ❌ |
| `API_PORT` | Puerto de la API | 8000 | ❌ |
| `DEBUG` | Modo debug | True | ❌ |
| `SECRET_KEY` | Clave para JWT | - | ✅ |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Cristian Arboleda** - *Desarrollo inicial* - [cristiancalderon82192-hue](https://github.com/cristiancalderon82192-hue)

## 📞 Contacto

- Email: tu-email@ejemplo.com
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- FastAPI Documentation
- SQLAlchemy Documentation
- Comunidad de Python

---

⭐️ Si este proyecto te fue útil, dale una estrella en GitHub!