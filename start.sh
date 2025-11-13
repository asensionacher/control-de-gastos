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

echo "📦 Construyendo contenedores..."
docker-compose build

echo ""
echo "🔧 Iniciando servicios..."
docker-compose up -d

echo ""
echo "✅ ¡Aplicación iniciada correctamente!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 Documentación API: http://localhost:8000/docs"
echo ""
echo "Para ver los logs: docker-compose logs -f"
echo "Para detener: docker-compose down"
