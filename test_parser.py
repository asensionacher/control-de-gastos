#!/usr/bin/env python3
import sys
sys.path.append('/app')

from parsers import KutxabankAccountParser

# Leer el archivo
with open('movimientos.xls', 'rb') as f:
    content = f.read()

parser = KutxabankAccountParser()
transactions = parser.parse(content)

print(f'Total de transacciones parseadas: {len(transactions)}')
print(f'\nTransacciones parseadas:')
for i, trans in enumerate(transactions, 1):
    print(f"{i}. {trans['date'].strftime('%d/%m/%Y')} - {trans['description'][:40]} - {trans['amount']}")

print(f'\n=== RESUMEN ===')
print(f'Esperadas: 38')
print(f'Importadas: {len(transactions)}')
print(f'Faltantes: {38 - len(transactions)}')
