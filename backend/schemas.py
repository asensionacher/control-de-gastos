from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
import re

# User & Auth Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        if len(v) > 50:
            raise ValueError('El nombre de usuario no puede tener más de 50 caracteres')
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('El nombre de usuario solo puede contener letras, números, guiones y guiones bajos')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if len(v) > 100:
            raise ValueError('La contraseña no puede tener más de 100 caracteres')
        
        # Validar complejidad de contraseña
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe contener al menos un número')
        
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Category Schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Subcategory Schemas
class SubcategoryBase(BaseModel):
    name: str
    category_id: int

class SubcategoryCreate(SubcategoryBase):
    pass

class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None

class Subcategory(SubcategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryWithSubcategories(Category):
    subcategories: List[Subcategory] = []

# Transaction Schemas
class TransactionBase(BaseModel):
    bank_type: str
    date: datetime
    description: str
    amount: float
    balance: Optional[float] = None
    reference: Optional[str] = None
    extra_info: Optional[str] = None

class TransactionCreate(TransactionBase):
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    description: Optional[str] = None
    apply_to_all: Optional[bool] = False

class Transaction(TransactionBase):
    id: int
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None
    subcategory: Optional[Subcategory] = None
    
    class Config:
        from_attributes = True

# Upload Schemas
class UploadResponse(BaseModel):
    success: bool
    total_rows: int
    imported: int
    duplicates: int
    errors: int
    message: str

# Report Schemas
class MonthlyReport(BaseModel):
    month: str
    total_income: float
    total_expenses: float
    balance: float

class CategoryReport(BaseModel):
    category_name: str
    total: float
    count: int
    percentage: float

class ReportSummary(BaseModel):
    monthly_reports: List[MonthlyReport]
    category_reports: List[CategoryReport]
    top_expenses: List[Transaction]
