"""Bank file format detector"""
from typing import Optional, Tuple
import chardet
from io import BytesIO
import re


class BankDetector:
    """Detecta automáticamente el tipo de banco basándose en el contenido del archivo"""
    
    @staticmethod
    def detect_encoding(file_content: bytes) -> str:
        """Detectar la codificación del archivo"""
        result = chardet.detect(file_content)
        return result['encoding'] or 'utf-8'
    
    @staticmethod
    def is_html_file(file_content: bytes) -> bool:
        """Verificar si el archivo es HTML (Openbank usa HTML con extensión .xls)"""
        try:
            # Buscar los primeros 1000 bytes
            sample = file_content[:1000].lower()
            return b'<!doctype html' in sample or b'<html' in sample
        except:
            return False
    
    @staticmethod
    def is_binary_xls(file_content: bytes) -> bool:
        """Verificar si es un archivo XLS binario (formato antiguo Excel)"""
        # Los archivos XLS binarios comienzan con la firma de OLE2
        return file_content[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    
    @staticmethod
    def is_xlsx(file_content: bytes) -> bool:
        """Verificar si es un archivo XLSX (formato moderno Excel)"""
        # Los archivos XLSX son archivos ZIP que comienzan con PK
        return file_content[:2] == b'PK'
    
    @staticmethod
    def detect_openbank(file_content: bytes) -> bool:
        """Detectar si el archivo es de Openbank"""
        try:
            # Openbank usa HTML con extensión .xls
            if BankDetector.is_html_file(file_content):
                content_sample = file_content[:5000].lower()
                # Buscar patrones específicos de Openbank
                return (b'openbank' in content_sample or 
                        b'open bank' in content_sample or
                        b'cuenta corriente open' in content_sample or
                        (b'fecha operaci' in content_sample and 
                         b'fecha valor' in content_sample and
                         b'concepto' in content_sample))
            return False
        except:
            return False
    
    @staticmethod
    def detect_kutxabank(file_content: bytes) -> Tuple[bool, Optional[str]]:
        """Detectar si el archivo es de Kutxabank y su tipo (cuenta o tarjeta)"""
        try:
            # Verificar si es XLS (binario antiguo) o XLSX (moderno)
            is_xls = BankDetector.is_binary_xls(file_content)
            is_xlsx_file = BankDetector.is_xlsx(file_content)
            
            if is_xls or is_xlsx_file:
                # Es un archivo Excel, probablemente Kutxabank
                # Intentar leer con pandas para ver el contenido
                import pandas as pd
                try:
                    # Intentar con el engine apropiado
                    if is_xls:
                        df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
                    else:
                        df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
                    
                    # Convertir todo a string para buscar patrones
                    content_str = ' '.join([
                        ' '.join([str(val) for val in row if pd.notna(val)])
                        for _, row in df.iterrows()
                    ]).lower()
                    
                    # Detectar si es tarjeta o cuenta basándose en palabras clave
                    # La tarjeta tiene "movimientos de tarjetas" o "información de movimientos de tarjetas"
                    # La cuenta tiene "movimientos de cuenta"
                    if 'movimientos de tarjetas' in content_str or 'información de movimientos de tarjetas' in content_str:
                        return True, 'kutxabank_card'
                    elif 'movimientos de cuenta' in content_str:
                        return True, 'kutxabank_account'
                    # Si tiene "saldo" es más probable que sea cuenta (las tarjetas no suelen tener saldo)
                    elif 'saldo' in content_str and 'importe' in content_str:
                        return True, 'kutxabank_account'
                    # Si solo tiene "importe de la operación" sin "saldo", probablemente es tarjeta
                    elif 'importe de la operación' in content_str or 'importe de la operacion' in content_str:
                        return True, 'kutxabank_card'
                    else:
                        # Por defecto, si no se puede determinar, asumir cuenta
                        return True, 'kutxabank_account'
                except Exception as e:
                    print(f"Error reading Kutxabank file: {e}")
                    # Si no se puede leer, asumir cuenta por defecto
                    return True, 'kutxabank_account'
            return False, None
        except:
            return False, None
    
    @staticmethod
    def detect_imaginbank(file_content: bytes) -> bool:
        """Detectar si el archivo es de Imaginbank"""
        try:
            encoding = BankDetector.detect_encoding(file_content)
            # Imaginbank es CSV, intentar decodificar
            content = file_content.decode(encoding, errors='ignore')
            
            # Buscar patrones típicos de Imaginbank
            # Los archivos incluyen "EUR" en los importes
            lines = content.split('\n')[:5]  # Primeras 5 líneas
            
            # Verificar si hay EUR en los valores
            has_eur = any('EUR' in line for line in lines)
            
            # Verificar estructura: Concepto;Fecha;Importe;Saldo
            if lines and ';' in lines[0]:
                headers = lines[0].lower().split(';')
                # Imaginbank usa: Concepto, Fecha, Importe, Saldo
                if (any('concepto' in h for h in headers) and
                    any('fecha' in h for h in headers) and
                    any('importe' in h for h in headers) and
                    has_eur):
                    return True
            
            return False
        except:
            return False
    
    @staticmethod
    def detect_bbva(file_content: bytes) -> bool:
        """Detectar si el archivo es de BBVA"""
        try:
            # BBVA usa archivos Excel (.xlsx principalmente)
            is_xls = BankDetector.is_binary_xls(file_content)
            is_xlsx_file = BankDetector.is_xlsx(file_content)
            
            if is_xls or is_xlsx_file:
                import pandas as pd
                try:
                    # Leer el archivo
                    if is_xlsx_file:
                        df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
                    else:
                        df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
                    
                    # Convertir a string para buscar patrones
                    content_str = ' '.join([
                        ' '.join([str(val) for val in row if pd.notna(val)])
                        for _, row in df.iterrows()
                    ]).lower()
                    
                    # Patrones específicos de BBVA:
                    # - Tienen "Últimos movimientos" en el encabezado
                    # - Columnas: F.Valor, Fecha, Concepto, Movimiento, Importe, Divisa, Disponible
                    if ('últimos movimientos' in content_str or 'ultimos movimientos' in content_str or
                        ('f.valor' in content_str and 'disponible' in content_str) or
                        ('bbva' in content_str)):
                        return True
                    
                    return False
                except:
                    return False
            return False
        except:
            return False
    
    @staticmethod
    def detect_ing(file_content: bytes) -> bool:
        """Detectar si el archivo es de ING Direct"""
        try:
            # ING usa archivos Excel (.xls principalmente)
            is_xls = BankDetector.is_binary_xls(file_content)
            is_xlsx_file = BankDetector.is_xlsx(file_content)
            
            if is_xls or is_xlsx_file:
                import pandas as pd
                try:
                    # Leer el archivo
                    if is_xls:
                        df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
                    else:
                        df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
                    
                    # Convertir a string para buscar patrones
                    content_str = ' '.join([
                        ' '.join([str(val) for val in row if pd.notna(val)])
                        for _, row in df.iterrows()
                    ]).lower()
                    
                    # Patrones específicos de ING:
                    # - "Movimientos de la Cuenta" en el título
                    # - Columnas: F. VALOR, CATEGORÍA, SUBCATEGORÍA, DESCRIPCIÓN, IMPORTE (€), SALDO (€)
                    # - "Ventajas ING" como categoría típica
                    if ('movimientos de la cuenta' in content_str or
                        'ventajas ing' in content_str or
                        ('f. valor' in content_str and 'categoría' in content_str and 'subcategoría' in content_str) or
                        ('f. valor' in content_str and 'categoria' in content_str and 'subcategoria' in content_str)):
                        return True
                    
                    return False
                except:
                    return False
            return False
        except:
            return False
    
    @staticmethod
    def detect_bank_type(file_content: bytes, filename: str = "") -> Optional[str]:
        """
        Detecta automáticamente el tipo de banco basándose en el contenido del archivo.
        
        Returns:
            str: El tipo de banco ('openbank', 'kutxabank_account', 'kutxabank_card', 'imaginbank', 'bbva', 'ing')
            None: Si no se puede detectar
        """
        # 1. Verificar Openbank (HTML disfrazado como XLS)
        if BankDetector.detect_openbank(file_content):
            return 'openbank'
        
        # 2. Verificar BBVA (Excel con "Últimos movimientos")
        if BankDetector.detect_bbva(file_content):
            return 'bbva'
        
        # 3. Verificar ING Direct (Excel con "Movimientos de la Cuenta")
        if BankDetector.detect_ing(file_content):
            return 'ing'
        
        # 4. Verificar Kutxabank (XLS binario)
        is_kutxa, kutxa_type = BankDetector.detect_kutxabank(file_content)
        if is_kutxa:
            return kutxa_type
        
        # 5. Verificar Imaginbank (CSV con EUR)
        if BankDetector.detect_imaginbank(file_content):
            return 'imaginbank'
        
        # 6. Si no se detecta, intentar por extensión del archivo
        if filename:
            filename_lower = filename.lower()
            if 'bbva' in filename_lower:
                return 'bbva'
            elif 'ing' in filename_lower:
                return 'ing'
            elif 'openbank' in filename_lower:
                return 'openbank'
            elif 'kutxabank' in filename_lower or 'kutxa' in filename_lower:
                if 'tarjeta' in filename_lower or 'card' in filename_lower:
                    return 'kutxabank_card'
                else:
                    return 'kutxabank_account'
            elif 'imaginbank' in filename_lower or 'imagin' in filename_lower:
                return 'imaginbank'
        
        return None
    
    @staticmethod
    def get_available_banks() -> list:
        """Retorna la lista de bancos soportados"""
        return [
            {'value': 'kutxabank_account', 'label': 'Kutxabank - Cuenta Corriente'},
            {'value': 'kutxabank_card', 'label': 'Kutxabank - Tarjeta de Crédito'},
            {'value': 'openbank', 'label': 'Openbank'},
            {'value': 'imaginbank', 'label': 'Imaginbank'},
            {'value': 'bbva', 'label': 'BBVA'},
            {'value': 'ing', 'label': 'ING Direct'}
        ]
