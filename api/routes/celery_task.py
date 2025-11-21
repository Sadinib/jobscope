# api/routes/tasks.py
from fastapi import APIRouter, HTTPException, Depends
from celery.result import AsyncResult
from tasks.scraping_tasks import manual_scrape, daily_scraping, clean_old_jobs
from api.auth import get_current_active_user
from api.models.user_models import User
from celery_app import app

router = APIRouter()

@router.post("/tasks/scrape")
async def trigger_scraping(
    query: str = "python", 
    location: str = "Colombia",
    current_user: User = Depends(get_current_active_user)
):
    """Disparar scraping manual (requiere autenticación)"""
    try:
        task = app.send_task(
            'tasks.scraping_tasks.manual_scrape',
            args=[query, location]
        )
        return {
            "task_id": task.id,
            "status": "started",
            "message": f"Scraping iniciado para '{query}' en {location}",
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/clean")
async def trigger_cleanup(current_user: User = Depends(get_current_active_user)):
    """Disparar limpieza de trabajos antiguos (requiere autenticación)"""
    try:
        task = app.send_task('tasks.scraping_tasks.clean_old_jobs')
        return {
            "task_id": task.id,
            "status": "started", 
            "message": "Limpieza de trabajos antiguos iniciada",
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Obtener estado de una tarea (requiere autenticación)"""
    task_result = AsyncResult(task_id)
    
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
        "successful": task_result.successful() if task_result.ready() else None,
        "user_id": current_user.id
    }

@router.get("/tasks")
async def get_active_tasks(current_user: User = Depends(get_current_active_user)):
    """Obtener información sobre tareas (requiere autenticación)"""
    return {
        "message": "Endpoints de tareas disponibles",
        "user_id": current_user.id,
        "endpoints": {
            "check_task": "GET /api/v1/tasks/{task_id}",
            "start_scraping": "POST /api/v1/tasks/scrape",
            "start_cleanup": "POST /api/v1/tasks/clean"
        }
    }