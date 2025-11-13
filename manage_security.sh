#!/bin/bash
# Script de utilidad para gestionar la seguridad del registro

COMPOSE_FILE="docker-compose.yml"

echo "======================================"
echo "  Control de Registro de Usuarios"
echo "======================================"
echo ""

# Función para verificar si el registro está habilitado
check_status() {
    echo "📊 Estado actual del registro:"
    curl -s http://localhost:8000/api/auth/registration-status | python3 -m json.tool
}

# Función para deshabilitar el registro
disable_registration() {
    echo "🔒 Deshabilitando el registro de nuevos usuarios..."
    
    # Verificar si ya está deshabilitado en docker-compose.yml
    if grep -q "REGISTRATION_ENABLED=false" "$COMPOSE_FILE" 2>/dev/null; then
        echo "   ℹ️  El registro ya está deshabilitado en docker-compose.yml"
    else
        # Descomentar o añadir la línea
        if grep -q "# - REGISTRATION_ENABLED=false" "$COMPOSE_FILE" 2>/dev/null; then
            sed -i 's/# - REGISTRATION_ENABLED=false/- REGISTRATION_ENABLED=false/' "$COMPOSE_FILE"
            echo "   ✓ Línea descomentada en docker-compose.yml"
        else
            # Buscar la sección environment del backend y añadir la línea
            echo "   ⚠️  Por favor, añade manualmente esta línea en docker-compose.yml:"
            echo "      - REGISTRATION_ENABLED=false"
        fi
    fi
    
    # Reiniciar el backend
    echo "   🔄 Reiniciando backend..."
    docker compose restart backend
    
    echo "   ✅ Registro deshabilitado. Verificando..."
    sleep 3
    check_status
}

# Función para habilitar el registro
enable_registration() {
    echo "🔓 Habilitando el registro de nuevos usuarios..."
    
    # Comentar la línea en docker-compose.yml
    if grep -q "- REGISTRATION_ENABLED=false" "$COMPOSE_FILE" 2>/dev/null; then
        sed -i 's/- REGISTRATION_ENABLED=false/# - REGISTRATION_ENABLED=false/' "$COMPOSE_FILE"
        echo "   ✓ Línea comentada en docker-compose.yml"
    fi
    
    # Reiniciar el backend
    echo "   🔄 Reiniciando backend..."
    docker compose restart backend
    
    echo "   ✅ Registro habilitado. Verificando..."
    sleep 3
    check_status
}

# Función para ajustar límites de rate
adjust_limits() {
    echo "⚙️  Configuración actual de límites:"
    echo ""
    grep -A 5 "Rate limiting" "$COMPOSE_FILE" 2>/dev/null || echo "No configurado explícitamente (usando valores por defecto)"
    echo ""
    echo "Valores por defecto:"
    echo "  - REGISTER_MAX_ATTEMPTS=5"
    echo "  - REGISTER_WINDOW_MINUTES=60"
    echo "  - LOGIN_MAX_ATTEMPTS=10"
    echo "  - LOGIN_WINDOW_MINUTES=15"
    echo ""
    echo "Para cambiar los límites, edita docker-compose.yml y descomenta/modifica las líneas correspondientes."
}

# Menú principal
show_menu() {
    echo ""
    echo "¿Qué deseas hacer?"
    echo ""
    echo "  1) Ver estado actual"
    echo "  2) Deshabilitar registro de usuarios"
    echo "  3) Habilitar registro de usuarios"
    echo "  4) Ver/Ajustar límites de rate limiting"
    echo "  5) Salir"
    echo ""
    read -p "Opción: " option
    
    case $option in
        1)
            check_status
            show_menu
            ;;
        2)
            disable_registration
            show_menu
            ;;
        3)
            enable_registration
            show_menu
            ;;
        4)
            adjust_limits
            show_menu
            ;;
        5)
            echo "👋 ¡Hasta luego!"
            exit 0
            ;;
        *)
            echo "❌ Opción inválida"
            show_menu
            ;;
    esac
}

# Verificar que estamos en el directorio correcto
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Error: No se encontró $COMPOSE_FILE"
    echo "   Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Ejecutar menú
show_menu
