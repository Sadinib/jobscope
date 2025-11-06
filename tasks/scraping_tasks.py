from celery import Celery
import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from celery_app import app
from scraping.scraping_orchestrator import ScrapingOrchestrator

@app.task(bind=True, max_retries=3)
def daily_scraping(self):
    try:
        print("Iniciando scraping automático")

        jobs_count, jobs = ScrapingOrchestrator.run_full_scraping()

        print(f"Scraping automático completado: {jobs_count} trabajos")
        return {
            "status": "success",
            "total_jobs": jobs_count,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error en scraping automático: {e}")
        raise self.retry(countdown=300, exc=e)

@app.task
def clean_old_jobs():
    try:
        ScrapingOrchestrator.clean_old_jobs()
        return {"status": "success", "cleaned_at": datetime.datetime.now().isoformat()}
    except Exception as e:
        print(f"Error en limpieza: {e}")
        return {"status": "error", "error": str(e)}
    
@app.task
def manual_scrape(query="python", location="Colombia"):
    try:
        print(f"Scraping manual: {query} en {location}")
        
        jobs_count, jobs = ScrapingOrchestrator.run_full_scraping(query, location)
        
        return {
            "status": "success",
            "query": query,
            "location": location, 
            "total_jobs": jobs_count,
        }
        
    except Exception as e:
        print(f"Error en scraping manual: {e}")
        return {"status": "error", "error": str(e)}