# ¿SQLite o PostgreSQL?

## 🤔 Guía Rápida de Decisión

### Usa **SQLite** (por defecto) si:
- ✅ Uso personal o familiar (1-5 usuarios)
- ✅ Pocos usuarios simultáneos
- ✅ Quieres simplicidad (sin configurar servidor de BD)
- ✅ Datos moderados (<1GB)
- ✅ Deployment simple
- ✅ Backups sencillos (solo copiar el archivo .db)

**Iniciar con SQLite:**
```bash
docker compose up -d
```

### Usa **PostgreSQL** si:
- ✅ Muchos usuarios (>10)
- ✅ Usuarios simultáneos frecuentes
- ✅ Grandes volúmenes de datos (>1GB)
- ✅ Necesitas replicación o alta disponibilidad
- ✅ Queries complejas con optimización avanzada
- ✅ Producción profesional

**Iniciar con PostgreSQL:**
```bash
# 1. Configura la contraseña en backend/.env.postgres
# 2. Inicia con:
docker compose -f docker-compose.postgres.yml up -d
```

## 📊 Comparación

| Característica | SQLite | PostgreSQL |
|----------------|--------|------------|
| Configuración | ⭐⭐⭐⭐⭐ Ninguna | ⭐⭐⭐ Servidor adicional |
| Rendimiento (1 usuario) | ⭐⭐⭐⭐⭐ Excelente | ⭐⭐⭐⭐ Muy bueno |
| Rendimiento (10+ usuarios) | ⭐⭐ Limitado | ⭐⭐⭐⭐⭐ Excelente |
| Concurrencia | ⭐⭐ Bloqueos | ⭐⭐⭐⭐⭐ MVCC |
| Backup | ⭐⭐⭐⭐⭐ Copiar archivo | ⭐⭐⭐ Herramientas |
| Recursos | ⭐⭐⭐⭐⭐ Mínimos | ⭐⭐⭐ Más RAM |
| Escalabilidad | ⭐⭐ Limitada | ⭐⭐⭐⭐⭐ Alta |

## 🔄 Cambiar de SQLite a PostgreSQL

Consulta [POSTGRESQL_GUIDE.md](POSTGRESQL_GUIDE.md) para migrar datos.

## 💡 Recomendación

Para **uso personal/familiar**: SQLite es perfecto.  
Para **equipos o producción**: PostgreSQL es mejor opción.
