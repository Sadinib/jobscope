from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

app = Celery(
    'jobscope',
    broker='sqla+sqlite:///celery_broker.sqlite',
    backend='db+sqlite:///celery_results.sqlite',
    include=['tasks.scraping_tasks']
)

#app = Celery(
#    "jobscope",
#    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
#    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
#    include=["task.scraping_tasks"]
#)

#Cofiguracion
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Bogota",
    enable_ult=True
)

# Tareas periódicas (Beat Schedule)
app.conf.beat_schedule = {
    'scrape-daily-morning': {
        'task': 'tasks.scraping_tasks.daily_scraping',
        'schedule': 3600.0,  # Cada 1 hora para testing (luego cambiar a 6-12 horas)
    },
    'clean-old-jobs-weekly': {
        'task': 'tasks.scraping_tasks.clean_old_jobs',
        'schedule': 604800.0,  # Una vez por semana
    },
}

if __name__ == '__main__':
    app.start()