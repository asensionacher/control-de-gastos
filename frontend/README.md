# Frontend - Control de Gastos UI 🎨

Aplicación web moderna construida con React para gestionar finanzas personales con una interfaz intuitiva y elegante en modo oscuro.

## ✨ Características

- 🎨 **Diseño moderno** con modo oscuro permanente
- 📱 **Responsive** - Funciona en móvil, tablet y escritorio
- ⚡ **Operaciones rápidas** sin recargas innecesarias
- 📊 **Gráficos interactivos** con Chart.js
- 🔍 **Filtrado avanzado** de transacciones
- 🏷️ **Categorización inteligente** masiva e individual
- 📄 **Paginación** eficiente (100 items por página)
- 🇪🇸 **100% en español**

## 📋 Requisitos

- Node.js 16 o superior
- npm 8 o superior

## 🚀 Instalación

```bash
# Instalar dependencias
npm install

# Copiar archivo de configuración
cp .env.example .env
```

## ▶️ Ejecutar

### Modo Desarrollo
```bash
npm start
```
La aplicación se abrirá en http://localhost:3000

### Build de Producción
```bash
npm run build
```
Los archivos optimizados estarán en la carpeta `build/`

### Servir Build de Producción
```bash
npm install -g serve
serve -s build -p 3000
```

## 📁 Estructura

```
frontend/
├── public/
│   ├── index.html           # HTML base
│   └── favicon.ico
│
├── src/
│   ├── pages/               # Páginas principales
│   │   ├── Dashboard.js     # Panel con estadísticas
│   │   ├── Transactions.js  # Lista con filtros
│   │   ├── Upload.js        # Importación de archivos
│   │   ├── Categories.js    # Gestión de categorías
│   │   └── Reports.js       # Gráficos y reportes
│   │
│   ├── services/
│   │   └── api.js           # Cliente de la API
│   │
│   ├── App.js               # Componente principal
│   ├── App.css              # Estilos globales
│   ├── index.js             # Punto de entrada
│   └── index.css            # Reset y variables CSS
│
├── package.json
├── .env.example
└── Dockerfile
```

## 🎨 Paleta de Colores

```css
--bg-primary: #0d0d0d      /* Fondo principal */
--bg-secondary: #1a1a1a    /* Fondo secundario */
--bg-tertiary: #262626     /* Fondo terciario */
--text-primary: #ffffff    /* Texto principal */
--text-secondary: #a8a8a8  /* Texto secundario */
--accent-primary: #ff9f1c  /* Acento naranja */
--accent-secondary: #2ec4b6 /* Acento verde-azul */
--income-color: #4caf50    /* Verde ingresos */
--expense-color: #f44336   /* Rojo gastos */
--border-color: #333333    /* Bordes */
--hover-bg: #2d2d2d        /* Hover */
```

## 📄 Páginas

### Dashboard (`/`)
Panel principal con vista general:
- 📊 4 cards de estadísticas (transacciones, ingresos, gastos, balance)
- 📈 Gráfico de evolución de últimos 6 meses
- 🔔 Alerta de transacciones sin categorizar
- 🔗 Enlaces rápidos a otras secciones

**Componentes:**
- Cards de estadísticas con iconos
- Line chart (Chart.js)
- Links de navegación

### Transacciones (`/transactions`)
Gestión completa de transacciones:

**Filtros:**
- 📝 Descripción (búsqueda en tiempo real, min 3 chars)
- 💰 Tipo (gastos/ingresos)
- 🏦 Banco (Kutxabank cuenta/tarjeta, Openbank, Imaginbank, BBVA, ING Direct)
- 🏷️ Categoría (incluye "Sin categoría")
- 📅 Rango de fechas (desde/hasta)
- 🔄 Botón limpiar filtros

**Funcionalidades:**
- ✅ Selección múltiple con checkboxes
- 🏷️ Categorización masiva con dropdown
- 🗑️ Eliminación masiva
- ✏️ Categorización individual inline
- 🔄 "Aplicar a todas las similares" (confirmación)
- 📄 Paginación (100 por página)
- ⬇️ Sin scroll al modificar/eliminar

**Componentes:**
- Formulario de filtros
- Barra de acciones masivas
- Tabla responsive con badges
- Dropdowns de categorías
- Controles de paginación

### Subir Archivo (`/upload`)
Importación de extractos bancarios:

**Modos:**
- 🤖 **Automático**: Detecta el banco del archivo
- ✋ **Manual**: Selección manual del banco

**Características:**
- 📁 Soporte múltiples formatos (CSV, XLS, XLSX, HTML)
- 🔍 Detección en tiempo real al seleccionar archivo
- ✅ Validación de formato
- 📊 Resultado detallado (total, importadas, duplicadas, errores)
- 📚 Información sobre formatos soportados

**Componentes:**
- Toggle auto/manual
- Selector de banco
- Input de archivo con detección
- Card de resultados
- Sección informativa

### Categorías (`/categories`)
Gestión de categorías y subcategorías:

**Funcionalidades:**
- ➕ Crear categorías
- ✏️ Editar nombre
- 🗑️ Eliminar (con confirmación)
- ➕ Añadir subcategorías
- 🎯 Inicializar categorías por defecto
- 📋 Vista en grid de cards

**Categorías por Defecto:**
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

**Componentes:**
- Formulario de creación
- Grid de cards
- Botones de acción inline
- Modal de edición

### Reportes (`/reports`)
Visualización de estadísticas:

**Selector de Período:**
- Últimos 3 meses
- Últimos 6 meses
- Último año
- Últimos 2 años

**Gráficos:**
- 📊 **Evolución mensual**: Bar chart (ingresos vs gastos)
- 🍩 **Distribución por categorías**: Doughnut chart con porcentajes
- 📋 **Detalle de categorías**: Tabla con total y porcentaje
- 💸 **Top 10 mayores gastos**: Tabla ordenada
- 📅 **Resumen mensual**: Tabla con ingresos/gastos/balance

**Componentes:**
- Selector de período
- Bar Chart (Chart.js)
- Doughnut Chart (Chart.js)
- Tablas con formato de moneda

## 🔌 Servicios API

Archivo: `src/services/api.js`

### Configuración
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### Funciones Principales

#### Transacciones
```javascript
getTransactions(params)           // GET /api/transactions/
updateTransaction(id, data)       // PUT /api/transactions/{id}
deleteTransaction(id)             // DELETE /api/transactions/{id}
bulkCategorize(ids, categoryId)   // POST /api/transactions/bulk-categorize
bulkDelete(ids)                   // POST /api/transactions/bulk-delete
```

#### Categorías
```javascript
getCategories()                   // GET /api/categories/
createCategory(name)              // POST /api/categories/
updateCategory(id, name)          // PUT /api/categories/{id}
deleteCategory(id)                // DELETE /api/categories/{id}
initDefaultCategories()           // POST /api/categories/init-default
```

#### Upload
```javascript
uploadCSV(file, bankType)         // POST /api/upload/
detectBank(file)                  // POST /api/upload/detect-bank
getBankTypes()                    // GET /api/upload/bank-types
```

#### Reportes
```javascript
getReportSummary(months)          // GET /api/reports/summary
getMonthlyReport()                // GET /api/reports/monthly
getCategoryReport()               // GET /api/reports/by-category
getTopExpenses(limit)             // GET /api/reports/top-expenses
getStats()                        // GET /api/reports/stats
```

## 🎯 Componentes Reutilizables

### Card
```jsx
<div className="card">
  <div className="card-header">
    <h2 className="card-title">Título</h2>
  </div>
  <div className="card-body">
    {/* Contenido */}
  </div>
</div>
```

### Form Group
```jsx
<div className="form-group">
  <label className="form-label">Etiqueta</label>
  <input className="form-control" />
</div>
```

### Button
```jsx
<button className="btn btn-primary">Primario</button>
<button className="btn btn-secondary">Secundario</button>
<button className="btn btn-danger">Peligro</button>
<button className="btn btn-small">Pequeño</button>
```

### Badge
```jsx
<span className="badge badge-income">+1000€</span>
<span className="badge badge-expense">-500€</span>
```

### Grid
```jsx
<div className="grid grid-2">  {/* 2 columnas */}
<div className="grid grid-3">  {/* 3 columnas */}
<div className="grid grid-4">  {/* 4 columnas */}
```

## 🧪 Testing

```bash
# Ejecutar tests
npm test

# Ejecutar tests con cobertura
npm test -- --coverage

# Ejecutar tests en modo watch
npm test -- --watch
```

## 🐛 Debugging

### React DevTools
Instala la extensión [React Developer Tools](https://react.dev/learn/react-developer-tools) para Chrome/Firefox.

### Debug en VSCode
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "React App",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

### Console Logging
```javascript
console.log('Debug:', data);
console.error('Error:', error);
console.table(transactions);
```

## ⚙️ Configuración

### Variables de Entorno (`.env`)
```bash
# URL de la API
REACT_APP_API_URL=http://localhost:8000

# Habilitar source maps en producción (no recomendado)
GENERATE_SOURCEMAP=false

# Puerto personalizado
PORT=3001
```

### Proxy para Desarrollo
```json
// package.json
{
  "proxy": "http://localhost:8000"
}
```

## 📦 Dependencias Principales

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2",
  "chart.js": "^4.4.0",
  "react-chartjs-2": "^5.2.0"
}
```

## 🚀 Deploy

### Build Optimizado
```bash
npm run build
```

### Análisis del Bundle
```bash
npm install -g source-map-explorer
npm run build
source-map-explorer 'build/static/js/*.js'
```

### Deploy en Netlify
```bash
# netlify.toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Deploy en Vercel
```bash
vercel --prod
```

### Docker
```bash
docker build -t control-gastos-frontend .
docker run -p 3000:80 control-gastos-frontend
```

## 🎨 Personalización

### Cambiar Paleta de Colores
Edita las variables CSS en `src/index.css`:
```css
:root {
  --accent-primary: #tu-color;
  --accent-secondary: #tu-color;
}
```

### Añadir Nueva Página

1. **Crear componente** en `src/pages/MiPagina.js`:
```jsx
import React from 'react';

function MiPagina() {
  return (
    <div className="container">
      <h1>Mi Nueva Página</h1>
    </div>
  );
}

export default MiPagina;
```

2. **Añadir ruta** en `src/App.js`:
```jsx
import MiPagina from './pages/MiPagina';

// En el Router:
<Route path="/mi-pagina" element={<MiPagina />} />
```

3. **Añadir link** en la navegación:
```jsx
<Link to="/mi-pagina">Mi Página</Link>
```

### Añadir Nuevo Gráfico

```jsx
import { Line, Bar, Doughnut, Pie } from 'react-chartjs-2';

const data = {
  labels: ['Ene', 'Feb', 'Mar'],
  datasets: [{
    label: 'Mi Dataset',
    data: [100, 200, 150],
    backgroundColor: 'rgba(255, 159, 28, 0.5)',
    borderColor: '#ff9f1c',
  }]
};

<Line data={data} options={...} />
```

## 🤝 Contribuir

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) en la raíz del proyecto.

### Checklist para nuevas features:
- [ ] Crear componente en `src/pages/` o `src/components/`
- [ ] Añadir estilos en CSS correspondiente
- [ ] Añadir funciones API en `src/services/api.js` si es necesario
- [ ] Añadir ruta en `App.js`
- [ ] Probar responsive en móvil/tablet
- [ ] Actualizar esta documentación

### Guía de Estilo
- Usar functional components con hooks
- Preferir `const` sobre `let`
- Nombres de componentes en PascalCase
- Nombres de archivos iguales al componente
- Comentarios claros en español
- Mantener componentes pequeños y reutilizables

## 📱 Responsive Breakpoints

```css
/* Móvil */
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1025px) {
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
}
```

## 📄 Licencia

MIT - Ver [LICENSE](../LICENSE) en la raíz del proyecto.

---

**Desarrollado con React** ⚛️
