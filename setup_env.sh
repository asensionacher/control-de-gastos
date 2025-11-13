#!/bin/bash

# Script para configurar el entorno por primera vez

echo "============================================================"
echo "Configuración inicial - Control de Gastos"
echo "============================================================"
echo ""

# Verificar si ya existe el archivo .env
if [ -f "backend/.env" ]; then
    echo "⚠️  El archivo backend/.env ya existe."
    read -p "¿Deseas sobrescribirlo? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Operación cancelada."
        exit 0
    fi
fi

# Generar SECRET_KEY
echo "🔑 Generando SECRET_KEY segura..."
cd backend
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Crear archivo .env
cat > .env << EOF
# Variables de entorno para el backend

# SEGURIDAD - Clave secreta para JWT
SECRET_KEY=$SECRET_KEY

# Base de datos (si usas PostgreSQL u otra BD en el futuro)
# DATABASE_URL=postgresql://user:password@localhost/dbname

# Configuración de CORS (añade tus dominios en producción)
# ALLOWED_ORIGINS=http://localhost:3000,https://tudominio.com
EOF

echo "✅ Archivo backend/.env creado con SECRET_KEY segura"
echo ""
echo "SECRET_KEY generada:"
echo "$SECRET_KEY"
echo ""
echo "============================================================"
echo "✨ Configuración completada"
echo "============================================================"
echo ""
echo "Próximos pasos:"
echo "1. Instalar dependencias: pip install -r requirements.txt"
echo "2. Iniciar backend: uvicorn main:app --reload"
echo "3. Iniciar frontend: cd ../frontend && npm start"
echo "4. Acceder a http://localhost:3000/register"
echo ""
