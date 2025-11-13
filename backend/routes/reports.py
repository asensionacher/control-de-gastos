from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from database import get_db
from models import Transaction as TransactionModel, Category as CategoryModel
from schemas import MonthlyReport, CategoryReport, ReportSummary, Transaction
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/monthly", response_model=List[MonthlyReport])
def get_monthly_report(
    months: int = Query(12, description="Número de meses a incluir"),
    db: Session = Depends(get_db)
):
    """Obtener reporte mensual de ingresos y gastos"""
    # Calcular fecha de inicio
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    # Agrupar por año y mes
    results = db.query(
        extract('year', TransactionModel.date).label('year'),
        extract('month', TransactionModel.date).label('month'),
        func.sum(case((TransactionModel.amount > 0, TransactionModel.amount), else_=0)).label('income'),
        func.sum(case((TransactionModel.amount < 0, TransactionModel.amount), else_=0)).label('expenses')
    ).filter(
        TransactionModel.date >= start_date
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    monthly_reports = []
    for row in results:
        month_str = f"{int(row.year)}-{int(row.month):02d}"
        monthly_reports.append(MonthlyReport(
            month=month_str,
            total_income=float(row.income or 0),
            total_expenses=abs(float(row.expenses or 0)),
            balance=float(row.income or 0) + float(row.expenses or 0)
        ))
    
    return monthly_reports

@router.get("/by-category", response_model=List[CategoryReport])
def get_category_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener reporte de gastos por categoría"""
    query = db.query(
        CategoryModel.name,
        func.sum(TransactionModel.amount).label('total'),
        func.count(TransactionModel.id).label('count')
    ).join(
        TransactionModel, TransactionModel.category_id == CategoryModel.id
    ).filter(
        TransactionModel.amount < 0  # Solo gastos
    )
    
    if start_date:
        query = query.filter(TransactionModel.date >= datetime.fromisoformat(start_date))
    
    if end_date:
        query = query.filter(TransactionModel.date <= datetime.fromisoformat(end_date))
    
    results = query.group_by(CategoryModel.name).all()
    
    # Calcular total para porcentajes
    total_expenses = sum(abs(float(r.total)) for r in results)
    
    category_reports = []
    for row in results:
        total = abs(float(row.total))
        percentage = (total / total_expenses * 100) if total_expenses > 0 else 0
        
        category_reports.append(CategoryReport(
            category_name=row.name,
            total=total,
            count=int(row.count),
            percentage=round(percentage, 2)
        ))
    
    # Ordenar por total descendente
    category_reports.sort(key=lambda x: x.total, reverse=True)
    
    return category_reports

@router.get("/top-expenses", response_model=List[Transaction])
def get_top_expenses(
    limit: int = Query(10, description="Número de gastos a devolver"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener los gastos más grandes"""
    query = db.query(TransactionModel).filter(
        TransactionModel.amount < 0
    )
    
    if start_date:
        query = query.filter(TransactionModel.date >= datetime.fromisoformat(start_date))
    
    if end_date:
        query = query.filter(TransactionModel.date <= datetime.fromisoformat(end_date))
    
    top_expenses = query.order_by(TransactionModel.amount.asc()).limit(limit).all()
    
    return top_expenses

@router.get("/summary", response_model=ReportSummary)
def get_report_summary(
    months: int = Query(6, description="Número de meses"),
    db: Session = Depends(get_db)
):
    """Obtener resumen completo de reportes"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    # Obtener reportes
    monthly = get_monthly_report(months=months, db=db)
    categories = get_category_report(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        db=db
    )
    top_expenses = get_top_expenses(
        limit=10,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        db=db
    )
    
    return ReportSummary(
        monthly_reports=monthly,
        category_reports=categories,
        top_expenses=top_expenses
    )

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Obtener estadísticas generales"""
    total_transactions = db.query(TransactionModel).count()
    total_income = db.query(func.sum(TransactionModel.amount)).filter(
        TransactionModel.amount > 0
    ).scalar() or 0
    total_expenses = db.query(func.sum(TransactionModel.amount)).filter(
        TransactionModel.amount < 0
    ).scalar() or 0
    uncategorized = db.query(TransactionModel).filter(
        TransactionModel.category_id == None
    ).count()
    
    return {
        "total_transactions": total_transactions,
        "total_income": float(total_income),
        "total_expenses": abs(float(total_expenses)),
        "balance": float(total_income) + float(total_expenses),
        "uncategorized": uncategorized
    }
