from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import Transaction as TransactionModel, StoreMapping, User
from schemas import UploadResponse
from parsers import get_parser
from bank_detector import BankDetector
from typing import Optional, List
from auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=UploadResponse)
async def upload_csv(
    files: List[UploadFile] = File(...),
    bank_type: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Subir uno o varios archivos de extracto bancario (CSV, XLS, HTML)
    
    Si no se especifica bank_type, se intentará detectar automáticamente.
    
    Tipos de banco soportados:
    - kutxabank_account
    - kutxabank_card
    - openbank
    - imaginbank
    """
    try:
        # Estadísticas totales
        total_rows = 0
        imported = 0
        duplicates = 0
        errors = 0
        processed_files = 0
        file_details = []
        
        # Procesar cada archivo
        for file in files:
            try:
                # Leer el contenido del archivo
                content = await file.read()
                
                # Detectar o usar el tipo de banco proporcionado
                detected_bank_type = bank_type
                
                if not detected_bank_type:
                    # Intentar detectar automáticamente
                    detected_bank_type = BankDetector.detect_bank_type(content, file.filename)
                    
                    if not detected_bank_type:
                        file_details.append(f"❌ {file.filename}: No se pudo detectar el banco")
                        errors += 1
                        continue
                
                # Obtener el parser apropiado
                try:
                    parser = get_parser(detected_bank_type)
                except ValueError as e:
                    file_details.append(f"❌ {file.filename}: {str(e)}")
                    errors += 1
                    continue
                
                # Parsear el archivo
                transactions = parser.parse(content)
                
                if not transactions:
                    file_details.append(f"⚠️ {file.filename}: Sin transacciones")
                    continue
                
                # Estadísticas por archivo
                file_imported = 0
                file_duplicates = 0
                file_errors = 0
                
                total_rows += len(transactions)
                
                # Insertar transacciones
                for trans_data in transactions:
                    try:
                        # Buscar mapeo de tienda para auto-categorización
                        store_name = trans_data['description'].split()[0] if trans_data['description'] else ""
                        store_mapping = db.query(StoreMapping).filter(
                            StoreMapping.store_name == store_name
                        ).first()
                        
                        if store_mapping:
                            trans_data['category_id'] = store_mapping.category_id
                            trans_data['subcategory_id'] = store_mapping.subcategory_id
                        
                        # Crear transacción
                        transaction = TransactionModel(**trans_data)
                        db.add(transaction)
                        db.commit()
                        imported += 1
                        file_imported += 1
                        
                    except IntegrityError:
                        # Duplicado detectado por transaction_hash único
                        db.rollback()
                        duplicates += 1
                        file_duplicates += 1
                    except Exception as e:
                        db.rollback()
                        errors += 1
                        file_errors += 1
                        print(f"Error al insertar transacción: {e}")
                
                processed_files += 1
                bank_name = dict(BankDetector.get_available_banks()).get(
                    detected_bank_type, detected_bank_type
                )
                file_details.append(
                    f"✓ {file.filename} ({bank_name}): {file_imported} nuevas, {file_duplicates} duplicadas"
                )
                
            except Exception as e:
                file_details.append(f"❌ {file.filename}: Error - {str(e)}")
                errors += 1
                continue
        
        # Construir mensaje de resumen
        if processed_files == 0:
            return UploadResponse(
                success=False,
                total_rows=total_rows,
                imported=imported,
                duplicates=duplicates,
                errors=errors,
                message="No se pudo procesar ningún archivo. " + "; ".join(file_details)
            )
        
        summary = f"Procesados {processed_files} de {len(files)} archivo(s): {imported} nuevas, {duplicates} duplicadas, {errors} errores"
        if file_details:
            summary += "\n\n" + "\n".join(file_details)
        
        return UploadResponse(
            success=True,
            total_rows=total_rows,
            imported=imported,
            duplicates=duplicates,
            errors=errors,
            message=summary
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los archivos: {str(e)}")

@router.get("/bank-types")
def get_bank_types():
    """Obtener lista de tipos de banco soportados"""
    banks = BankDetector.get_available_banks()
    return {
        "bank_types": [
            {"id": bank['value'], "name": bank['label']}
            for bank in banks
        ]
    }

@router.post("/detect-bank")
async def detect_bank(file: UploadFile = File(...)):
    """Detectar automáticamente el tipo de banco del archivo"""
    try:
        content = await file.read()
        detected_type = BankDetector.detect_bank_type(content, file.filename)
        
        if detected_type:
            banks = {bank['value']: bank['label'] for bank in BankDetector.get_available_banks()}
            return {
                "success": True,
                "bank_type": detected_type,
                "bank_name": banks.get(detected_type, detected_type)
            }
        else:
            return {
                "success": False,
                "message": "No se pudo detectar el tipo de banco automáticamente"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar el archivo: {str(e)}")
