#!/usr/bin/env python3
import pandas as pd
from io import BytesIO

# Leer el archivo
with open('movimientos.xls', 'rb') as f:
    content = f.read()

print(f'Tamaño del archivo: {len(content)} bytes')

# Intentar con xlrd primero
try:
    df = pd.read_excel(BytesIO(content), engine='xlrd', header=None)
    engine = 'xlrd'
except Exception as e:
    print(f'xlrd falló: {e}')
    try:
        df = pd.read_excel(BytesIO(content), engine='openpyxl', header=None)
        engine = 'openpyxl'
    except Exception as e2:
        print(f'openpyxl también falló: {e2}')
        exit(1)

print(f'Motor usado: {engine}')
print(f'Total de filas: {len(df)}')
print(f'Total de columnas: {len(df.columns)}')

# Mostrar todas las filas para análisis
print(f'\n=== TODAS LAS FILAS ===')
for idx, row in df.iterrows():
    row_values = [str(val) if pd.notna(val) else '' for val in row]
    print(f'Fila {idx}: {row_values[:6]}')

# Buscar el header
header_row = None
for idx, row in df.iterrows():
    row_str = ' '.join([str(val).lower() for val in row if pd.notna(val)])
    if 'fecha' in row_str and ('concepto' in row_str or 'importe' in row_str):
        header_row = idx
        print(f'\n=== Header encontrado en fila {idx} ===')
        print(f'Contenido: {row.tolist()}')
        break

if header_row is not None:
    # Contar filas con datos válidos
    valid_rows = 0
    print(f'\n=== Filas de datos ===')
    for idx in range(header_row + 2, len(df)):
        first_cell = df.iloc[idx, 0]
        if pd.notna(first_cell):
            valid_rows += 1
            print(f'Fila {idx}: {first_cell}')
    
    print(f'\n=== TOTAL filas con datos: {valid_rows} ===')
