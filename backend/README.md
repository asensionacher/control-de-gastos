# Backend - Control de Gastos API 🔌

Backend REST API construido con FastAPI para la gestión de transacciones financieras, categorización inteligente y generación de reportes.

## 🎯 Características

- ⚡ **FastAPI** - Framework moderno y de alto rendimiento
- 🗄️ **SQLAlchemy ORM** - Manejo robusto de base de datos
- 📊 **Pandas** - Procesamiento eficiente de archivos bancarios
- 🔍 **Detección automática** de banco y formato
- 🚫 **Prevención de duplicados** con hash SHA-256
- 🤖 **Auto-categorización** basada en aprendizaje
- 📝 **Documentación interactiva** con Swagger UI

## 📋 Requisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecutar

### Modo Desarrollo
```bash
uvicorn main:app --reload --port 8000
```

### Modo Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estructura

```
backend/
├── routes/                  # Endpoints de la API
│   ├── __init__.py
│   ├── transactions.py      # CRUD y filtrado de transacciones
│   ├── categories.py        # Gestión de categorías
│   ├── upload.py            # Importación de archivos
│   └── reports.py           # Generación de reportes
│
├── parsers.py               # Parsers específicos por banco
├── bank_detector.py         # Detección automática de banco
├── models.py                # Modelos SQLAlchemy
├── schemas.py               # Schemas Pydantic
├── database.py              # Configuración de base de datos
├── main.py                  # Aplicación FastAPI principal
├── requirements.txt         # Dependencias
└── Dockerfile              # Imagen Docker
```

## 🗄️ Modelos de Datos

### Category
Categorías principales para clasificar transacciones.
```python
- id: int (PK)
- name: str (UNIQUE)
- created_at: datetime
```

### Subcategory
Subcategorías para clasificación más detallada.
```python
- id: int (PK)
- name: str
- category_id: int (FK → Category)
- created_at: datetime
```

### Transaction
Transacciones bancarias importadas.
```python
- id: int (PK)
- bank_type: str (kutxabank_account, kutxabank_card, openbank, imaginbank, bbva, ing)
- date: datetime (indexed)
- description: str
- amount: float
- balance: float (nullable)
- reference: str (nullable)
- extra_info: str (nullable)
- category_id: int (FK → Category, nullable)
- subcategory_id: int (FK → Subcategory, nullable)
- transaction_hash: str (UNIQUE, indexed)
- created_at: datetime
- updated_at: datetime
```

### StoreMapping
Mapeo de establecimientos a categorías para auto-categorización.
```python
- id: int (PK)
- store_name: str (UNIQUE, indexed)
- category_id: int (FK → Category, nullable)
- subcategory_id: int (FK → Subcategory, nullable)
- created_at: datetime
- updated_at: datetime
```

## 🔌 API Endpoints

### Transacciones

#### `GET /api/transactions/`
Lista transacciones con filtros opcionales.

**Query Parameters:**
- `skip`: Offset para paginación (default: 0)
- `limit`: Límite de resultados (default: 100)
- `bank_type`: Filtrar por banco
- `category_id`: Filtrar por categoría (usar "null" para sin categoría)
- `transaction_type`: "expense" o "income"
- `description`: Búsqueda por descripción (mín. 3 caracteres)
- `start_date`: Fecha inicio (ISO format)
- `end_date`: Fecha fin (ISO format)

**Response:** `List[Transaction]`

#### `GET /api/transactions/{id}`
Obtiene una transacción específica.

**Response:** `Transaction`

#### `PUT /api/transactions/{id}`
Actualiza una transacción.

**Body:**
```json
{
  "category_id": 1,
  "subcategory_id": 2,
  "apply_to_all": false
}
```

**Response:** `Transaction`

#### `DELETE /api/transactions/{id}`
Elimina una transacción.

**Response:** `{"message": "Transacción eliminada correctamente"}`

#### `POST /api/transactions/bulk-categorize`
Categoriza múltiples transacciones.

**Body:**
```json
{
  "transaction_ids": [1, 2, 3],
  "category_id": 1,
  "subcategory_id": 2
}
```

**Response:** `{"message": "...", "updated_count": 3}`

#### `POST /api/transactions/bulk-delete`
Elimina múltiples transacciones.

**Body:** `[1, 2, 3]`

**Response:** `{"message": "...", "deleted_count": 3}`

### Categorías

#### `GET /api/categories/`
Lista todas las categorías con sus subcategorías.

**Response:** `List[CategoryWithSubcategories]`

#### `POST /api/categories/`
Crea una nueva categoría.

**Body:**
```json
{
  "name": "Nueva Categoría"
}
```

#### `POST /api/categories/init-default`
Inicializa las categorías predeterminadas.

**Response:** Lista de categorías creadas

### Upload

#### `POST /api/upload/`
Importa archivo bancario (CSV, XLS, HTML).

**Form Data:**
- `file`: Archivo a importar
- `bank_type`: (Opcional) Tipo de banco, se detecta automáticamente si no se proporciona

**Response:**
```json
{
  "success": true,
  "total_rows": 50,
  "imported": 45,
  "duplicates": 5,
  "errors": 0,
  "message": "..."
}
```

#### `POST /api/upload/detect-bank`
Detecta el tipo de banco de un archivo.

**Form Data:**
- `file`: Archivo a analizar

**Response:**
```json
{
  "bank_type": "kutxabank_account",
  "confidence": "high"
}
```

#### `GET /api/upload/bank-types`
Lista tipos de banco soportados.

**Response:** `List[str]`

### Reportes

#### `GET /api/reports/summary`
Resumen completo de reportes.

**Query Parameters:**
- `months`: Número de meses (default: 6)

**Response:**
```json
{
  "monthly_reports": [...],
  "category_reports": [...],
  "top_expenses": [...]
}
```

#### `GET /api/reports/monthly`
Reporte mensual de ingresos/gastos.

**Response:** `List[MonthlyReport]`

#### `GET /api/reports/by-category`
Distribución por categorías.

**Response:** `List[CategoryReport]`

#### `GET /api/reports/top-expenses`
Top 10 mayores gastos.

**Response:** `List[Transaction]`

#### `GET /api/reports/stats`
Estadísticas generales.

**Response:**
```json
{
  "total_transactions": 1234,
  "total_income": 50000.00,
  "total_expenses": -30000.00,
  "balance": 20000.00,
  "uncategorized": 15
}
```

## 🏦 Parsers de Bancos

### Estructura Base
Todos los parsers heredan de `BaseParser`:
- Detección automática de encoding
- Generación de hash para duplicados
- Manejo de errores robusto

### Bancos Soportados

#### Kutxabank - Cuenta
- **Formato**: XLS binario (xlrd engine)
- **Columnas**: Fecha, Concepto, Fecha Valor, Importe, Saldo
- **Particularidades**: 
  - Header dinámico (busca "Fecha" en las primeras 20 filas)
  - Omite filas de metadatos

#### Kutxabank - Tarjeta
- **Formato**: XLS binario
- **Columnas**: Similar a cuenta
- **Particularidades**: Mismo manejo que cuenta

#### Openbank
- **Formato**: HTML disfrazado de XLS
- **Columnas**: Fecha Operación, Fecha Valor, Concepto, Importe, Saldo
- **Particularidades**: 
  - Parseo de tabla HTML con lxml
  - Fallback a CSV si falla HTML

#### Imaginbank
- **Formato**: CSV
- **Columnas**: Concepto, Fecha, Importe, Saldo
- **Particularidades**: 
  - Sufijo "EUR" en importes (ej: "-217,98EUR")
  - Separador: punto y coma
  - Decimal: coma

#### BBVA
- **Formato**: XLSX (Excel moderno)
- **Columnas**: F.Valor, Fecha, Concepto, Movimiento, Importe, Divisa, Disponible, Observaciones
- **Particularidades**:
  - Header dinámico (busca "F.Valor" en las primeras filas)
  - Combina "Concepto" y "Movimiento" en la descripción
  - Incluye observaciones en extra_info
  - Soporta múltiples formatos de fecha

#### ING Direct
- **Formato**: XLS (Excel 97-2003)
- **Columnas**: F. VALOR, CATEGORÍA, SUBCATEGORÍA, DESCRIPCIÓN, COMENTARIO, IMAGEN, IMPORTE (€), SALDO (€)
- **Particularidades**:
  - Header dinámico (busca "F. VALOR" en las primeras filas)
  - Combina categoría, subcategoría y descripción
  - Incluye comentarios en extra_info
  - Categorías propias de ING ("Ventajas ING", "Movimientos excluidos", etc.)

### Añadir un Nuevo Banco

1. **Crear clase parser** en `parsers.py`:

```python
class NuevoBancoParser(BaseParser):
    def parse(self, file_content: bytes) -> List[dict]:
        # Detectar encoding
        encoding = self.detect_encoding(file_content)
        
        # Leer contenido
        content = file_content.decode(encoding)
        
        # Parsear según formato
        # ...
        
        # Retornar lista de dicts con:
        # - date (datetime)
        # - description (str)
        # - amount (float)
        # - balance (float, opcional)
        # - reference (str, opcional)
        
        return transactions
```

2. **Añadir detección** en `bank_detector.py`:

```python
def detect_bank_type(file_content: bytes, filename: str = "") -> Optional[str]:
    # ... código existente ...
    
    # Añadir tu detección
    if "patron_especifico_banco" in content_str:
        return "nuevo_banco"
```

3. **Actualizar** `routes/upload.py`:

```python
# Añadir en get_parser()
bank_parsers = {
    # ... existentes ...
    "nuevo_banco": NuevoBancoParser(),
}
```

## 🔐 Sistema de Duplicados

### Generación de Hash
```python
hash_input = f"{date}_{description}_{amount}_{bank_type}"
transaction_hash = hashlib.sha256(hash_input.encode()).hexdigest()
```

### Prevención
- Hash único indexado en base de datos
- SQLAlchemy ignora inserts con hash duplicado
- Contador de duplicados en respuesta de upload

## 🤖 Auto-Categorización

### Funcionamiento

1. **Al categorizar una transacción**:
   - Se extrae el nombre del establecimiento (primera palabra de la descripción)
   - Se crea/actualiza registro en `store_mappings`

2. **En importaciones futuras**:
   - Se busca el establecimiento en `store_mappings`
   - Se aplica automáticamente la categoría guardada

3. **Actualización**:
   - Al cambiar categoría, se actualiza el mapeo
   - Opción de aplicar a todas las transacciones similares

### Ejemplo
```
Primera vez:
  Descripción: "MERCADONA VALENCIA" → Sin categoría
  Usuario categoriza como: "Comida"
  Se guarda: store_mappings["MERCADONA"] = "Comida"

Siguientes veces:
  Descripción: "MERCADONA VALENCIA" → Auto-categorizado como "Comida"
  Descripción: "MERCADONA ALICANTE" → Auto-categorizado como "Comida"
```

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=. --cov-report=html
```

## 🐛 Debugging

### Activar modo debug
```python
# En main.py
app = FastAPI(debug=True)
```

### Ver logs SQL
```python
# En database.py
engine = create_engine(
    DATABASE_URL,
    echo=True  # Muestra todas las queries SQL
)
```

### Usar debugger
```python
import pdb; pdb.set_trace()
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Ruta a la base de datos
DATABASE_PATH=./data/control_gastos.db

# Modo debug
DEBUG=True

# CORS origins (separados por coma)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📦 Dependencias Principales

- **fastapi** (0.104.1) - Framework web
- **uvicorn** (0.24.0) - Servidor ASGI
- **sqlalchemy** (2.0.23) - ORM
- **pydantic** (2.5.0) - Validación de datos
- **pandas** (2.1.3) - Procesamiento de datos
- **xlrd** (2.0.1) - Lectura de XLS
- **openpyxl** (3.1.2) - Lectura de XLSX
- **lxml** (4.9.3) - Parseo de HTML
- **chardet** (5.2.0) - Detección de encoding

## 🚀 Deploy

### Docker
```bash
docker build -t control-gastos-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data control-gastos-backend
```

### Producción con Gunicorn
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## 🤝 Contribuir

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) en la raíz del proyecto.

### Checklist para nuevos features:
- [ ] Añadir modelos si es necesario
- [ ] Crear schemas de Pydantic
- [ ] Implementar endpoints en routes/
- [ ] Añadir tests
- [ ] Actualizar esta documentación
- [ ] Probar en Docker

## 📄 Licencia

MIT - Ver [LICENSE](../LICENSE) en la raíz del proyecto.

---

**Desarrollado con FastAPI** ⚡
