#!/bin/bash

echo "Probando endpoint de registro..."
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
echo ""
