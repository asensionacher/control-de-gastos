# Sistema de Autenticación - Control de Gastos

## Cambios Implementados

### Backend

#### 1. Nuevas Dependencias (`requirements.txt`)
- `python-jose[cryptography]==3.3.0` - Para crear y verificar tokens JWT
- `passlib[bcrypt]==1.7.4` - Para hashear contraseñas de forma segura

#### 2. Modelo de Usuario (`models.py`)
- Nueva tabla `users` con:
  - `username` (único)
  - `hashed_password`
  - `is_active`
  - Timestamps de creación y actualización

#### 3. Schemas de Autenticación (`schemas.py`)
- `UserCreate` - Para registro de usuarios
- `UserLogin` - Para inicio de sesión
- `User` - Datos del usuario
- `Token` - Respuesta con token JWT
- `TokenData` - Datos contenidos en el token

#### 4. Módulo de Autenticación (`auth.py`)
- `verify_password()` - Verifica contraseñas
- `get_password_hash()` - Genera hash de contraseñas
- `create_access_token()` - Crea tokens JWT (válidos 30 días)
- `authenticate_user()` - Autentica usuario con credenciales
- `get_current_user()` - Obtiene usuario desde token JWT
- `get_current_active_user()` - Verifica que el usuario esté activo

**IMPORTANTE**: La clave secreta en `auth.py` debe cambiarse en producción.

#### 5. Rutas de Autenticación (`routes/auth.py`)
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión (devuelve token)
- `GET /api/auth/me` - Obtener información del usuario actual

#### 6. Protección de Rutas Existentes
Todas las rutas existentes ahora requieren autenticación:
- `/api/transactions/*`
- `/api/categories/*`
- `/api/upload/*`
- `/api/reports/*`

Se añadió `current_user: User = Depends(get_current_active_user)` a todas las funciones.

#### 7. Actualización de `main.py`
- Registrado el router de autenticación en `/api/auth`

### Frontend

#### 1. Actualización de `api.js`
- **Interceptor de Request**: Añade automáticamente el token JWT a todas las peticiones
- **Interceptor de Response**: Maneja errores 401 (no autorizado) redirigiendo al login
- Nuevas funciones:
  - `register(username, password)`
  - `login(username, password)`
  - `getCurrentUser()`

#### 2. Página de Login (`pages/Login.js`)
- Formulario de inicio de sesión
- Guarda token y username en localStorage
- Redirección automática después del login

#### 3. Página de Registro (`pages/Register.js`)
- Formulario de registro de usuario
- Validación de contraseñas (mínimo 6 caracteres, coincidencia)
- Redirección al login después del registro

#### 4. Actualización de `App.js`
- Componente `PrivateRoute` para proteger rutas
- Componente `Navigation` con botón de logout y nombre de usuario
- Rutas públicas: `/login` y `/register`
- Rutas protegidas: todas las demás

## Cómo Usar

### 1. Configurar SECRET_KEY (IMPORTANTE)
```bash
cd backend
python generate_secret_key.py
# Copia la clave generada
cp .env.example .env
# Edita .env y añade: SECRET_KEY=tu-clave-generada
```

### 2. Instalar Dependencias del Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Crear la Base de Datos
Al ejecutar el backend, se creará automáticamente la tabla `users`:
```bash
python main.py
```

### 4. Primer Usuario
1. Accede a `http://localhost:3000/register`
2. Crea un usuario con username y contraseña
3. Inicia sesión en `http://localhost:3000/login`

### 5. Flujo de Autenticación
1. El usuario se registra o inicia sesión
2. El backend devuelve un token JWT
3. El token se guarda en localStorage
4. Todas las peticiones incluyen el token en el header `Authorization: Bearer <token>`
5. El token es válido por 30 días
6. Si el token expira o es inválido, se redirige al login

## Seguridad

### Configuración de SECRET_KEY

La `SECRET_KEY` se obtiene automáticamente de las variables de entorno. Para configurarla:

**1. Generar una clave segura:**
```bash
cd backend
python generate_secret_key.py
```

**2. Crear archivo `.env` en el directorio `backend/`:**
```bash
cp .env.example .env
```

**3. Editar `.env` y añadir tu SECRET_KEY:**
```bash
SECRET_KEY=tu-clave-generada-aqui
```

**Nota para desarrollo:** Si no configuras la SECRET_KEY, el sistema generará una clave temporal automáticamente (verás un warning en la consola). Esta clave cambiará cada vez que reinicies el servidor, invalidando todos los tokens existentes.

**Nota para producción:** La SECRET_KEY es OBLIGATORIA. Configúrala como variable de entorno o en el archivo `.env`.

### Recomendaciones Adicionales
- Usar HTTPS en producción
- Configurar CORS apropiadamente para tu dominio
- Considerar implementar refresh tokens
- Añadir rate limiting para endpoints de autenticación
- Implementar logs de intentos de login fallidos

## API Endpoints

### Autenticación (Público)
- `POST /api/auth/register` - Registro
- `POST /api/auth/login` - Login

### Autenticados (Requieren Token)
- `GET /api/auth/me` - Info del usuario
- Todos los endpoints de `/api/transactions/*`
- Todos los endpoints de `/api/categories/*`
- Todos los endpoints de `/api/upload/*`
- Todos los endpoints de `/api/reports/*`
