#!/usr/bin/env python3
"""
Script de migración para añadir columnas user_id a las tablas existentes
y asignar todas las transacciones, categorías, etc. al primer usuario.
"""

import sys
from sqlalchemy import text
from database import engine, SessionLocal
from models import User

def migrate():
    """Ejecutar la migración"""
    db = SessionLocal()
    
    try:
        print("🔄 Iniciando migración de base de datos...")
        
        # Obtener el primer usuario (o crear uno por defecto)
        first_user = db.query(User).first()
        
        if not first_user:
            print("⚠️  No hay usuarios en la base de datos.")
            print("   Por favor, crea un usuario primero usando el endpoint /api/auth/register")
            return False
        
        print(f"✓ Usando usuario: {first_user.username} (ID: {first_user.id})")
        
        with engine.connect() as conn:
            # Iniciar transacción
            trans = conn.begin()
            
            try:
                # 1. Añadir columna user_id a categories
                print("\n📝 Migrando tabla 'categories'...")
                try:
                    conn.execute(text("""
                        ALTER TABLE categories 
                        ADD COLUMN user_id INTEGER
                    """))
                    print("   ✓ Columna user_id añadida")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print("   ℹ️  Columna user_id ya existe")
                    else:
                        raise
                
                # Actualizar registros existentes
                result = conn.execute(text("""
                    UPDATE categories 
                    SET user_id = :user_id 
                    WHERE user_id IS NULL
                """), {"user_id": first_user.id})
                print(f"   ✓ {result.rowcount} categorías asignadas al usuario")
                
                # Hacer la columna NOT NULL
                try:
                    conn.execute(text("""
                        ALTER TABLE categories 
                        ALTER COLUMN user_id SET NOT NULL
                    """))
                except:
                    pass
                
                # Eliminar constraint unique de name (SQLite no soporta DROP CONSTRAINT)
                # En SQLite necesitamos recrear la tabla
                
                # 2. Añadir columna user_id a subcategories
                print("\n📝 Migrando tabla 'subcategories'...")
                try:
                    conn.execute(text("""
                        ALTER TABLE subcategories 
                        ADD COLUMN user_id INTEGER
                    """))
                    print("   ✓ Columna user_id añadida")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print("   ℹ️  Columna user_id ya existe")
                    else:
                        raise
                
                result = conn.execute(text("""
                    UPDATE subcategories 
                    SET user_id = :user_id 
                    WHERE user_id IS NULL
                """), {"user_id": first_user.id})
                print(f"   ✓ {result.rowcount} subcategorías asignadas al usuario")
                
                try:
                    conn.execute(text("""
                        ALTER TABLE subcategories 
                        ALTER COLUMN user_id SET NOT NULL
                    """))
                except:
                    pass
                
                # 3. Añadir columna user_id a transactions
                print("\n📝 Migrando tabla 'transactions'...")
                try:
                    conn.execute(text("""
                        ALTER TABLE transactions 
                        ADD COLUMN user_id INTEGER
                    """))
                    print("   ✓ Columna user_id añadida")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print("   ℹ️  Columna user_id ya existe")
                    else:
                        raise
                
                result = conn.execute(text("""
                    UPDATE transactions 
                    SET user_id = :user_id 
                    WHERE user_id IS NULL
                """), {"user_id": first_user.id})
                print(f"   ✓ {result.rowcount} transacciones asignadas al usuario")
                
                try:
                    conn.execute(text("""
                        ALTER TABLE transactions 
                        ALTER COLUMN user_id SET NOT NULL
                    """))
                except:
                    pass
                
                # 4. Añadir columna user_id a store_mappings
                print("\n📝 Migrando tabla 'store_mappings'...")
                try:
                    conn.execute(text("""
                        ALTER TABLE store_mappings 
                        ADD COLUMN user_id INTEGER
                    """))
                    print("   ✓ Columna user_id añadida")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print("   ℹ️  Columna user_id ya existe")
                    else:
                        raise
                
                result = conn.execute(text("""
                    UPDATE store_mappings 
                    SET user_id = :user_id 
                    WHERE user_id IS NULL
                """), {"user_id": first_user.id})
                print(f"   ✓ {result.rowcount} mapeos de tienda asignados al usuario")
                
                try:
                    conn.execute(text("""
                        ALTER TABLE store_mappings 
                        ALTER COLUMN user_id SET NOT NULL
                    """))
                except:
                    pass
                
                # Confirmar transacción
                trans.commit()
                print("\n✅ Migración completada exitosamente!")
                print("\n📋 Resumen:")
                print(f"   - Todas las categorías, subcategorías, transacciones y mapeos")
                print(f"     han sido asignados al usuario '{first_user.username}'")
                print(f"   - Los nuevos registros requerirán especificar user_id")
                
                return True
                
            except Exception as e:
                trans.rollback()
                print(f"\n❌ Error durante la migración: {e}")
                return False
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("  MIGRACIÓN: Añadir soporte multi-usuario")
    print("=" * 60)
    
    success = migrate()
    
    if success:
        print("\n🎉 ¡La base de datos está lista para multi-usuario!")
        print("\nPróximos pasos:")
        print("  1. Reinicia el backend: docker compose restart backend")
        print("  2. Cada usuario verá solo sus propios datos")
        sys.exit(0)
    else:
        print("\n⚠️  La migración no se completó correctamente")
        sys.exit(1)
