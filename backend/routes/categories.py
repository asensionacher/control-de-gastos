from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Category as CategoryModel, Subcategory as SubcategoryModel
from schemas import (
    Category, CategoryCreate, CategoryUpdate, CategoryWithSubcategories,
    Subcategory, SubcategoryCreate, SubcategoryUpdate
)

router = APIRouter()

# Categorías
@router.get("/", response_model=List[CategoryWithSubcategories])
def get_categories(db: Session = Depends(get_db)):
    """Obtener todas las categorías con sus subcategorías"""
    categories = db.query(CategoryModel).all()
    return categories

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Crear una nueva categoría"""
    # Verificar si ya existe
    existing = db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una categoría"""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    for field, value in category.dict(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Eliminar una categoría"""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Categoría eliminada correctamente"}

# Subcategorías
@router.get("/{category_id}/subcategories", response_model=List[Subcategory])
def get_subcategories(category_id: int, db: Session = Depends(get_db)):
    """Obtener subcategorías de una categoría"""
    subcategories = db.query(SubcategoryModel).filter(
        SubcategoryModel.category_id == category_id
    ).all()
    return subcategories

@router.post("/{category_id}/subcategories", response_model=Subcategory)
def create_subcategory(
    category_id: int,
    subcategory: SubcategoryCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva subcategoría"""
    # Verificar que la categoría existe
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar subcategoría duplicada
    existing = db.query(SubcategoryModel).filter(
        SubcategoryModel.name == subcategory.name,
        SubcategoryModel.category_id == category_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="La subcategoría ya existe")
    
    db_subcategory = SubcategoryModel(**subcategory.dict())
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

@router.put("/subcategories/{subcategory_id}", response_model=Subcategory)
def update_subcategory(
    subcategory_id: int,
    subcategory: SubcategoryUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una subcategoría"""
    db_subcategory = db.query(SubcategoryModel).filter(
        SubcategoryModel.id == subcategory_id
    ).first()
    if not db_subcategory:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    
    for field, value in subcategory.dict(exclude_unset=True).items():
        setattr(db_subcategory, field, value)
    
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

@router.delete("/subcategories/{subcategory_id}")
def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    """Eliminar una subcategoría"""
    db_subcategory = db.query(SubcategoryModel).filter(
        SubcategoryModel.id == subcategory_id
    ).first()
    if not db_subcategory:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    
    db.delete(db_subcategory)
    db.commit()
    return {"message": "Subcategoría eliminada correctamente"}

@router.post("/init-default")
def initialize_default_categories(db: Session = Depends(get_db)):
    """Inicializar categorías por defecto"""
    default_categories = [
        "Hipoteca", "Coche", "Gasolina", "Parking", "Comida",
        "Niños", "Cumpleaños", "Préstamos", "Suministros",
        "Colegio", "Salud", "IBI"
    ]
    
    created = []
    for cat_name in default_categories:
        existing = db.query(CategoryModel).filter(CategoryModel.name == cat_name).first()
        if not existing:
            category = CategoryModel(name=cat_name)
            db.add(category)
            created.append(cat_name)
    
    db.commit()
    return {"message": f"Categorías inicializadas", "created": created}
