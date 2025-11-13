import pandas as pd
import hashlib
from datetime import datetime
from typing import List, Dict, Any
from abc import ABC, abstractmethod
import chardet
from io import BytesIO
from lxml import html
import re

class BaseParser(ABC):
    """Clase base para parsers de CSV de bancos"""
    
    @abstractmethod
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        """Parsear el contenido del CSV y devolver lista de transacciones"""
        pass
    
    def detect_encoding(self, file_content: bytes) -> str:
        """Detectar la codificación del archivo"""
        result = chardet.detect(file_content)
        return result['encoding'] or 'utf-8'
    
    def generate_hash(self, date: datetime, description: str, amount: float, bank_type: str) -> str:
        """Generar hash único para detectar duplicados"""
        hash_string = f"{date.isoformat()}{description}{amount}{bank_type}"
        return hashlib.sha256(hash_string.encode()).hexdigest()

class KutxabankAccountParser(BaseParser):
    """Parser para extractos de cuenta corriente de Kutxabank"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        try:
            # Kutxabank cuenta es un archivo XLS/XLSX binario
            # Intentar primero con xlrd (archivos .xls antiguos)
            # Si falla, intentar con openpyxl (archivos .xlsx modernos)
            try:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
            
            # Buscar la fila con los encabezados (fecha, concepto, etc.)
            header_row = None
            for idx, row in df.iterrows():
                row_str = ' '.join([str(val).lower() for val in row if pd.notna(val)])
                if 'fecha' in row_str and 'concepto' in row_str and 'importe' in row_str:
                    header_row = idx
                    break
            
            if header_row is None:
                raise ValueError("No se encontró la fila de encabezados en el archivo de Kutxabank")
            
            # Leer de nuevo sin skiprows, usando el header_row como header
            # pandas automáticamente usará esa fila como nombres de columnas
            try:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=header_row)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=header_row)
            
            # Limpiar: remover filas vacías
            df = df.dropna(how='all')
            
            # Resetear el índice después de limpiar
            df = df.reset_index(drop=True)
            
            transactions = []
            
            # Formato Kutxabank: fecha, concepto, fecha valor, importe, saldo
            for _, row in df.iterrows():
                try:
                    # Saltar filas con NaN en la primera columna (fecha)
                    if pd.isna(row.iloc[0]):
                        continue
                    
                    # La primera columna suele ser la fecha
                    date_val = row.iloc[0]
                    
                    # Si es string, parsear
                    if isinstance(date_val, str):
                        date = pd.to_datetime(date_val, format='%d/%m/%Y', errors='coerce')
                    else:
                        # Si ya es datetime
                        date = pd.to_datetime(date_val, errors='coerce')
                    
                    if pd.isna(date):
                        continue
                    
                    # Segunda columna: concepto/descripción
                    description = str(row.iloc[1]).strip()
                    if description == 'nan' or not description:
                        continue
                    
                    # Buscar la columna de importe (generalmente columna -2 o -1)
                    # y saldo (última columna)
                    amount = None
                    balance = None
                    
                    # Intentar obtener importe (penúltima o antepenúltima columna)
                    for i in [-2, -1, 3]:
                        if i < len(row):
                            val = row.iloc[i]
                            if pd.notna(val) and isinstance(val, (int, float)):
                                if amount is None:
                                    amount = float(val)
                                elif balance is None:
                                    balance = float(val)
                                    break
                    
                    if amount is None:
                        continue
                    
                    transaction = {
                        'bank_type': 'kutxabank_account',
                        'date': date.to_pydatetime(),
                        'description': description,
                        'amount': amount,
                        'balance': balance,
                        'reference': None,
                        'extra_info': None
                    }
                    
                    transaction['transaction_hash'] = self.generate_hash(
                        transaction['date'],
                        transaction['description'],
                        transaction['amount'],
                        transaction['bank_type']
                    )
                    
                    transactions.append(transaction)
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
            
            return transactions
        except Exception as e:
            print(f"Error reading Kutxabank account file: {e}")
            raise ValueError(f"No se pudo leer el archivo de Kutxabank: {e}")

class KutxabankCardParser(BaseParser):
    """Parser para extractos de tarjeta de crédito de Kutxabank"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        try:
            # Kutxabank tarjeta es un archivo XLS/XLSX binario
            # Intentar primero con xlrd (archivos .xls antiguos)
            # Si falla, intentar con openpyxl (archivos .xlsx modernos)
            try:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
            
            # Buscar la fila con los encabezados (fecha, concepto, etc.)
            header_row = None
            for idx, row in df.iterrows():
                row_str = ' '.join([str(val).lower() for val in row if pd.notna(val)])
                if 'fecha' in row_str and 'concepto' in row_str:
                    header_row = idx
                    break
            
            if header_row is None:
                raise ValueError("No se encontró la fila de encabezados en el archivo de tarjeta Kutxabank")
            
            # Leer de nuevo sin skiprows, usando el header_row como header
            try:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=header_row)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=header_row)
            
            # Limpiar: remover filas vacías
            df = df.dropna(how='all')
            
            # Resetear el índice después de limpiar
            df = df.reset_index(drop=True)
            
            transactions = []
            
            # Formato típico de tarjeta: fecha, concepto, fecha valor, importe
            for _, row in df.iterrows():
                try:
                    # Saltar filas con NaN en la primera columna (fecha)
                    if pd.isna(row.iloc[0]):
                        continue
                    
                    # Primera columna: fecha operación
                    date_val = row.iloc[0]
                    if isinstance(date_val, str):
                        date = pd.to_datetime(date_val, format='%d/%m/%Y', errors='coerce')
                    else:
                        date = pd.to_datetime(date_val, errors='coerce')
                    
                    if pd.isna(date):
                        continue
                    
                    # Segunda columna: concepto
                    description = str(row.iloc[1]).strip()
                    if description == 'nan' or not description:
                        continue
                    
                    # Última columna: importe (ya es float)
                    amount = row.iloc[-1]
                    if pd.isna(amount):
                        continue
                    
                    amount = float(amount)
                    
                    transaction = {
                        'bank_type': 'kutxabank_card',
                        'date': date.to_pydatetime(),
                        'description': description,
                        'amount': amount,
                        'balance': None,
                        'reference': None,
                        'extra_info': None
                    }
                    
                    transaction['transaction_hash'] = self.generate_hash(
                        transaction['date'],
                        transaction['description'],
                        transaction['amount'],
                        transaction['bank_type']
                    )
                    
                    transactions.append(transaction)
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
            
            return transactions
        except Exception as e:
            print(f"Error reading Kutxabank card file: {e}")
            raise ValueError(f"No se pudo leer el archivo de tarjeta Kutxabank: {e}")

class OpenbankParser(BaseParser):
    """Parser para extractos de Openbank (HTML disfrazado como XLS)"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        try:
            # Openbank exporta HTML con extensión .xls
            # Intentar leer como HTML primero
            encoding = self.detect_encoding(file_content)
            content = file_content.decode(encoding, errors='ignore')
            
            # Si es HTML, parsear la tabla
            if '<html' in content.lower():
                return self._parse_html(content)
            else:
                # Si no es HTML, intentar como CSV
                return self._parse_csv(file_content, encoding)
        except Exception as e:
            print(f"Error reading Openbank file: {e}")
            raise ValueError(f"No se pudo leer el archivo de Openbank: {e}")
    
    def _parse_html(self, content: str) -> List[Dict[str, Any]]:
        """Parsear archivo HTML de Openbank"""
        transactions = []
        
        try:
            tree = html.fromstring(content)
            
            # Buscar todas las filas de la tabla
            # Openbank usa una tabla con las transacciones
            rows = tree.xpath('//tr')
            
            # Buscar las filas que contienen datos (tienen valores de fecha)
            for row in rows:
                cells = row.xpath('.//td//font/text() | .//td/text()')
                cells = [c.strip() for c in cells if c.strip()]
                
                if len(cells) < 4:
                    continue
                
                # Intentar detectar si esta fila contiene una transacción
                # Formato: Fecha Operación, Fecha Valor, Concepto, Importe, Saldo
                try:
                    # Primera celda no vacía debería ser fecha
                    date_str = cells[0]
                    # Verificar si parece una fecha (DD/MM/YYYY)
                    if not re.match(r'\d{2}/\d{2}/\d{4}', date_str):
                        continue
                    
                    date = pd.to_datetime(date_str, format='%d/%m/%Y', errors='coerce')
                    if pd.isna(date):
                        continue
                    
                    # Buscar concepto (texto largo)
                    # Buscar importe (número con posible signo negativo)
                    # Buscar saldo (último número)
                    
                    # Típicamente: [Fecha Op, Fecha Valor, Concepto, Importe, Saldo]
                    if len(cells) >= 5:
                        description = cells[2].strip()
                        amount_str = cells[3].replace('.', '').replace(',', '.')
                        balance_str = cells[4].replace('.', '').replace(',', '.')
                    elif len(cells) == 4:
                        description = cells[2].strip()
                        amount_str = cells[3].replace('.', '').replace(',', '.')
                        balance_str = None
                    else:
                        continue
                    
                    try:
                        amount = float(amount_str)
                    except:
                        continue
                    
                    balance = None
                    if balance_str:
                        try:
                            balance = float(balance_str)
                        except:
                            pass
                    
                    transaction = {
                        'bank_type': 'openbank',
                        'date': date.to_pydatetime(),
                        'description': description,
                        'amount': amount,
                        'balance': balance,
                        'reference': None,
                        'extra_info': None
                    }
                    
                    transaction['transaction_hash'] = self.generate_hash(
                        transaction['date'],
                        transaction['description'],
                        transaction['amount'],
                        transaction['bank_type']
                    )
                    
                    transactions.append(transaction)
                except Exception as e:
                    continue
            
            return transactions
        except Exception as e:
            print(f"Error parsing Openbank HTML: {e}")
            raise ValueError(f"No se pudo parsear el HTML de Openbank: {e}")
    
    def _parse_csv(self, file_content: bytes, encoding: str) -> List[Dict[str, Any]]:
        """Parsear archivo CSV de Openbank (formato alternativo)"""
        df = pd.read_csv(
            BytesIO(file_content),
            encoding=encoding,
            sep=';',
            decimal=',',
            thousands='.'
        )
        
        transactions = []
        
        # Formato Openbank CSV: Fecha;Concepto;Cargo;Abono;Saldo
        for _, row in df.iterrows():
            try:
                date = pd.to_datetime(row.iloc[0], format='%d/%m/%Y', errors='coerce')
                if pd.isna(date):
                    continue
                
                description = str(row.iloc[1]).strip()
                
                # Openbank suele tener columnas separadas para cargo y abono
                cargo = str(row.iloc[2]).replace('.', '').replace(',', '.') if len(row) > 2 else '0'
                abono = str(row.iloc[3]).replace('.', '').replace(',', '.') if len(row) > 3 else '0'
                
                cargo_val = float(cargo) if cargo and cargo != '' else 0
                abono_val = float(abono) if abono and abono != '' else 0
                
                amount = abono_val - cargo_val
                balance = float(str(row.iloc[4]).replace('.', '').replace(',', '.')) if len(row) > 4 else None
                
                transaction = {
                    'bank_type': 'openbank',
                    'date': date.to_pydatetime(),
                    'description': description,
                    'amount': amount,
                    'balance': balance,
                    'reference': None,
                    'extra_info': None
                }
                
                transaction['transaction_hash'] = self.generate_hash(
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['bank_type']
                )
                
                transactions.append(transaction)
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return transactions

class ImaginbankParser(BaseParser):
    """Parser para extractos de Imaginbank"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        try:
            # Detectar encoding
            encoding = self.detect_encoding(file_content)
            
            # Imaginbank proporciona CSVs con punto y coma como separador
            df = pd.read_csv(
                BytesIO(file_content),
                sep=';',
                encoding=encoding,
                decimal=',',
                thousands='.',
                parse_dates=[0],  # Primera columna es la fecha
                dayfirst=True
            )
            
            # Limpiar nombres de columnas
            df.columns = df.columns.str.strip()
            
            # Limpiar filas vacías
            df = df.dropna(how='all')
            
            transactions = []
            
            for _, row in df.iterrows():
                try:
                    # Fecha (primera columna)
                    date = pd.to_datetime(row.iloc[0], errors='coerce')
                    if pd.isna(date):
                        continue
                    
                    # Descripción (segunda columna generalmente)
                    description = str(row.iloc[1]).strip() if len(row) > 1 else ''
                    if not description or description == 'nan':
                        continue
                    
                    # Buscar importe
                    amount = None
                    balance = None
                    
                    # Recorrer las columnas buscando valores numéricos
                    for i in range(2, len(row)):
                        val = row.iloc[i]
                        if pd.notna(val) and isinstance(val, (int, float)):
                            if amount is None:
                                amount = float(val)
                            elif balance is None:
                                balance = float(val)
                    
                    # Si no encontramos importe, saltar
                    if amount is None:
                        continue
                    
                    transaction_hash = self.generate_hash(date, description, amount, 'imaginbank')
                    
                    transactions.append({
                        'bank_type': 'imaginbank',
                        'date': date,
                        'description': description,
                        'amount': amount,
                        'balance': balance,
                        'transaction_hash': transaction_hash
                    })
                    
                except (ValueError, IndexError, AttributeError) as e:
                    print(f"Error procesando fila de Imaginbank: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            raise ValueError(f"Error al parsear CSV de Imaginbank: {str(e)}")


class BBVAParser(BaseParser):
    """Parser para extractos de BBVA"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        try:
            # BBVA proporciona archivos Excel (.xlsx)
            try:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
            
            # Buscar la fila con los encabezados
            # BBVA tiene columnas como: F.Valor, Fecha, Concepto, Movimiento, Importe, Divisa, Disponible
            header_row = None
            for idx, row in df.iterrows():
                row_str = ' '.join([str(val).lower() for val in row if pd.notna(val)])
                if 'f.valor' in row_str or ('fecha' in row_str and 'concepto' in row_str and 'importe' in row_str):
                    header_row = idx
                    break
            
            if header_row is None:
                raise ValueError("No se encontró la fila de encabezados en el archivo de BBVA")
            
            # Leer usando la fila de encabezados encontrada
            try:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=header_row)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=header_row)
            
            # Limpiar: remover filas vacías
            df = df.dropna(how='all')
            df = df.reset_index(drop=True)
            
            transactions = []
            
            for _, row in df.iterrows():
                try:
                    # Buscar la columna de fecha (puede ser "F.Valor" o "Fecha")
                    date = None
                    description = None
                    amount = None
                    balance = None
                    extra_info = []
                    
                    # Intentar obtener fecha de "F.Valor" o "Fecha"
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'f.valor' in col_lower or (col_lower == 'fecha' and date is None):
                            date_val = row[col]
                            if pd.notna(date_val):
                                if isinstance(date_val, str):
                                    date = pd.to_datetime(date_val, format='%d/%m/%Y', errors='coerce')
                                else:
                                    date = pd.to_datetime(date_val, errors='coerce')
                                if pd.notna(date):
                                    break
                    
                    if pd.isna(date):
                        continue
                    
                    # Buscar concepto/descripción
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'concepto' in col_lower or 'descripción' in col_lower or 'descripcion' in col_lower:
                            description = str(row[col]).strip()
                            if description != 'nan':
                                break
                    
                    # Si hay columna "Movimiento", añadirla a la descripción
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'movimiento' in col_lower:
                            mov = str(row[col]).strip()
                            if mov != 'nan' and mov:
                                if description:
                                    description = f"{description} - {mov}"
                                else:
                                    description = mov
                                break
                    
                    if not description or description == 'nan':
                        continue
                    
                    # Buscar importe
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'importe' in col_lower:
                            amt = row[col]
                            if pd.notna(amt) and amt != '':
                                try:
                                    amount = float(amt)
                                    break
                                except:
                                    pass
                    
                    # Buscar saldo/disponible
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'disponible' in col_lower or 'saldo' in col_lower:
                            bal = row[col]
                            if pd.notna(bal) and bal != '':
                                try:
                                    balance = float(bal)
                                    break
                                except:
                                    pass
                    
                    if amount is None:
                        continue
                    
                    # Añadir observaciones si existen
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'observacion' in col_lower:
                            obs = str(row[col]).strip()
                            if obs != 'nan' and obs:
                                extra_info.append(obs)
                    
                    transaction_hash = self.generate_hash(date, description, amount, 'bbva')
                    
                    transactions.append({
                        'bank_type': 'bbva',
                        'date': date,
                        'description': description,
                        'amount': amount,
                        'balance': balance,
                        'extra_info': ' | '.join(extra_info) if extra_info else None,
                        'transaction_hash': transaction_hash
                    })
                    
                except (ValueError, IndexError, AttributeError) as e:
                    print(f"Error procesando fila de BBVA: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            raise ValueError(f"Error al parsear archivo de BBVA: {str(e)}")


class INGParser(BaseParser):
    """Parser para extractos de ING Direct"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        try:
            # ING proporciona archivos Excel (.xls o .xlsx)
            try:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=None)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=None)
            
            # Buscar la fila con los encabezados
            # ING tiene columnas como: F. VALOR, CATEGORÍA, SUBCATEGORÍA, DESCRIPCIÓN, IMPORTE (€), SALDO (€)
            header_row = None
            for idx, row in df.iterrows():
                row_str = ' '.join([str(val).lower() for val in row if pd.notna(val)])
                if 'f. valor' in row_str or ('categoria' in row_str and 'importe' in row_str):
                    header_row = idx
                    break
            
            if header_row is None:
                raise ValueError("No se encontró la fila de encabezados en el archivo de ING")
            
            # Leer usando la fila de encabezados encontrada
            try:
                df = pd.read_excel(BytesIO(file_content), engine='xlrd', header=header_row)
            except:
                df = pd.read_excel(BytesIO(file_content), engine='openpyxl', header=header_row)
            
            # Limpiar nombres de columnas
            df.columns = [str(col).strip() for col in df.columns]
            
            # Limpiar: remover filas vacías
            df = df.dropna(how='all')
            df = df.reset_index(drop=True)
            
            transactions = []
            
            for _, row in df.iterrows():
                try:
                    # Buscar la columna de fecha
                    date = None
                    description = None
                    amount = None
                    balance = None
                    category_info = []
                    
                    # Obtener fecha (primera columna o columna con "F. VALOR")
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'f. valor' in col_lower or 'fecha' in col_lower:
                            date_val = row[col]
                            if pd.notna(date_val):
                                date = pd.to_datetime(date_val, errors='coerce')
                                if pd.notna(date):
                                    break
                    
                    # Si no encontramos fecha específica, probar la primera columna
                    if pd.isna(date):
                        date_val = row.iloc[0]
                        if pd.notna(date_val):
                            date = pd.to_datetime(date_val, errors='coerce')
                    
                    if pd.isna(date):
                        continue
                    
                    # Buscar descripción
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'descripcion' in col_lower or 'descripción' in col_lower:
                            description = str(row[col]).strip()
                            if description != 'nan':
                                break
                    
                    if not description or description == 'nan':
                        description = ''
                    
                    # Añadir categoría y subcategoría a la descripción
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'categoria' in col_lower or 'categoría' in col_lower:
                            cat = str(row[col]).strip()
                            if cat != 'nan' and cat:
                                category_info.append(cat)
                        elif 'subcategoria' in col_lower or 'subcategoría' in col_lower:
                            subcat = str(row[col]).strip()
                            if subcat != 'nan' and subcat:
                                category_info.append(subcat)
                    
                    # Combinar categorías con descripción
                    if category_info:
                        cat_str = ' - '.join(category_info)
                        if description:
                            description = f"{cat_str}: {description}"
                        else:
                            description = cat_str
                    
                    if not description:
                        continue
                    
                    # Buscar importe
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'importe' in col_lower:
                            amt = row[col]
                            if pd.notna(amt) and amt != '':
                                try:
                                    amount = float(amt)
                                    break
                                except:
                                    pass
                    
                    # Buscar saldo
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'saldo' in col_lower:
                            bal = row[col]
                            if pd.notna(bal) and bal != '':
                                try:
                                    balance = float(bal)
                                    break
                                except:
                                    pass
                    
                    if amount is None:
                        continue
                    
                    # Añadir comentario si existe
                    extra_info = []
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'comentario' in col_lower:
                            comment = str(row[col]).strip()
                            if comment != 'nan' and comment:
                                extra_info.append(comment)
                    
                    transaction_hash = self.generate_hash(date, description, amount, 'ing')
                    
                    transactions.append({
                        'bank_type': 'ing',
                        'date': date,
                        'description': description,
                        'amount': amount,
                        'balance': balance,
                        'extra_info': ' | '.join(extra_info) if extra_info else None,
                        'transaction_hash': transaction_hash
                    })
                    
                except (ValueError, IndexError, AttributeError) as e:
                    print(f"Error procesando fila de ING: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            raise ValueError(f"Error al parsear archivo de ING: {str(e)}")


def get_parser(bank_type: str) -> BaseParser:
    """Parser para extractos de Imaginbank"""
    
    def parse(self, file_content: bytes) -> List[Dict[str, Any]]:
        encoding = self.detect_encoding(file_content)
        
        df = pd.read_csv(
            BytesIO(file_content),
            encoding=encoding,
            sep=';',
            decimal=',',
            thousands='.'
        )
        
        transactions = []
        
        # Formato Imaginbank: Concepto;Fecha;Importe;Saldo
        # Los valores tienen "EUR" al final
        for _, row in df.iterrows():
            try:
                # En Imaginbank, la fecha está en la segunda columna
                # Columnas: Concepto, Fecha, Importe, Saldo
                description = str(row.iloc[0]).strip()
                
                # Fecha en la segunda posición
                date_str = str(row.iloc[1]).strip()
                date = pd.to_datetime(date_str, format='%d/%m/%Y', errors='coerce')
                if pd.isna(date):
                    continue
                
                # Importe en la tercera posición (con EUR al final)
                amount_str = str(row.iloc[2]).strip()
                # Quitar "EUR" si existe
                amount_str = amount_str.replace('EUR', '').strip()
                # Limpiar formato: -217,98 -> -217.98
                amount_str = amount_str.replace('.', '').replace(',', '.')
                try:
                    amount = float(amount_str)
                except:
                    continue
                
                # Saldo en la cuarta posición (con EUR al final)
                balance = None
                if len(row) > 3:
                    try:
                        balance_str = str(row.iloc[3]).strip()
                        balance_str = balance_str.replace('EUR', '').strip()
                        balance_str = balance_str.replace('.', '').replace(',', '.')
                        balance = float(balance_str)
                    except:
                        pass
                
                transaction = {
                    'bank_type': 'imaginbank',
                    'date': date.to_pydatetime(),
                    'description': description,
                    'amount': amount,
                    'balance': balance,
                    'reference': None,
                    'extra_info': None
                }
                
                transaction['transaction_hash'] = self.generate_hash(
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['bank_type']
                )
                
                transactions.append(transaction)
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return transactions

def get_parser(bank_type: str) -> BaseParser:
    """Factory para obtener el parser apropiado según el tipo de banco"""
    parsers = {
        'kutxabank_account': KutxabankAccountParser(),
        'kutxabank_card': KutxabankCardParser(),
        'openbank': OpenbankParser(),
        'imaginbank': ImaginbankParser(),
        'bbva': BBVAParser(),
        'ing': INGParser()
    }
    
    parser = parsers.get(bank_type)
    if not parser:
        raise ValueError(f"Tipo de banco no soportado: {bank_type}")
    
    return parser
