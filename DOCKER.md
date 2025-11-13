# 🐳 Guía Docker - Control de Gastos

## Inicio Súper Rápido

```bash
./start.sh
```

¡Eso es todo! Abre http://localhost:3000/register y crea tu usuario.

---

## ¿Qué hace `start.sh`?

El script automatiza completamente la configuración:

1. ✅ **Verifica** que Docker y Docker Compose estén instalados
2. 🔑 **Genera** una SECRET_KEY segura automáticamente
3. 📝 **Crea** el archivo `backend/.env` con la configuración
4. 📁 **Crea** el directorio `data/` para la base de datos
5. 🏗️ **Construye** las imágenes Docker
6. 🚀 **Inicia** los contenedores

## Comandos Útiles

### Iniciar la aplicación
```bash
./start.sh
# o manualmente:
docker-compose up -d
```

### Ver los logs en tiempo real
```bash
docker-compose logs -f
# Solo backend:
docker-compose logs -f backend
# Solo frontend:
docker-compose logs -f frontend
```

### Detener la aplicación
```bash
docker-compose down
```

### Reiniciar después de cambios
```bash
docker-compose restart
# o reconstruir:
docker-compose up -d --build
```

### Ver contenedores en ejecución
```bash
docker-compose ps
```

### Acceder al contenedor backend
```bash
docker-compose exec backend bash
```

### Limpiar todo (¡cuidado! elimina la base de datos)
```bash
docker-compose down -v
rm -rf data/
```

## Regenerar SECRET_KEY

Si necesitas regenerar la SECRET_KEY (invalida todos los tokens):

```bash
./regenerate_secret.sh
docker-compose restart backend
```

## Estructura de Archivos

```
control-de-gastos/
├── start.sh                    # Script de inicio automático ⭐
├── regenerate_secret.sh        # Regenerar SECRET_KEY
├── docker-compose.yml          # Configuración de contenedores
├── backend/
│   ├── .env                    # Variables de entorno (auto-generado)
│   ├── .env.example           # Plantilla de configuración
│   ├── Dockerfile             # Imagen del backend
│   └── ...
├── frontend/
│   ├── Dockerfile             # Imagen del frontend
│   └── ...
└── data/                      # Base de datos SQLite (persistente)
    └── control_gastos.db
```

## Variables de Entorno

El archivo `backend/.env` contiene:

```bash
SECRET_KEY=<generada-automáticamente>
```

**Importante:** 
- Este archivo es creado automáticamente por `start.sh`
- Está en `.gitignore` (no se sube a git)
- Para producción, usa una SECRET_KEY diferente

## Puertos

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Solución de Problemas

### Error: "Cannot connect to Docker daemon"
Docker no está ejecutándose. Inicia Docker Desktop o el servicio de Docker.

### Error: "port is already allocated"
El puerto 3000 o 8000 ya está en uso. Detén la aplicación que lo usa o modifica los puertos en `docker-compose.yml`.

### Backend no arranca: "SECRET_KEY not found"
El archivo `.env` no se creó correctamente. Ejecuta:
```bash
./regenerate_secret.sh
docker-compose restart backend
```

### Los cambios en el código no se reflejan
Reconstruye las imágenes:
```bash
docker-compose up -d --build
```

### Limpiar y empezar de cero
```bash
docker-compose down -v
rm -rf data/ backend/.env
./start.sh
```

## Producción

Para producción:

1. **Genera una SECRET_KEY fuerte:**
   ```bash
   python3 backend/generate_secret_key.py
   ```

2. **Configúrala como variable de entorno del sistema:**
   ```bash
   export SECRET_KEY="tu-clave-super-segura"
   ```

3. **Usa un servidor de base de datos real** (PostgreSQL, MySQL)

4. **Configura HTTPS** con un proxy inverso (nginx, traefik)

5. **Ajusta CORS** para tu dominio en el backend

6. **Desactiva el modo reload** en el comando de uvicorn

7. **Usa volumes para persistencia** adecuada

## Mantenimiento

### Backup de la base de datos
```bash
cp data/control_gastos.db data/backup-$(date +%Y%m%d).db
```

### Actualizar la aplicación
```bash
git pull
docker-compose down
docker-compose up -d --build
```

### Ver espacio usado por Docker
```bash
docker system df
```

### Limpiar imágenes antiguas
```bash
docker system prune -a
```

---

**¿Problemas?** Consulta la [documentación completa](README.md) o abre un issue.
