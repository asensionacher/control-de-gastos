#!/bin/bash

echo "🚀 Iniciando Control de Gastos..."
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Crear directorio de datos si no existe
mkdir -p data

# Configurar SECRET_KEY si no existe
if [ ! -f "backend/.env" ]; then
    echo "� Generando SECRET_KEY para autenticación..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || \
                 python -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null)
    
    if [ -z "$SECRET_KEY" ]; then
        echo "⚠️  No se pudo generar SECRET_KEY automáticamente."
        echo "   Creando con valor temporal..."
        SECRET_KEY="temp-key-$(date +%s)-change-in-production"
    fi
    
    cat > backend/.env << EOF
# Variables de entorno - Generado automáticamente por start.sh
SECRET_KEY=$SECRET_KEY
EOF
    echo "✅ SECRET_KEY configurada en backend/.env"
    echo ""
else
    echo "✅ Archivo backend/.env ya existe"
    echo ""
fi

echo "�📦 Construyendo contenedores..."
docker compose build

echo ""
echo "🔧 Iniciando servicios..."
docker compose up -d

echo ""
echo "✅ ¡Aplicación iniciada correctamente!"
echo ""
echo "🌐 Accede a: http://localhost:3000"
echo "📝 Primera vez: Ve a /register para crear tu usuario"
echo ""
echo "🔌 Backend API: http://localhost:8000"
echo "📚 Documentación API: http://localhost:8000/docs"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Para ver los logs: docker-compose logs -f"
echo "Para detener: docker-compose down"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
