# Guía de Inicio Rápido - Control de Gastos

## 🚀 Inicio Rápido (con Docker)

### 1. Requisitos Previos
- Docker instalado
- Docker Compose instalado

### 2. Iniciar la aplicación

```bash
# Opción 1: Usar el script de inicio
./start.sh

# Opción 2: Manualmente
docker-compose up -d
```

### 3. Acceder a la aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs

### 4. Primeros pasos

#### a) Inicializar categorías
1. Ve a la sección "Categorías"
2. Haz clic en "Cargar Por Defecto" para crear las categorías predefinidas:
   - Hipoteca, Coche, Gasolina, Parking, Comida, Niños, Cumpleaños, 
     Préstamos, Suministros, Colegio, Salud, IBI

#### b) Subir tu primer CSV
1. Ve a "Subir CSV/XLS"
2. Selecciona el banco correspondiente:
   - Kutxabank - Cuenta Corriente
   - Kutxabank - Tarjeta de Crédito
   - Openbank
   - Imaginbank
3. Selecciona tu archivo CSV o XLS
4. Haz clic en "Subir ficheros/"
5. El sistema detectará automáticamente duplicados

#### c) Categorizar transacciones
1. Ve a "Transacciones"
2. Para cada transacción sin categoría, haz clic en "Editar"
3. Selecciona la categoría apropiada
4. La próxima vez que aparezca ese establecimiento, se categorizará automáticamente

#### d) Ver reportes
1. Ve a "Reportes"
2. Visualiza:
   - Evolución mensual de ingresos y gastos
   - Distribución por categorías
   - Mayores gastos
   - Resumen mensual detallado

## 📝 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend

# Ver logs solo del frontend
docker-compose logs -f frontend

# Detener la aplicación
docker-compose down

# Detener y eliminar volúmenes (¡CUIDADO! Esto borra la base de datos)
docker-compose down -v

# Reconstruir los contenedores
docker-compose build --no-cache
docker-compose up -d
```

## 🔧 Desarrollo Local (sin Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_PATH=./data/control_gastos.db
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

## 📊 Estructura de los CSV

Los CSV deben descargarse directamente de tu banco. El sistema detecta automáticamente el formato de cada entidad.

### Formato general esperado:
- **Fecha**: DD/MM/YYYY
- **Descripción**: Texto del movimiento
- **Importe**: Número con coma decimal (formato español)
- **Saldo**: (Opcional) Saldo después del movimiento

### Ejemplos de formato por banco:

**Kutxabank Cuenta**: `Fecha;Concepto;Importe;Saldo`
**Kutxabank Tarjeta**: `Fecha;Fecha Valor;Concepto;Importe`
**Openbank**: `Fecha;Concepto;Cargo;Abono;Saldo`
**Imaginbank**: `Fecha;Concepto;Importe;Saldo`

## 🔍 Características Clave

### Detección de Duplicados
El sistema genera un hash único para cada transacción basado en:
- Fecha
- Descripción
- Importe
- Tipo de banco

Esto previene importaciones duplicadas automáticamente.

### Auto-categorización
Cuando categorizas una transacción, el sistema:
1. Extrae el nombre del establecimiento
2. Guarda la relación establecimiento-categoría
3. Auto-categoriza futuras transacciones del mismo establecimiento

### Subcategorías
Cada categoría puede tener múltiples subcategorías para un análisis más detallado:
- Ejemplo: Categoría "Comida" → Subcategorías: "Supermercado", "Restaurantes", "Comida rápida"

## 🎨 Personalización

### Añadir nuevas categorías
1. Ve a "Categorías"
2. Escribe el nombre en "Nueva Categoría"
3. Haz clic en "Añadir Categoría"

### Añadir subcategorías
1. En cada tarjeta de categoría
2. Escribe el nombre de la subcategoría
3. Haz clic en "Añadir"

### Modificar categorías existentes
- Haz clic en "Editar" en la categoría
- Cambia el nombre y confirma

## 🛟 Solución de Problemas

### El CSV no se importa correctamente
- Verifica que el archivo sea realmente CSV (no Excel)
- Asegúrate de seleccionar el banco correcto
- Comprueba que el formato coincida con el esperado
- Revisa los logs: `docker-compose logs backend`

### Las transacciones no se auto-categorizan
- Asegúrate de haber categorizado al menos una transacción del mismo establecimiento previamente
- El nombre del establecimiento debe coincidir exactamente

### No aparecen datos en los gráficos
- Verifica que tienes transacciones importadas
- Asegúrate de haber categorizado al menos algunas transacciones
- Ajusta el período de análisis en "Reportes"

### Error al iniciar los contenedores
```bash
# Limpia y reinicia
docker-compose down
docker system prune -f
docker-compose up -d --build
```

## 📦 Backup de Datos

La base de datos se encuentra en `./data/control_gastos.db`

Para hacer backup:
```bash
# Copiar la base de datos
cp data/control_gastos.db data/backup_$(date +%Y%m%d).db

# O detener los contenedores y copiar
docker-compose down
cp data/control_gastos.db ~/backups/control_gastos_$(date +%Y%m%d).db
docker-compose up -d
```

## 🔐 Seguridad

- La aplicación está diseñada para uso local
- No expone puertos al exterior por defecto
- Los datos se almacenan localmente en tu máquina
- **Importante**: Haz backups regulares de la carpeta `data/`

## 🆘 Soporte

Si encuentras problemas:
1. Revisa esta guía
2. Consulta los logs: `docker-compose logs -f`
3. Verifica la documentación de la API: http://localhost:8000/docs
4. Abre un issue en el repositorio

## 📄 Licencia

MIT License - Libre para uso personal y comercial
