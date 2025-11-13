# Guía de PostgreSQL

## 📘 Usar PostgreSQL en lugar de SQLite

La aplicación soporta tanto **SQLite** (por defecto) como **PostgreSQL**. Esta guía explica cómo cambiar a PostgreSQL.

## 🔀 Diferencias entre SQLite y PostgreSQL

### SQLite (Por Defecto)
- ✅ **Ventajas**:
  - Sin configuración adicional
  - Archivo único, fácil de respaldar
  - Perfecto para uso personal/familiar
  - Menos recursos
- ❌ **Limitaciones**:
  - No apto para muchos usuarios concurrentes
  - Menos opciones de optimización

### PostgreSQL (Opcional)
- ✅ **Ventajas**:
  - Mejor para múltiples usuarios simultáneos
  - Mejor rendimiento en grandes volúmenes
  - Características avanzadas (índices, vistas, etc.)
  - Backups y replicación profesionales
- ❌ **Limitaciones**:
  - Requiere servidor adicional (más recursos)
  - Más complejo de configurar

## 🚀 Cómo Cambiar a PostgreSQL

### Opción 1: Usar Docker Compose (Recomendado)

#### 1. Configurar variables de entorno

Edita el archivo `backend/.env.postgres`:

```bash
# Cambiar la contraseña por defecto
POSTGRES_PASSWORD=tu_password_super_seguro_aqui

# El resto de valores están bien por defecto
POSTGRES_USER=control_gastos
POSTGRES_DB=control_gastos
```

#### 2. Iniciar con PostgreSQL

```bash
# Detener los contenedores actuales (SQLite)
docker compose down

# Iniciar con PostgreSQL
docker compose -f docker-compose.postgres.yml up -d

# Ver los logs
docker compose -f docker-compose.postgres.yml logs -f
```

#### 3. Inicializar la base de datos

```bash
# Ejecutar el script de inicialización dentro del contenedor
docker compose -f docker-compose.postgres.yml exec backend python init_db.py

# O ejecutar migraciones si ya tenías datos
docker compose -f docker-compose.postgres.yml exec backend python migrate_add_user_id.py
```

#### 4. Verificar que funciona

```bash
# Verificar logs del backend
docker compose -f docker-compose.postgres.yml logs backend | grep -i postgres

# Deberías ver: "🐘 Using PostgreSQL database: ..."
```

### Opción 2: PostgreSQL Externo (No Docker)

Si ya tienes PostgreSQL instalado localmente o en un servidor:

#### 1. Crear la base de datos

```sql
CREATE DATABASE control_gastos;
CREATE USER control_gastos WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE control_gastos TO control_gastos;
```

#### 2. Configurar la variable de entorno

En `backend/.env`:

```bash
DATABASE_URL=postgresql://control_gastos:tu_password@localhost:5432/control_gastos
```

#### 3. Inicializar

```bash
cd backend
python init_db.py
```

## 📦 Migrar Datos de SQLite a PostgreSQL

Si ya tienes datos en SQLite y quieres migrarlos a PostgreSQL:

### Método 1: Exportar e Importar CSV

```bash
# 1. Exportar datos de SQLite (desde Python)
python << EOF
import sqlite3
import pandas as pd

conn = sqlite3.connect('./data/control_gastos.db')

# Exportar cada tabla
for table in ['users', 'categories', 'subcategories', 'transactions', 'store_mappings']:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(f'{table}.csv', index=False)
    print(f"✓ Exportado {table}: {len(df)} filas")

conn.close()
EOF

# 2. Iniciar PostgreSQL
docker compose -f docker-compose.postgres.yml up -d

# 3. Importar los CSVs (necesitarás crear un script Python personalizado)
```

### Método 2: Usar pgloader (Recomendado)

```bash
# Instalar pgloader
sudo apt-get install pgloader  # Ubuntu/Debian
brew install pgloader           # macOS

# Migrar
pgloader sqlite://./data/control_gastos.db \
         postgresql://control_gastos:password@localhost:5432/control_gastos
```

## 🔧 Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar PostgreSQL
docker compose -f docker-compose.postgres.yml up -d

# Detener
docker compose -f docker-compose.postgres.yml down

# Ver logs
docker compose -f docker-compose.postgres.yml logs -f backend
docker compose -f docker-compose.postgres.yml logs -f db

# Reiniciar solo el backend
docker compose -f docker-compose.postgres.yml restart backend
```

### Acceder a PostgreSQL

```bash
# Conectar con psql
docker compose -f docker-compose.postgres.yml exec db psql -U control_gastos -d control_gastos

# Comandos útiles en psql:
\dt              # Listar tablas
\d+ users        # Describir tabla users
\q               # Salir
```

### Backup y Restore

```bash
# Backup
docker compose -f docker-compose.postgres.yml exec db pg_dump -U control_gastos control_gastos > backup.sql

# Restore
docker compose -f docker-compose.postgres.yml exec -T db psql -U control_gastos control_gastos < backup.sql
```

## ⚙️ Configuración Avanzada

### Variables de Entorno Disponibles

En `backend/.env.postgres`:

```bash
# PostgreSQL
POSTGRES_USER=control_gastos
POSTGRES_PASSWORD=cambiar_en_produccion
POSTGRES_DB=control_gastos
POSTGRES_HOST=db
POSTGRES_PORT=5432

# O usar DATABASE_URL directamente
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Seguridad
SECRET_KEY=tu_clave_secreta_jwt
REGISTRATION_ENABLED=false  # Cerrar registro después de crear usuarios

# Rate Limiting
REGISTER_MAX_ATTEMPTS=5
REGISTER_WINDOW_MINUTES=60
LOGIN_MAX_ATTEMPTS=10
LOGIN_WINDOW_MINUTES=15
```

### Optimización de PostgreSQL

Para mejor rendimiento, puedes ajustar en `docker-compose.postgres.yml`:

```yaml
db:
  environment:
    - POSTGRES_SHARED_BUFFERS=256MB
    - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
    - POSTGRES_MAX_CONNECTIONS=100
  command: >
    postgres
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
    -c max_connections=100
```

## 🔄 Volver a SQLite

Si quieres volver a usar SQLite:

```bash
# Detener PostgreSQL
docker compose -f docker-compose.postgres.yml down

# Iniciar con SQLite
docker compose up -d

# Los datos de SQLite están en ./data/control_gastos.db
```

## 🆘 Troubleshooting

### Error: "could not connect to server"

```bash
# Verificar que PostgreSQL está corriendo
docker compose -f docker-compose.postgres.yml ps

# Ver logs de PostgreSQL
docker compose -f docker-compose.postgres.yml logs db
```

### Error: "password authentication failed"

Verifica que la contraseña en `.env.postgres` coincida con la usada en `DATABASE_URL`.

### Error: "database does not exist"

```bash
# Recrear la base de datos
docker compose -f docker-compose.postgres.yml exec db createdb -U control_gastos control_gastos
```

### El backend no puede conectar

```bash
# Verificar el healthcheck de PostgreSQL
docker compose -f docker-compose.postgres.yml exec db pg_isready -U control_gastos

# Debe devolver: "accepting connections"
```

## 📊 Monitoreo

### Ver estadísticas de la base de datos

```sql
-- Conectar a PostgreSQL
docker compose -f docker-compose.postgres.yml exec db psql -U control_gastos -d control_gastos

-- Ver tamaño de tablas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Ver número de registros por tabla
SELECT 
    schemaname,
    tablename,
    n_live_tup AS row_count
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

## 🎯 Recomendaciones

- **Desarrollo local**: Usar SQLite (más simple)
- **Producción con pocos usuarios (<10)**: SQLite es suficiente
- **Producción con muchos usuarios (>10)**: PostgreSQL recomendado
- **Grandes volúmenes de datos (>10GB)**: PostgreSQL
- **Necesitas replicación/HA**: PostgreSQL

## 📚 Recursos Adicionales

- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [Docker PostgreSQL Image](https://hub.docker.com/_/postgres)
