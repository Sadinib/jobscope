# test_imports.py
import sys
import os
print("🔍 Verificando estructura...")

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(f"Python path: {sys.path}")

try:
    from db.db import db
    print("✅ MongoDB importado correctamente")
except ImportError as e:
    print(f"❌ Error importando MongoDB: {e}")

try:
    from scraping.job_scrapers.computrabajo_scraper import ComputrabajoScraper
    print("✅ ComputrabajoScraper importado correctamente")
except ImportError as e:
    print(f"❌ Error importando ComputrabajoScraper: {e}")

try:
    from scraping.job_scrapers.indeed_scraper import IndeedScraper
    print("✅ IndeedScraper importado correctamente")
except ImportError as e:
    print(f"❌ Error importando IndeedScraper: {e}")

print("🏁 Test de imports completado")