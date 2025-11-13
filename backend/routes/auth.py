from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import User
import schemas
from auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from rate_limiter import rate_limiter
import os

router = APIRouter()

# Variable de entorno para controlar si el registro está habilitado
REGISTRATION_ENABLED = os.getenv("REGISTRATION_ENABLED", "true").lower() == "true"

# Límites de rate limiting para registro
REGISTER_MAX_ATTEMPTS = int(os.getenv("REGISTER_MAX_ATTEMPTS", "5"))  # 5 intentos
REGISTER_WINDOW_MINUTES = int(os.getenv("REGISTER_WINDOW_MINUTES", "60"))  # por hora

# Límites de rate limiting para login
LOGIN_MAX_ATTEMPTS = int(os.getenv("LOGIN_MAX_ATTEMPTS", "10"))  # 10 intentos
LOGIN_WINDOW_MINUTES = int(os.getenv("LOGIN_WINDOW_MINUTES", "15"))  # por 15 minutos

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: schemas.UserCreate, 
    request: Request,
    db: Session = Depends(get_db)
):
    """Registra un nuevo usuario"""
    
    # Verificar si el registro está habilitado
    if not REGISTRATION_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El registro de nuevos usuarios está deshabilitado. Contacta al administrador."
        )
    
    # Verificar rate limit
    rate_limiter.check_rate_limit(
        request=request,
        endpoint="register",
        max_requests=REGISTER_MAX_ATTEMPTS,
        window_minutes=REGISTER_WINDOW_MINUTES
    )
    # Verificar si el usuario ya existe
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    
    # Crear el nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=schemas.Token)
async def login(
    user_credentials: schemas.UserLogin, 
    request: Request,
    db: Session = Depends(get_db)
):
    """Inicia sesión y devuelve un token JWT"""
    
    # Verificar rate limit para login
    rate_limiter.check_rate_limit(
        request=request,
        endpoint="login",
        max_requests=LOGIN_MAX_ATTEMPTS,
        window_minutes=LOGIN_WINDOW_MINUTES
    )
    
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Crear el token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Obtiene la información del usuario actual"""
    return current_user

@router.get("/registration-status")
async def registration_status(request: Request):
    """Obtiene el estado del registro y límites de rate"""
    
    # Obtener intentos restantes de registro
    remaining_register, reset_register = rate_limiter.get_remaining_attempts(
        request=request,
        endpoint="register",
        max_requests=REGISTER_MAX_ATTEMPTS,
        window_minutes=REGISTER_WINDOW_MINUTES
    )
    
    # Obtener intentos restantes de login
    remaining_login, reset_login = rate_limiter.get_remaining_attempts(
        request=request,
        endpoint="login",
        max_requests=LOGIN_MAX_ATTEMPTS,
        window_minutes=LOGIN_WINDOW_MINUTES
    )
    
    return {
        "registration_enabled": REGISTRATION_ENABLED,
        "rate_limits": {
            "register": {
                "max_attempts": REGISTER_MAX_ATTEMPTS,
                "window_minutes": REGISTER_WINDOW_MINUTES,
                "remaining_attempts": remaining_register,
                "reset_time": reset_register.isoformat() if remaining_register == 0 else None
            },
            "login": {
                "max_attempts": LOGIN_MAX_ATTEMPTS,
                "window_minutes": LOGIN_WINDOW_MINUTES,
                "remaining_attempts": remaining_login,
                "reset_time": reset_login.isoformat() if remaining_login == 0 else None
            }
        },
        "password_requirements": {
            "min_length": 8,
            "max_length": 100,
            "requires_lowercase": True,
            "requires_uppercase": True,
            "requires_number": True,
            "requires_special": False
        }
    }
