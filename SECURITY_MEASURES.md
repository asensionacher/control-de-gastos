# Medidas de Seguridad para Registro de Usuarios

## 🛡️ Protecciones Implementadas

Para prevenir el abuso del registro de usuarios, se han implementado las siguientes medidas de seguridad:

## 1. Rate Limiting (Limitación de Tasa)

### ✅ Protección contra Registro Masivo

- **Límite por defecto**: 5 intentos de registro por hora desde la misma IP
- **Configurable** mediante variables de entorno:
  ```bash
  REGISTER_MAX_ATTEMPTS=5          # Número de intentos permitidos
  REGISTER_WINDOW_MINUTES=60       # Ventana de tiempo (60 min = 1 hora)
  ```

### ✅ Protección contra Fuerza Bruta en Login

- **Límite por defecto**: 10 intentos de login cada 15 minutos desde la misma IP
- **Configurable** mediante variables de entorno:
  ```bash
  LOGIN_MAX_ATTEMPTS=10            # Número de intentos permitidos
  LOGIN_WINDOW_MINUTES=15          # Ventana de tiempo en minutos
  ```

### Cómo funciona:
- El sistema rastrea las peticiones por dirección IP
- Si se excede el límite, devuelve un error `429 Too Many Requests`
- Los contadores se resetean automáticamente después de la ventana de tiempo
- Las peticiones antiguas se limpian automáticamente

## 2. Validación de Contraseña Fuerte

### ✅ Requisitos Obligatorios

Las contraseñas deben cumplir:

- ✓ Mínimo 8 caracteres
- ✓ Máximo 100 caracteres
- ✓ Al menos una letra minúscula (a-z)
- ✓ Al menos una letra mayúscula (A-Z)
- ✓ Al menos un número (0-9)

### Ejemplos:

❌ **Rechazadas**:
- `password` - Sin mayúsculas ni números
- `Pass123` - Menos de 8 caracteres
- `password123` - Sin mayúsculas
- `PASSWORD123` - Sin minúsculas
- `Password` - Sin números

✅ **Aceptadas**:
- `Password123`
- `MiClave2024`
- `Segur0Pass`

## 3. Validación de Nombre de Usuario

### ✅ Requisitos

- Mínimo 3 caracteres
- Máximo 50 caracteres
- Solo letras, números, guiones (-) y guiones bajos (_)
- No se permiten espacios ni caracteres especiales

### Ejemplos:

❌ **Rechazados**:
- `ab` - Menos de 3 caracteres
- `mi usuario` - Contiene espacios
- `user@email` - Contiene @ (no permitido)

✅ **Aceptados**:
- `sergi`
- `usuario_123`
- `mi-usuario`
- `user2024`

## 4. Control de Habilitación de Registro

### ✅ Deshabilitar Registro Público

Puedes **cerrar completamente** el registro de nuevos usuarios después de crear las cuentas iniciales:

```bash
# En el archivo .env o docker-compose.yml
REGISTRATION_ENABLED=false
```

Cuando está deshabilitado:
- Cualquier intento de registro devuelve un error `403 Forbidden`
- Los usuarios existentes pueden seguir haciendo login normalmente
- Solo un administrador con acceso al servidor puede habilitar el registro nuevamente

### Recomendación de uso:

1. **Fase inicial**: Dejar `REGISTRATION_ENABLED=true`
2. **Crear usuarios**: Registrar todos los usuarios necesarios (sergi, familia, etc.)
3. **Cerrar registro**: Cambiar a `REGISTRATION_ENABLED=false`
4. **Producción**: El sistema queda cerrado a nuevos registros

## 5. Endpoint de Verificación

### ✅ Consultar Estado de Seguridad

Endpoint público para verificar el estado del registro y límites:

```bash
GET /api/auth/registration-status
```

**Respuesta**:
```json
{
  "registration_enabled": true,
  "rate_limits": {
    "register": {
      "max_attempts": 5,
      "window_minutes": 60,
      "remaining_attempts": 3,
      "reset_time": "2025-11-13T12:45:00" // Si remaining_attempts = 0
    },
    "login": {
      "max_attempts": 10,
      "window_minutes": 15,
      "remaining_attempts": 8,
      "reset_time": null
    }
  },
  "password_requirements": {
    "min_length": 8,
    "max_length": 100,
    "requires_lowercase": true,
    "requires_uppercase": true,
    "requires_number": true,
    "requires_special": false
  }
}
```

## 📋 Configuración Recomendada

### Para Uso Personal/Familiar (Alta Seguridad)

```bash
# .env o docker-compose.yml
REGISTRATION_ENABLED=false         # Cerrar después de crear usuarios
REGISTER_MAX_ATTEMPTS=3            # Solo 3 intentos por hora
REGISTER_WINDOW_MINUTES=60         # 1 hora de bloqueo
LOGIN_MAX_ATTEMPTS=5               # 5 intentos de login
LOGIN_WINDOW_MINUTES=30            # 30 minutos de bloqueo
```

### Para Uso Comunitario (Seguridad Media)

```bash
REGISTRATION_ENABLED=true          # Registro abierto
REGISTER_MAX_ATTEMPTS=5            # 5 intentos por hora
REGISTER_WINDOW_MINUTES=60         # 1 hora de bloqueo
LOGIN_MAX_ATTEMPTS=10              # 10 intentos de login
LOGIN_WINDOW_MINUTES=15            # 15 minutos de bloqueo
```

## 🚀 Cómo Aplicar los Cambios

### Opción 1: Variables de Entorno

1. Edita el archivo `.env` en `backend/`:
   ```bash
   REGISTRATION_ENABLED=false
   REGISTER_MAX_ATTEMPTS=3
   ```

2. Reinicia el backend:
   ```bash
   docker compose restart backend
   ```

### Opción 2: Docker Compose (más permanente)

1. Edita `docker-compose.yml`:
   ```yaml
   backend:
     environment:
       - REGISTRATION_ENABLED=false
       - REGISTER_MAX_ATTEMPTS=3
       - REGISTER_WINDOW_MINUTES=60
   ```

2. Reinicia:
   ```bash
   docker compose up -d backend
   ```

## 🔒 Medidas Adicionales Recomendadas (Futuro)

Si necesitas más seguridad, considera:

1. **CAPTCHA**: Añadir Google reCAPTCHA en el registro
2. **Verificación por Email**: Requerir confirmar email antes de activar cuenta
3. **Código de Invitación**: Solo permitir registro con código secreto
4. **Lista Blanca de IPs**: Solo permitir registro desde IPs conocidas
5. **2FA (Autenticación de Dos Factores)**: Para login

## 📊 Monitoreo

Para ver intentos bloqueados, revisa los logs:

```bash
docker compose logs backend | grep "Too Many Requests"
docker compose logs backend | grep "429"
```

## ⚠️ Importante

- El rate limiting se basa en **dirección IP**
- Si usas un proxy o CDN, asegúrate de que la IP real del cliente se pase correctamente
- Los límites son **por IP**, no por usuario
- Un usuario malintencionado podría usar múltiples IPs (VPN, proxy), pero el rate limiting dificulta ataques masivos simples

## 🎯 Resumen

Con estas medidas implementadas:
- ✅ Máximo 5 registros por hora desde una IP (configurable)
- ✅ Contraseñas fuertes obligatorias
- ✅ Validación de nombres de usuario
- ✅ Posibilidad de cerrar el registro completamente
- ✅ Protección contra ataques de fuerza bruta en login
- ✅ Endpoint para verificar estado y límites

¡Tu aplicación está mucho más protegida contra abuso! 🛡️
