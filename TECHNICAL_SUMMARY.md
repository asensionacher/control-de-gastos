# Control de Gastos - Resumen Técnico

## 📋 Descripción General

Aplicación web completa para el control financiero doméstico con soporte para múltiples bancos españoles, desarrollada con Python (FastAPI) en el backend y React en el frontend, completamente dockerizada.

## 🏗️ Arquitectura

### Backend (Python/FastAPI)
- **Framework**: FastAPI 0.104.1
- **Base de datos**: SQLite (LiteDB)
- **ORM**: SQLAlchemy 2.0.23
- **Procesamiento CSV**: Pandas 2.1.3
- **Puerto**: 8000

### Frontend (React)
- **Framework**: React 18.2.0
- **Gráficos**: Chart.js 4.4.0 + react-chartjs-2
- **Routing**: React Router DOM 6.20.0
- **HTTP Client**: Axios 1.6.2
- **Puerto**: 3000

### Infraestructura
- **Contenedorización**: Docker + Docker Compose
- **Base de datos**: SQLite persistente en volumen

## 📁 Estructura del Proyecto

```
control-gastos/
├── backend/
│   ├── routes/              # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── transactions.py  # CRUD de transacciones
│   │   ├── categories.py    # Gestión de categorías
│   │   ├── upload.py        # Importación de CSV
│   │   └── reports.py       # Reportes y estadísticas
│   ├── database.py          # Configuración SQLAlchemy
│   ├── models.py            # Modelos de datos
│   ├── schemas.py           # Schemas Pydantic
│   ├── parsers.py           # Parsers de CSV por banco
│   ├── main.py              # Aplicación FastAPI
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js      # Panel principal
│   │   │   ├── Transactions.js   # Lista de transacciones
│   │   │   ├── Upload.js         # Subida de CSV
│   │   │   ├── Categories.js     # Gestión de categorías
│   │   │   └── Reports.js        # Reportes visuales
│   │   ├── services/
│   │   │   └── api.js            # Cliente API
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
│
├── data/                    # Volumen de datos (SQLite)
│   └── .gitignore
│
├── docker-compose.yml       # Orquestación de servicios
├── start.sh                 # Script de inicio
├── README.md
├── QUICK_START.md
├── LICENSE
└── .gitignore
```

## 🗄️ Modelo de Datos

### Tablas Principales

#### `categories`
- id (PK)
- name (UNIQUE)
- created_at

#### `subcategories`
- id (PK)
- name
- category_id (FK)
- created_at

#### `transactions`
- id (PK)
- bank_type (kutxabank_account, kutxabank_card, openbank, imaginbank, bbva, ing)
- date (indexed)
- description
- amount
- balance
- reference
- extra_info
- category_id (FK)
- subcategory_id (FK)
- transaction_hash (UNIQUE, indexed) - Para detección de duplicados
- created_at
- updated_at

#### `store_mappings`
- id (PK)
- store_name (UNIQUE, indexed)
- category_id (FK)
- subcategory_id (FK)
- created_at
- updated_at

## 🔌 API Endpoints

### Transacciones
- `GET /api/transactions/` - Listar transacciones (con filtros)
- `GET /api/transactions/{id}` - Obtener transacción
- `PUT /api/transactions/{id}` - Actualizar transacción
- `DELETE /api/transactions/{id}` - Eliminar transacción
- `GET /api/transactions/uncategorized/count` - Contar sin categorizar

### Categorías
- `GET /api/categories/` - Listar todas las categorías
- `POST /api/categories/` - Crear categoría
- `PUT /api/categories/{id}` - Actualizar categoría
- `DELETE /api/categories/{id}` - Eliminar categoría
- `GET /api/categories/{id}/subcategories` - Listar subcategorías
- `POST /api/categories/{id}/subcategories` - Crear subcategoría
- `PUT /api/categories/subcategories/{id}` - Actualizar subcategoría
- `DELETE /api/categories/subcategories/{id}` - Eliminar subcategoría
- `POST /api/categories/init-default` - Inicializar categorías por defecto

### Upload
- `POST /api/upload/` - Subir archivo CSV
- `GET /api/upload/bank-types` - Listar tipos de banco soportados

### Reportes
- `GET /api/reports/monthly` - Reporte mensual
- `GET /api/reports/by-category` - Reporte por categoría
- `GET /api/reports/top-expenses` - Mayores gastos
- `GET /api/reports/summary` - Resumen completo
- `GET /api/reports/stats` - Estadísticas generales

## 🎨 Características del Frontend

### Diseño
- **Modo oscuro permanente** con paleta de colores personalizada
- **Responsive** - Adaptable a móviles y tablets
- **Animaciones suaves** para mejor UX
- **Interfaz completamente en español**

### Páginas

#### Dashboard
- Estadísticas generales (transacciones, ingresos, gastos, balance)
- Gráfico de evolución de últimos 6 meses
- Alertas de transacciones sin categorizar

#### Transacciones
- Lista completa con filtros (banco, categoría, fechas)
- Edición inline de categorías
- Badges de color según tipo (ingreso/gasto)
- Eliminación de transacciones

#### Subir CSV
- Selector de banco
- Drag & drop o selección de archivo
- Validación de formato
- Resultado detallado de la importación
- Información sobre formatos soportados

#### Categorías
- Gestión completa de categorías y subcategorías
- Creación, edición y eliminación
- Inicialización de categorías por defecto
- Vista en grid de tarjetas

#### Reportes
- **Evolución mensual**: Gráfico de barras (ingresos vs gastos)
- **Distribución por categorías**: Gráfico de dona con porcentajes
- **Detalle de categorías**: Lista con importes y porcentajes
- **Mayores gastos**: Tabla de top 10
- **Resumen mensual**: Tabla detallada por mes
- Selector de período (3, 6, 12, 24 meses)

## 🔧 Parsers de CSV

Cada banco tiene su propio parser que:
1. Detecta automáticamente la codificación del archivo
2. Maneja formatos específicos (separadores, decimales)
3. Parsea fechas en formato DD/MM/YYYY
4. Extrae descripción, importe y saldo
5. Genera hash único para detección de duplicados

### Bancos Soportados

#### Kutxabank - Cuenta Corriente
- Formato: `Fecha;Concepto;Importe;Saldo`
- Separador: `;`
- Decimal: `,`

#### Kutxabank - Tarjeta de Crédito
- Formato: `Fecha;Fecha Valor;Concepto;Importe`
- Columnas adicionales para fecha de valor

#### Openbank
- Formato: `Fecha;Concepto;Cargo;Abono;Saldo`
- Columnas separadas para cargo y abono

#### Imaginbank
- Formato: `Fecha;Concepto;Importe;Saldo`
- Similar a cuenta Kutxabank

#### BBVA
- Formato: XLSX con columnas `F.Valor;Fecha;Concepto;Movimiento;Importe;Disponible`
- Detección dinámica de cabeceras
- Combina concepto y movimiento en descripción

#### ING Direct
- Formato: XLS con columnas `F. VALOR;CATEGORÍA;SUBCATEGORÍA;DESCRIPCIÓN;IMPORTE (€);SALDO (€)`
- Detección dinámica de cabeceras
- Incluye categorización propia del banco

## 🛡️ Características de Seguridad

### Detección de Duplicados
- Hash SHA-256 basado en: fecha + descripción + importe + tipo_banco
- Índice único en base de datos
- Prevención automática de importaciones duplicadas

### Auto-categorización Inteligente
1. Al categorizar una transacción, se extrae el nombre del establecimiento
2. Se crea/actualiza un mapeo en `store_mappings`
3. Futuras transacciones del mismo establecimiento se categorizan automáticamente
4. El mapeo es actualizable en cualquier momento

## 📊 Sistema de Reportes

### Métricas Disponibles
- Total de transacciones
- Ingresos totales
- Gastos totales
- Balance general
- Transacciones sin categorizar

### Visualizaciones
- **Line Chart**: Evolución temporal
- **Bar Chart**: Comparativas mensuales
- **Doughnut Chart**: Distribución por categorías
- **Tables**: Detalles y rankings

### Filtros
- Período temporal (últimos 3, 6, 12, 24 meses)
- Rango de fechas personalizado
- Por categoría
- Por tipo de banco

## 🚀 Despliegue

### Con Docker (Recomendado)
```bash
./start.sh
# o
docker-compose up -d
```

### Manual

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_PATH=./data/control_gastos.db
uvicorn main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

## 🔄 Flujo de Trabajo Típico

1. **Inicialización**
   - Iniciar la aplicación con Docker
   - Crear categorías (o usar las predeterminadas)

2. **Importación de Datos**
   - Descargar CSV del banco
   - Seleccionar tipo de banco en la app
   - Subir CSV
   - Revisar resultado de importación

3. **Categorización**
   - Ir a lista de transacciones
   - Asignar categorías a transacciones nuevas
   - El sistema aprende y auto-categoriza futuras transacciones

4. **Análisis**
   - Visualizar dashboard para resumen rápido
   - Explorar reportes detallados
   - Comparar períodos
   - Identificar patrones de gasto

5. **Mantenimiento**
   - Actualizar categorías según necesidad
   - Crear subcategorías para análisis más fino
   - Revisar y corregir categorizaciones erróneas

## 🎯 Categorías por Defecto

1. Hipoteca
2. Coche
3. Gasolina
4. Parking
5. Comida
6. Niños
7. Cumpleaños
8. Préstamos
9. Suministros
10. Colegio
11. Salud
12. IBI

Cada una puede tener subcategorías ilimitadas.

## 📦 Dependencias Clave

### Backend
- `fastapi` - Framework web moderno y rápido
- `uvicorn` - Servidor ASGI
- `sqlalchemy` - ORM
- `pydantic` - Validación de datos
- `pandas` - Procesamiento de CSV
- `chardet` - Detección de codificación

### Frontend
- `react` - Librería UI
- `react-router-dom` - Navegación
- `axios` - Cliente HTTP
- `chart.js` + `react-chartjs-2` - Gráficos
- `react-scripts` - Herramientas de desarrollo

## 🔮 Posibles Mejoras Futuras

- [ ] Exportación de reportes a PDF
- [ ] Más tipos de gráficos (treemap, sankey)
- [ ] Presupuestos por categoría
- [ ] Alertas de gastos inusuales
- [ ] Múltiples usuarios/cuentas
- [ ] Autenticación y autorización
- [ ] API para importación automática
- [ ] Aplicación móvil
- [ ] Predicciones basadas en IA
- [ ] Comparación con períodos anteriores
- [ ] Objetivos de ahorro
- [ ] Sincronización con bancos (Open Banking)

## 📄 Licencia

MIT - Uso libre para fines personales y comerciales

## 👨‍💻 Desarrollo

El proyecto está listo para desarrollo inmediato:
- Hot reload en backend (FastAPI)
- Hot reload en frontend (React)
- Base de datos persistente
- Logs accesibles
- Documentación interactiva en `/docs`

---

**Desarrollado con ❤️ para el control financiero personal**
