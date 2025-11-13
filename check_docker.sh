#!/bin/bash

echo "Verificando estado de Docker..."
docker ps

echo ""
echo "Logs del backend:"
docker logs control-gastos-backend --tail 50
