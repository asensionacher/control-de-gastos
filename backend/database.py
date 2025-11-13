import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Soportar tanto SQLite como PostgreSQL
# Prioridad: DATABASE_URL > SQLite con DATABASE_PATH
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Por defecto usar SQLite
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/control_gastos.db")
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configurar engine según el tipo de base de datos
if DATABASE_URL.startswith("sqlite"):
    # SQLite necesita check_same_thread=False para FastAPI
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    print(f"📁 Using SQLite database: {DATABASE_URL}")
else:
    # PostgreSQL, MySQL u otras bases de datos
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verificar conexión antes de usar
        pool_recycle=3600,   # Reciclar conexiones cada hora
    )
    # Ocultar password en el log
    safe_url = DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL
    print(f"🐘 Using PostgreSQL database: ...@{safe_url}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
