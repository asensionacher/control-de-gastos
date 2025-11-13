#!/bin/bash

# Script para regenerar la SECRET_KEY

echo "🔑 Regeneración de SECRET_KEY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "backend/.env" ]; then
    echo "⚠️  ADVERTENCIA: Ya existe un archivo backend/.env"
    echo "   Regenerar la SECRET_KEY invalidará todos los tokens JWT existentes."
    echo "   Los usuarios deberán iniciar sesión nuevamente."
    echo ""
    read -p "¿Deseas continuar? (s/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Operación cancelada."
        exit 0
    fi
    echo ""
fi

# Generar nueva SECRET_KEY
echo "🔐 Generando nueva SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || \
             python -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null)

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Error: No se pudo generar SECRET_KEY."
    echo "   Asegúrate de tener Python instalado."
    exit 1
fi

# Crear o actualizar archivo .env
cat > backend/.env << EOF
# Variables de entorno - Regenerado el $(date)
SECRET_KEY=$SECRET_KEY
EOF

echo "✅ SECRET_KEY regenerada exitosamente"
echo ""
echo "Nueva SECRET_KEY:"
echo "$SECRET_KEY"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "El archivo backend/.env ha sido actualizado."
echo ""
echo "Si estás usando Docker, reinicia los contenedores:"
echo "  docker-compose restart backend"
echo ""
echo "Si ejecutas manualmente, reinicia el servidor backend."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
