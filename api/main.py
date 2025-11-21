# api/main.py - VERSIÓN CORREGIDA
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sql_db.database import engine, Base
from api.models import user_models
from api import auth_router
from api.routes import users, jobs, celery_task

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobScope API",
    description="API para gestión de trabajos y matching de empleos",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
app.include_router(celery_task.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "JobScope API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}