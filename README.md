# ByteBank API - FastAPI + MySQL

API REST completa para gestión de sistema bancario construida con FastAPI, SQLAlchemy y MySQL, diseñada para ser consumida desde aplicaciones Blazor.

## Tabla de Contenidos

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

## Características

- API REST completa con operaciones CRUD
- Gestión de cuentahabientes, cuentas, sucursales y préstamos
- Sistema de movimientos bancarios (depósitos, retiros, transferencias)
- Soporte para múltiples titulares por cuenta
- Control de sobregiros autorizados y no autorizados
- Documentación automática con Swagger/OpenAPI
- Validación de datos con Pydantic
- Migraciones de base de datos con Alembic
- CORS configurado para Blazor
- Pruebas unitarias con pytest
- Arquitectura modular y escalable

## Modelo de Datos

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
ciudad → cuentahabiente
         → sucursal
         
tipodocumento → cuentahabiente
tiposucursal → sucursal
tipocuenta → cuenta
tipomovimiento → movimiento

cuentahabiente ←→ titular ←→ cuenta
                                  
                        
                        ↓         ↓         ↓
                   movimiento  prestamo  sucursal
```

## Tecnologías

- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **Base de Datos**: MySQL 8.0+
- **Validación**: Pydantic 2.5.3
- **Migraciones**: Alembic 1.13.1
- **Testing**: pytest 7.4.4
- **Servidor**: Uvicorn 0.27.0

## Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)
- Git

## Instalación

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

## Configuración

### 1. Crear base de datos MySQL

**Opción A: Ejecutar script SQL completo** (Recomendado)

Ejecuta el archivo `database/schema.sql` que contiene la estructura completa:

```bash
mysql -u root -p < database/schema.sql
```
y Ejecuta el archivo `database/database_filling.sql` que pobla la base de datos:

```bash
mysql -u root -p < database/database_filling.sql
```

O desde MySQL Workbench/DBeaver, abre y ejecuta los archivos `database/schema.sql` y `database/schema.sql`

**Opción B: Crear solo la base de datos**

```sql
DROP DATABASE IF EXISTS BancoDB;
CREATE DATABASE BancoDB;
USE BancoDB;
```

### 2. Verificar la base de datos

Antes de continuar, verifica que la base de datos esté correctamente configurada:

```bash
python verify_db.py
```

Este script verificará:
- Conexión a la base de datos
- Existencia de las 11 tablas requeridas
- Compatibilidad con los modelos SQLAlchemy
- Cantidad de registros en cada tabla

### 3. Poblar con datos de prueba (Opcional)

Si la base de datos está vacía, puedes poblarla con datos de ejemplo:

```bash
python init_db.py
```

Este script insertará:
- 5 ciudades
- 5 tipos de documento
- 4 tipos de cuenta
- 6 tipos de movimiento
- 4 tipos de sucursal
- 3 sucursales
- 3 cuentahabientes
- 3 cuentas con sus titulares

### 4. Configurar variables de entorno

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
** IMPORTANTE: Alembic es OPCIONAL en este proyecto**

#### Opción A: Sin Alembic (Recomendado para comenzar)

Si ya ejecutaste el script SQL (`database/schema.sql`), las tablas ya existen y **NO necesitas Alembic**. Los modelos SQLAlchemy funcionarán directamente con las tablas existentes.

#### Opción B: Con Alembic (Para gestión avanzada de migraciones)

Si prefieres usar Alembic para trackear cambios en la estructura de la BD:

```bash
# 1. Inicializar Alembic (solo primera vez)
alembic init alembic

# 2. Si las tablas YA EXISTEN, marca como aplicadas sin ejecutar
alembic stamp head

# 3. Para futuros cambios en la estructura
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
```

**Cuándo usar Alembic:**
- Cuando trabajas en equipo y necesitas sincronizar cambios de BD
- Cuando quieres historial de cambios en la estructura
- Cuando necesitas revertir cambios fácilmente
- NO es necesario si solo usas el script SQL y no planeas modificar la estructura

### 4. Verificar instalación

## Uso

### Scripts de utilidad

#### Verificar base de datos

Antes de iniciar la API, verifica que todo esté configurado correctamente:

```bash
python verify_db.py
```

**Salida esperada:**
```
 ByteBank - Verificación de Base de Datos
==================================================

 Verificando conexión a base de datos...
 Conexión exitosa a la base de datos

 Tablas en la base de datos:
==================================================
   ciudad               - 5 registros
   tipocuenta          - 4 registros
   tipodocumento       - 5 registros
   tipomovimiento      - 6 registros
   tiposucursal        - 4 registros
   cuentahabiente      - 3 registros
   sucursal            - 3 registros
   cuenta              - 3 registros
   titular             - 3 registros
   movimiento          - 0 registros
   prestamo            - 0 registros

 Todas las tablas existen correctamente!
```

#### Poblar base de datos

Si necesitas datos de prueba:

```bash
python init_db.py
```

## Uso

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

## Estructura del Proyecto

```
byte_bank_back/
│
├──app/                           # Aplicación principal
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── database.py                # Configuración de BD
│   │
│   ├── models/                    # Modelos SQLAlchemy (Tablas)
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
│   ├── schemas/                   # Esquemas Pydantic (Validación)
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
│   ├── routers/                   # Endpoints REST (API)
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
│   ├── crud/                      # Operaciones CRUD (Lógica de BD)
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
│   ├── schema.sql                 # Esquema completo de BD
│   └── database_filling.sql        # Poblar la Base de Datos
│
│
├── alembic/                       # Migraciones (Opcional)
│   ├── versions/                 # Versiones de migraciones
│   ├── env.py                    # Configuración de Alembic
│   ├── script.py.mako
│   └── README
│
├── venv/                          # Entorno virtual Python
│
├── .env                          # Variables de entorno (NO versionar)
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias Python
├── alembic.ini                   # Config Alembic (solo si se usa)
├── init_db.py                    # Script para poblar BD con datos de prueba
├── verify_db.py                  # Script para verificar BD existente
├── test_schemas.py               # Script para verificar Schemas existentes
└── README.md                     # Este archivo
```

## Endpoints

### Tablas Maestras (Catálogos)

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

### Cuentahabientes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/cuentahabientes` | Listar todos los cuentahabientes |
| GET | `/api/cuentahabientes/{id}` | Obtener cuentahabiente por ID |
| GET | `/api/cuentahabientes/documento/{documento}` | Buscar por documento |
| POST | `/api/cuentahabientes` | Crear nuevo cuentahabiente |
| PUT | `/api/cuentahabientes/{id}` | Actualizar cuentahabiente |
| DELETE | `/api/cuentahabientes/{id}` | Eliminar cuentahabiente |
| GET | `/api/cuentahabientes/{id}/cuentas` | Obtener cuentas del cliente |

### Sucursales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/sucursales` | Listar todas las sucursales |
| GET | `/api/sucursales/{id}` | Obtener sucursal por ID |
| GET | `/api/sucursales/ciudad/{id_ciudad}` | Sucursales por ciudad |
| POST | `/api/sucursales` | Crear nueva sucursal |
| PUT | `/api/sucursales/{id}` | Actualizar sucursal |
| DELETE | `/api/sucursales/{id}` | Eliminar sucursal |

### Cuentas

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

### Titulares

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/titulares` | Asociar titular a cuenta |
| DELETE | `/api/titulares/{id_cuenta}/{id_cuentahabiente}` | Remover titular |
| GET | `/api/titulares/cuenta/{id_cuenta}` | Titulares de una cuenta |
| GET | `/api/titulares/cuentahabiente/{id}` | Cuentas de un titular |

### Movimientos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/movimientos` | Listar todos los movimientos |
| GET | `/api/movimientos/{id}` | Obtener movimiento por ID |
| GET | `/api/movimientos/cuenta/{id_cuenta}` | Movimientos por cuenta |
| GET | `/api/movimientos/fecha/{fecha_inicio}/{fecha_fin}` | Filtrar por rango de fechas |
| POST | `/api/movimientos/deposito` | Registrar depósito |
| POST | `/api/movimientos/retiro` | Registrar retiro |
| POST | `/api/movimientos/transferencia` | Realizar transferencia |

### Préstamos

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

### Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado general de la API |
| GET | `/health` | Verificar conexión a BD |

## Pruebas

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

## Despliegue

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

## Seguridad

- No versionar el archivo `.env`
- Cambiar `SECRET_KEY` en producción
- Usar HTTPS en producción
- Configurar CORS específicamente (no usar `allow_origins=["*"]`)
- Implementar rate limiting
- Validar y sanitizar todas las entradas
- Implementar autenticación JWT para endpoints sensibles

## Variables de Entorno

| Variable | Descripción | Default | Requerido |
|----------|-------------|---------|-----------|
| `DB_HOST` | Host de MySQL | localhost | Si |
| `DB_PORT` | Puerto de MySQL | 3306 | Si |
| `DB_USER` | Usuario de BD | root | Si |
| `DB_PASSWORD` | Contraseña de BD | - | Si |
| `DB_NAME` | Nombre de la BD | bancodb | Si |
| `API_HOST` | Host donde corre la API | 0.0.0.0 | No |
| `API_PORT` | Puerto de la API | 8000 | No |
| `DEBUG` | Modo desarrollo (logs detallados) | True | No |
| `SECRET_KEY` | Clave para encriptación JWT | - | Si |
| `ALGORITHM` | Algoritmo de encriptación | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración de tokens | 30 | No |

## Preguntas Frecuentes (FAQ)

### ¿Necesito usar Alembic?

**No es obligatorio**. Alembic es útil para:
- Gestionar cambios en la estructura de BD en equipo
- Mantener historial de migraciones
- Revertir cambios fácilmente

Si ya tienes la BD creada con el script SQL, puedes trabajar directamente sin Alembic.

### ¿Cómo verifico que todo funciona?

```bash
# 1. Verificar base de datos
python verify_db.py

# 2. Iniciar API
uvicorn app.main:app --reload

# 3. Visitar http://localhost:8000/docs
```

### ¿Qué hago si la BD ya tiene datos?

Si tu base de datos ya está poblada:
1. **NO ejecutes** `init_db.py` (sobrescribirá datos)
2. **Ejecuta** `verify_db.py` para verificar compatibilidad
3. Inicia la API directamente con `uvicorn`

### ¿Cómo agrego datos de prueba?

```bash
# Solo si la BD está vacía
python init_db.py
```

### ¿Dónde están los endpoints?

Visita la documentación interactiva en:
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Error: "No module named 'app'"

Asegúrate de:
1. Estar en la raíz del proyecto (donde está la carpeta `app/`)
2. Tener el entorno virtual activado
3. Haber instalado las dependencias: `pip install -r requirements.txt`

### Error de conexión a MySQL

Verifica en `.env`:
1. Credenciales correctas (usuario, password)
2. MySQL está corriendo
3. La base de datos `BancoDB` existe

```bash
# Verificar conexión
python verify_db.py
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autores

- **Cristian Arboleda** - *Desarrollo inicial* - [cristiancalderon82192-hue](https://github.com/cristiancalderon82192-hue)

## Agradecimientos

- FastAPI Documentation
- SQLAlchemy Documentation
- Comunidad de Python
