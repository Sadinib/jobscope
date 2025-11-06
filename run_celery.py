import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from celery_app import app

if __name__ == '__main__':
    print("Iniciando Celery Worker...")
    print("   - Broker: SQLite")
    print("   - Tareas: Scraping automático")
    print("   - Presiona Ctrl+C para detener")
    
    app.worker_main(['worker', 
                     '--loglevel=info', 
                     '--concurrency=1',
                     '--pool=solo'
                     ])