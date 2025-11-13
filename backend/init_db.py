#!/usr/bin/env python3
"""
Script para inicializar las tablas de la base de datos
Funciona tanto con SQLite como con PostgreSQL
"""

import sys
import os

# Añadir el directorio actual al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from models import User, Category, Subcategory, Transaction, StoreMapping

def init_db():
    """Crear todas las tablas en la base de datos"""
    try:
        print("🔧 Inicializando base de datos...")
        print(f"📍 Conectando a: {engine.url}")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tablas creadas exitosamente!")
        print("\n📋 Tablas disponibles:")
        for table in Base.metadata.sorted_tables:
            print(f"   - {table.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Inicialización de Base de Datos")
    print("=" * 60)
    print()
    
    success = init_db()
    
    if success:
        print("\n✨ Base de datos lista para usar!")
        print("\nPróximos pasos:")
        print("  1. Inicia el servidor: uvicorn main:app --reload")
        print("  2. Registra tu primer usuario en: /register")
        sys.exit(0)
    else:
        print("\n⚠️  La inicialización falló")
        sys.exit(1)
