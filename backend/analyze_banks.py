import pandas as pd
import sys

# Analizar BBVA
print("="*60)
print("ANÁLISIS ARCHIVO BBVA")
print("="*60)
try:
    # Leer sin encabezado para ver la estructura real
    df_bbva = pd.read_excel('../examples/bbva_ejemplo.xlsx', header=None)
    print(f"\nTotal de filas: {len(df_bbva)}")
    print(f"\nTodas las filas:")
    print(df_bbva.to_string())
    
    # Buscar la fila de encabezados
    for idx, row in df_bbva.iterrows():
        if 'F.Valor' in str(row.values):
            print(f"\n✓ Fila de encabezados encontrada en índice: {idx}")
            print(f"Encabezados: {row.tolist()}")
            break
            
except Exception as e:
    print(f"Error al leer BBVA: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("ANÁLISIS ARCHIVO ING")
print("="*60)
try:
    # Leer sin encabezado
    df_ing = pd.read_excel('../examples/ing_ejemplo.xls', header=None)
    print(f"\nTotal de filas: {len(df_ing)}")
    print(f"\nTodas las filas:")
    print(df_ing.to_string())
    
    # Buscar la fila de encabezados
    for idx, row in df_ing.iterrows():
        if 'F. VALOR' in str(row.values).upper() or 'FECHA' in str(row.values).upper():
            print(f"\n✓ Fila de encabezados encontrada en índice: {idx}")
            print(f"Encabezados: {row.tolist()}")
            break
            
except Exception as e:
    print(f"Error al leer ING: {e}")
    import traceback
    traceback.print_exc()

