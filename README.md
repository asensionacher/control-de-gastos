# Control de Gastos 💰

> Sistema completo de gestión financiera personal con soporte multi-banco para España

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.2-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com/)

Aplicación web moderna para el control financiero doméstico con importación automática de extractos bancarios, categorización inteligente, y análisis visual de gastos e ingresos.

## ✨ Características Principales

### � Importación Multi-Banco
- ✅ **Kutxabank** (Cuenta corriente y Tarjeta)
- ✅ **Openbank**
- ✅ **Imaginbank**
- 🔄 **Detección automática** de formato y banco
- 📁 Soporte para **CSV, XLS, XLSX, HTML**
- 🚫 **Detección de duplicados** automática

### 🏷️ Categorización Inteligente
- 🤖 **Auto-categorización** basada en aprendizaje
- 📋 **Categorías y subcategorías** personalizables
- ⚡ **Categorización masiva** con selección múltiple
- 🔄 **Aplicar a similares** - Categoriza transacciones iguales de una vez
- 📝 11 categorías predefinidas listas para usar

### � Análisis y Reportes
- 📈 **Gráficos interactivos** (evolución, distribución, comparativas)
- 📅 **Reportes mensuales** con ingresos/gastos/balance
- � **Top gastos** y estadísticas detalladas
- 🔍 **Filtros avanzados** por fecha, banco, categoría, tipo, descripción
- 📄 **Paginación** inteligente (100 transacciones por página)

### 🎨 Interfaz Moderna
- 🌙 **Modo oscuro** elegante y permanente
- 📱 **Responsive** - Funciona en móvil, tablet y escritorio
- 🇪🇸 **Completamente en español**
- ⚡ **Operaciones sin scroll** - La interfaz se mantiene estable
- 🎯 **UX optimizada** para rapidez y eficiencia

## 🚀 Inicio Rápido

### Prerequisitos
- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)
- O bien: Python 3.11+ y Node.js 16+

### Instalación con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/asensionacher/control-de-gastos.git
cd control-gastos

# 2. Crear directorio de datos
mkdir -p data

# 3. Iniciar la aplicación
docker-compose up -d

# 4. Acceder a la aplicación
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Documentación API: http://localhost:8000/docs
```

### Instalación Manual

```bash
# Backend
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python -c "from database import create_tables; create_tables()"

# Iniciar servidor
uvicorn main:app --reload --port 8000
```

```bash
# Frontend (nueva terminal)
cd frontend

# Instalar dependencias
npm install

# Iniciar aplicación
npm start
```

**Acceso:**
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

> 💡 **Nota**: Para desarrollo, consulta la sección [🛠️ Desarrollo](#%EF%B8%8F-desarrollo) más abajo.

## 📖 Uso

### 1️⃣ Importar Extractos Bancarios

1. Descarga el extracto de tu banco en formato CSV/XLS
2. Ve a **"Subir Archivo"** en la aplicación
3. Selecciona el archivo (la detección automática identificará el banco)
4. Revisa el resumen de importación

### 2️⃣ Categorizar Transacciones

**Categorización Individual:**
- Usa el dropdown en cada transacción
- El sistema pregunta si quieres aplicar a todas las similares

**Categorización Masiva:**
- Selecciona múltiples transacciones con los checkboxes
- Usa la barra de acciones para categorizar todas a la vez

### 3️⃣ Analizar Gastos

- **Dashboard**: Vista rápida de estadísticas generales
- **Reportes**: Gráficos de evolución y distribución
- **Transacciones**: Búsqueda y filtrado avanzado

## 🏗️ Arquitectura

```
┌─────────────────┐
│   React App     │  Puerto 3000
│   (Frontend)    │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   FastAPI       │  Puerto 8000
│   (Backend)     │
└────────┬────────┘
         │ SQLAlchemy
         │
┌────────▼────────┐
│   SQLite DB     │  ./data/
│  (Persistente)  │
└─────────────────┘
```

### Stack Tecnológico

**Backend:**
- FastAPI 0.104 - Framework web moderno
- SQLAlchemy 2.0 - ORM
- Pandas 2.1 - Procesamiento de datos
- Pydantic 2.5 - Validación

**Frontend:**
- React 18.2 - UI Library
- Chart.js 4.4 - Gráficos
- Axios 1.6 - Cliente HTTP
- React Router 6.20 - Navegación

**Infraestructura:**
- Docker & Docker Compose
- SQLite (LiteDB)

## 📁 Estructura del Proyecto

```
control-gastos/
├── backend/                 # API FastAPI
│   ├── routes/             # Endpoints REST
│   │   ├── transactions.py # CRUD transacciones + filtros
│   │   ├── categories.py   # Gestión categorías
│   │   ├── upload.py       # Importación archivos
│   │   └── reports.py      # Estadísticas y reportes
│   ├── parsers.py          # Parsers por banco
│   ├── bank_detector.py    # Detección automática
│   ├── models.py           # Modelos SQLAlchemy
│   ├── schemas.py          # Schemas Pydantic
│   ├── database.py         # Configuración DB
│   └── main.py             # Aplicación principal
│
├── frontend/               # Aplicación React
│   └── src/
│       ├── pages/          # Vistas principales
│       │   ├── Dashboard.js
│       │   ├── Transactions.js
│       │   ├── Upload.js
│       │   ├── Categories.js
│       │   └── Reports.js
│       └── services/
│           └── api.js      # Cliente API
│
├── data/                   # Base de datos (volumen Docker)
├── examples/               # Archivos de ejemplo
├── docker-compose.yml      # Configuración Docker
└── README.md
```

## 🗄️ Modelo de Datos

```
categories
├── id
├── name
└── created_at

subcategories
├── id
├── name
├── category_id → categories
└── created_at

transactions
├── id
├── bank_type
├── date (indexed)
├── description
├── amount
├── balance
├── category_id → categories
├── subcategory_id → subcategories
├── transaction_hash (UNIQUE, indexed)
├── created_at
└── updated_at

store_mappings (auto-categorización)
├── id
├── store_name (UNIQUE, indexed)
├── category_id → categories
├── subcategory_id → subcategories
└── updated_at
```

## 🔌 API Reference

Documentación interactiva completa en: `http://localhost:8000/docs`

### Principales Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/transactions/` | Lista transacciones (con filtros) |
| `PUT` | `/api/transactions/{id}` | Actualiza transacción |
| `POST` | `/api/transactions/bulk-categorize` | Categorización masiva |
| `POST` | `/api/transactions/bulk-delete` | Eliminación masiva |
| `GET` | `/api/categories/` | Lista categorías |
| `POST` | `/api/upload/` | Importar archivo |
| `POST` | `/api/upload/detect-bank` | Detectar banco del archivo |
| `GET` | `/api/reports/summary` | Resumen completo |

## 🛠️ Desarrollo

### Setup Local (sin Docker)

**Backend:**
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor de desarrollo
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

### Variables de Entorno

**Backend** (opcional):
```bash
DATABASE_PATH=./data/control_gastos.db
```

**Frontend** (`.env`):
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Añadir un Nuevo Banco

1. **Crear parser** en `backend/parsers.py`:
```python
class NuevoBancoParser(BaseParser):
    def parse(self, file_content: bytes) -> List[dict]:
        # Implementar lógica de parseo
        pass
```

2. **Añadir detección** en `backend/bank_detector.py`:
```python
def detect_bank_type(file_content: bytes) -> str:
    # Añadir lógica de detección
    if "patron_nuevo_banco" in content:
        return "nuevo_banco"
```

3. **Actualizar frontend** en `frontend/src/pages/Upload.js`:
```javascript
// Añadir opción en el select
<option value="nuevo_banco">Nuevo Banco</option>
```

### Ejecutar Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork** el proyecto
2. Crea una **rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

### Guías de Contribución

- **Código**: Sigue PEP 8 (Python) y ESLint (JavaScript)
- **Commits**: Mensajes claros y descriptivos en español
- **Tests**: Añade tests para nuevas funcionalidades
- **Documentación**: Actualiza README si es necesario

### Ideas para Contribuir

- 🏦 Añadir soporte para más bancos españoles
- 📊 Nuevos tipos de reportes y gráficos
- 🎯 Sistema de presupuestos y metas
- 📄 Exportación a PDF/Excel


## 🐛 Reportar Bugs

Si encuentras un bug, por favor [abre un issue](https://github.com/asensionacher/control-de-gastos/issues) con:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots si aplica
- Tu entorno (OS, versión de Docker, etc.)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- React por la librería UI
- Chart.js por los gráficos
- La comunidad open source

## 🤖 Desarrollo con IA

Este proyecto ha sido completamente desarrollado utilizando **Claude Sonnet 4.5** de Anthropic. Todo el código, arquitectura, documentación y funcionalidades han sido generadas mediante prompts conversacionales, demostrando las capacidades de la IA en el desarrollo de software moderno.

## 📧 Contacto

- **Proyecto**: [GitHub Repository](https://github.com/asensionacher/control-de-gastos)
- **Issues**: [Bug Reports](https://github.com/asensionacher/control-de-gastos/issues)

---

**Desarrollado con ❤️ para mejorar el control financiero personal**  
**Powered by Claude Sonnet 4.5** 🤖
