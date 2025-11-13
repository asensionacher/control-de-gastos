from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import transactions, categories, upload, reports, auth

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Control de Gastos API",
    description="API para el control financiero del hogar",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/")
async def root():
    return {"message": "Control de Gastos API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
