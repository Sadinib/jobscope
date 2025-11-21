# run_api.py
import sys
import os

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from api.main import app

if __name__ == "__main__":
    print("🚀 Iniciando JobScope FastAPI...")
    print("   - Host: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print("   - Presiona Ctrl+C para detener")
    
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True  # Auto-reload para desarrollo
    )