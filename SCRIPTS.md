# 📜 Scripts Disponibles - Control de Gastos

## Scripts Principales

### 🚀 `./start.sh`
**Inicio automático con Docker**

Ejecuta toda la configuración inicial y arranca la aplicación.

```bash
./start.sh
```

**Lo que hace:**
- Verifica Docker y Docker Compose
- Genera SECRET_KEY automáticamente (si no existe)
- Crea el archivo `backend/.env`
- Crea el directorio `data/`
- Construye las imágenes Docker
- Inicia los contenedores

**Primera vez:**
```bash
git clone <repo>
cd control-gastos
./start.sh
# Accede a http://localhost:3000/register
```

---

### 🔑 `./regenerate_secret.sh`
**Regenerar SECRET_KEY**

Genera una nueva SECRET_KEY y actualiza el archivo `.env`.

```bash
./regenerate_secret.sh
docker-compose restart backend
```

**Cuándo usar:**
- Comprometiste la SECRET_KEY
- Quieres invalidar todos los tokens activos
- Cambio de entorno (desarrollo → producción)

⚠️ **Advertencia:** Invalida todos los tokens JWT. Los usuarios deben volver a iniciar sesión.

---

### 🔧 `./setup_env.sh`
**Configuración de entorno sin Docker**

Genera el archivo `.env` para ejecución manual (sin Docker).

```bash
./setup_env.sh
```

**Cuándo usar:**
- Desarrollo sin Docker
- Configuración inicial manual
- Testing local

---

## Scripts de Backend

### 🔐 `backend/generate_secret_key.py`
**Generador de SECRET_KEY**

Genera una clave segura para JWT.

```bash
cd backend
python3 generate_secret_key.py
```

**Uso:**
- Desarrollo manual
- Copiar clave para producción
- Regenerar manualmente

---

## Comandos Docker Compose

### Inicio y detención

```bash
# Iniciar
docker-compose up -d

# Detener
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir e iniciar
docker-compose up -d --build
```

### Logs

```bash
# Ver todos los logs
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Mantenimiento

```bash
# Estado de contenedores
docker-compose ps

# Acceder al contenedor backend
docker-compose exec backend bash

# Acceder al contenedor frontend
docker-compose exec frontend sh

# Limpiar todo (¡cuidado!)
docker-compose down -v
rm -rf data/
```

---

## Flujos de Trabajo Comunes

### 🆕 Primera instalación

```bash
git clone <repo>
cd control-gastos
./start.sh
# Accede a http://localhost:3000/register
```

### 🔄 Actualizar la aplicación

```bash
git pull
docker-compose down
docker-compose up -d --build
```

### 🐛 Depuración

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar un servicio
docker-compose restart backend

# Reconstruir desde cero
docker-compose down
docker-compose up -d --build
```

### 💾 Backup de datos

```bash
# Backup de la base de datos
cp data/control_gastos.db data/backup-$(date +%Y%m%d).db

# Restaurar backup
cp data/backup-20250113.db data/control_gastos.db
docker-compose restart backend
```

### 🧹 Limpieza

```bash
# Limpiar contenedores detenidos
docker-compose down

# Limpiar todo (datos incluidos)
docker-compose down -v
rm -rf data/ backend/.env

# Limpiar imágenes Docker antiguas
docker system prune -a
```

### 🔐 Cambiar SECRET_KEY

```bash
./regenerate_secret.sh
docker-compose restart backend
# Los usuarios deben volver a iniciar sesión
```

---

## Desarrollo sin Docker

### Configuración inicial

```bash
# Backend
cd backend
./setup_env.sh  # o python3 generate_secret_key.py y crear .env manualmente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (nueva terminal)
cd frontend
npm install
npm start
```

### Ejecución

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## Variables de Entorno

### Archivo `backend/.env`

```bash
# Generado automáticamente por start.sh
SECRET_KEY=<generada-automáticamente>

# Opcional para desarrollo
DATABASE_PATH=./data/control_gastos.db
ALLOWED_ORIGINS=http://localhost:3000
```

### Producción

```bash
# Establecer en el entorno del sistema
export SECRET_KEY="tu-clave-super-segura-de-produccion"
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
export ALLOWED_ORIGINS="https://tudominio.com"
```

---

## Solución de Problemas

### Error: "SECRET_KEY not found"
```bash
./regenerate_secret.sh
docker-compose restart backend
```

### Error: "port already allocated"
```bash
# Cambiar puertos en docker-compose.yml o detener el servicio que los usa
docker-compose down
# Editar docker-compose.yml (cambiar 3000:3000 y 8000:8000)
docker-compose up -d
```

### Base de datos corrupta
```bash
docker-compose down
rm data/control_gastos.db
docker-compose up -d
# Restaurar desde backup si existe
```

### Contenedores no arrancan
```bash
docker-compose down
docker-compose up -d --build
docker-compose logs -f
```

---

**Documentación completa:**
- [README.md](README.md) - Descripción general
- [DOCKER.md](DOCKER.md) - Guía completa de Docker
- [QUICK_START.md](QUICK_START.md) - Inicio rápido detallado
- [AUTH_IMPLEMENTATION.md](AUTH_IMPLEMENTATION.md) - Sistema de autenticación

**¿Necesitas ayuda?** Abre un issue en GitHub.
