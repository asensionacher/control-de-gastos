from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Transaction as TransactionModel, StoreMapping
from schemas import Transaction, TransactionUpdate
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class BulkCategorizeRequest(BaseModel):
    transaction_ids: List[int]
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None

@router.get("/", response_model=List[Transaction])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    bank_type: Optional[str] = None,
    category_id: Optional[str] = None,  # Cambiado a str para permitir "null"
    transaction_type: Optional[str] = None,
    description: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de transacciones con filtros opcionales"""
    query = db.query(TransactionModel)
    
    if bank_type:
        query = query.filter(TransactionModel.bank_type == bank_type)
    
    if category_id:
        # Si es "null", filtrar por transacciones sin categoría
        if category_id == "null":
            query = query.filter(TransactionModel.category_id == None)
        else:
            query = query.filter(TransactionModel.category_id == int(category_id))
    
    if transaction_type:
        if transaction_type == 'expense':
            query = query.filter(TransactionModel.amount < 0)
        elif transaction_type == 'income':
            query = query.filter(TransactionModel.amount > 0)
    
    if description:
        query = query.filter(TransactionModel.description.ilike(f'%{description}%'))
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(TransactionModel.date >= start)
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(TransactionModel.date <= end)
    
    transactions = query.order_by(TransactionModel.date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Obtener una transacción específica"""
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    apply_to_all: Optional[bool] = False

@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una transacción (principalmente para categorización)"""
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Verificar si se está actualizando la categoría (incluyendo establecer a None)
    update_dict = transaction_update.model_dump(exclude_unset=True)
    has_category_update = 'category_id' in update_dict or 'subcategory_id' in update_dict
    
    # Si se actualiza la categoría y apply_to_all es True, actualizar todas con la misma descripción
    if has_category_update and transaction_update.apply_to_all:
        description = transaction.description
        
        # Actualizar todas las transacciones con la misma descripción
        transactions_to_update = db.query(TransactionModel).filter(
            TransactionModel.description == description
        ).all()
        
        for trans in transactions_to_update:
            if 'category_id' in update_dict:
                trans.category_id = transaction_update.category_id
            if 'subcategory_id' in update_dict:
                trans.subcategory_id = transaction_update.subcategory_id
        
        # Actualizar el mapeo de tienda
        store_name = description.split()[0] if description else ""
        
        if store_name:
            store_mapping = db.query(StoreMapping).filter(
                StoreMapping.store_name == store_name
            ).first()
            
            if store_mapping:
                if 'category_id' in update_dict:
                    store_mapping.category_id = transaction_update.category_id
                if 'subcategory_id' in update_dict:
                    store_mapping.subcategory_id = transaction_update.subcategory_id
            else:
                # Solo crear mapeo si hay una categoría válida (no None)
                if transaction_update.category_id is not None:
                    new_mapping = StoreMapping(
                        store_name=store_name,
                        category_id=transaction_update.category_id,
                        subcategory_id=transaction_update.subcategory_id
                    )
                    db.add(new_mapping)
    else:
        # Solo actualizar la transacción específica
        if 'category_id' in update_dict:
            transaction.category_id = transaction_update.category_id
        if 'subcategory_id' in update_dict:
            transaction.subcategory_id = transaction_update.subcategory_id
    
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Eliminar una transacción"""
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transacción eliminada correctamente"}

@router.get("/uncategorized/count")
def get_uncategorized_count(db: Session = Depends(get_db)):
    """Obtener el número de transacciones sin categorizar"""
    count = db.query(TransactionModel).filter(TransactionModel.category_id == None).count()
    return {"count": count}

@router.post("/bulk-categorize")
def bulk_categorize_transactions(
    request: BulkCategorizeRequest,
    db: Session = Depends(get_db)
):
    """Categorizar múltiples transacciones a la vez"""
    if not request.transaction_ids:
        raise HTTPException(status_code=400, detail="No se proporcionaron IDs de transacciones")
    
    # Actualizar todas las transacciones
    transactions = db.query(TransactionModel).filter(
        TransactionModel.id.in_(request.transaction_ids)
    ).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones")
    
    updated_count = 0
    for transaction in transactions:
        transaction.category_id = request.category_id
        transaction.subcategory_id = request.subcategory_id
        updated_count += 1
        
        # Actualizar mapeo de tienda solo si hay una categoría válida (no None)
        if request.category_id is not None:
            store_name = transaction.description.split()[0] if transaction.description else ""
            if store_name:
                store_mapping = db.query(StoreMapping).filter(
                    StoreMapping.store_name == store_name
                ).first()
                
                if store_mapping:
                    store_mapping.category_id = request.category_id
                    if request.subcategory_id:
                        store_mapping.subcategory_id = request.subcategory_id
                else:
                    new_mapping = StoreMapping(
                        store_name=store_name,
                        category_id=request.category_id,
                        subcategory_id=request.subcategory_id
                    )
                    db.add(new_mapping)
    
    db.commit()
    
    return {
        "message": f"Se categorizaron {updated_count} transacciones",
        "updated_count": updated_count
    }

@router.post("/bulk-delete")
def bulk_delete_transactions(
    transaction_ids: List[int],
    db: Session = Depends(get_db)
):
    """Eliminar múltiples transacciones a la vez"""
    if not transaction_ids:
        raise HTTPException(status_code=400, detail="No se proporcionaron IDs de transacciones")
    
    # Buscar las transacciones
    transactions = db.query(TransactionModel).filter(
        TransactionModel.id.in_(transaction_ids)
    ).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones")
    
    deleted_count = len(transactions)
    
    # Eliminar todas
    for transaction in transactions:
        db.delete(transaction)
    
    db.commit()
    
    return {
        "message": f"Se eliminaron {deleted_count} transacciones",
        "deleted_count": deleted_count
    }
