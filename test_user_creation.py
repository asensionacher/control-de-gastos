#!/usr/bin/env python3
"""Script para probar la creación de usuarios directamente en la base de datos"""

import sys
sys.path.insert(0, './backend')

from backend.database import SessionLocal, engine, Base
from backend.models import User
from backend.auth import get_password_hash

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def create_test_user():
    db = SessionLocal()
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            print("❌ El usuario 'testuser' ya existe")
            print(f"   ID: {existing_user.id}")
            print(f"   Activo: {existing_user.is_active}")
            print(f"   Creado: {existing_user.created_at}")
            return
        
        # Intentar crear el hash de la contraseña
        print("🔐 Generando hash de contraseña...")
        try:
            hashed_password = get_password_hash("testpass123")
            print("✅ Hash generado correctamente")
        except Exception as e:
            print(f"❌ Error al generar hash: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return
        
        # Crear el usuario
        print("👤 Creando usuario en la base de datos...")
        new_user = User(
            username="testuser",
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ Usuario creado exitosamente!")
        print(f"   ID: {new_user.id}")
        print(f"   Username: {new_user.username}")
        print(f"   Activo: {new_user.is_active}")
        print(f"   Creado: {new_user.created_at}")
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA DE CREACIÓN DE USUARIOS")
    print("=" * 60)
    create_test_user()
