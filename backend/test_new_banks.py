#!/usr/bin/env python3
"""Script para probar los parsers de BBVA e ING Direct"""

import sys
sys.path.append('/app')

from parsers import BBVAParser, INGParser
from bank_detector import BankDetector

def test_bbva():
    print("="*60)
    print("PROBANDO PARSER DE BBVA")
    print("="*60)
    
    try:
        with open('../examples/bbva_ejemplo.xlsx', 'rb') as f:
            content = f.read()
        
        # Probar detección
        detected = BankDetector.detect_bank_type(content, 'bbva_ejemplo.xlsx')
        print(f"\n✓ Banco detectado: {detected}")
        
        # Probar parser
        parser = BBVAParser()
        transactions = parser.parse(content)
        
        print(f"\n✓ Transacciones parseadas: {len(transactions)}")
        
        if transactions:
            print("\n📋 Primera transacción:")
            first = transactions[0]
            for key, value in first.items():
                print(f"  {key}: {value}")
            
            print("\n📋 Todas las transacciones:")
            for i, trans in enumerate(transactions, 1):
                print(f"\n  {i}. {trans['date'].strftime('%Y-%m-%d')} | {trans['description'][:50]} | {trans['amount']} € | Saldo: {trans.get('balance', 'N/A')}")
        
        print(f"\n✅ BBVA: Test completado exitosamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en BBVA: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ing():
    print("\n" + "="*60)
    print("PROBANDO PARSER DE ING DIRECT")
    print("="*60)
    
    try:
        with open('../examples/ing_ejemplo.xls', 'rb') as f:
            content = f.read()
        
        # Probar detección
        detected = BankDetector.detect_bank_type(content, 'ing_ejemplo.xls')
        print(f"\n✓ Banco detectado: {detected}")
        
        # Probar parser
        parser = INGParser()
        transactions = parser.parse(content)
        
        print(f"\n✓ Transacciones parseadas: {len(transactions)}")
        
        if transactions:
            print("\n📋 Primera transacción:")
            first = transactions[0]
            for key, value in first.items():
                print(f"  {key}: {value}")
            
            print("\n📋 Todas las transacciones:")
            for i, trans in enumerate(transactions, 1):
                extra = f" | {trans['extra_info']}" if trans.get('extra_info') else ''
                print(f"\n  {i}. {trans['date'].strftime('%Y-%m-%d')} | {trans['description'][:50]} | {trans['amount']} € | Saldo: {trans.get('balance', 'N/A')}{extra}")
        
        print(f"\n✅ ING: Test completado exitosamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en ING: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    bbva_ok = test_bbva()
    ing_ok = test_ing()
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"BBVA: {'✅ OK' if bbva_ok else '❌ ERROR'}")
    print(f"ING:  {'✅ OK' if ing_ok else '❌ ERROR'}")
    
    if bbva_ok and ing_ok:
        print("\n🎉 Todos los tests pasaron correctamente!")
        sys.exit(0)
    else:
        print("\n⚠️  Algunos tests fallaron")
        sys.exit(1)
