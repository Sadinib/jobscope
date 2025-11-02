# run_scrapers.py
import sys
import os
sys.path.insert(0, os.getcwd())

print("🚀 Iniciando JobScope Scrapers...")

try:
    from db.db import db
    print("MongoDB conectado")

    print("🧹 Limpiando TODOS los trabajos...")
    result = db.jobs.delete_many({})
    print(f"Eliminados {result.deleted_count} trabajos")
    
    # 1. COMPUTRABAJO (Requests) - Ya funciona
    print("\n" + "="*50)
    print("🔍 Probando ComputrabajoScraper...")
    from scraping.job_scrapers.computrabajo_scraper import ComputrabajoScraper
    
    compu_scraper = ComputrabajoScraper()
    compu_jobs = compu_scraper.scrape("python", "Colombia", pages=1)
    print(f"Computrabajo: {len(compu_jobs)} trabajos encontrados")
    
    # 2. INDEED (Selenium) - CÓDIGO EXACTO del test que funciona
    print("\n" + "="*50)
    print("Probando IndeedScraper con Selenium...")
    from scraping.job_scrapers.indeed_scraper import IndeedScraper
    
    indeed_scraper = IndeedScraper()
    try:
        indeed_jobs = indeed_scraper.scrape("python", "Medellín", pages=1)  # Mismo parámetro que en el test
        print(f"Indeed: {len(indeed_jobs)} trabajos encontrados")
            
    except Exception as e:
        print(f"Error en Indeed: {e}")
        indeed_jobs = []
    finally:
        indeed_scraper.selenium_scraper.close()  # MÉTODO EXACTO del test
    
    # RESUMEN FINAL
    print("\n" + "="*50)
    total_jobs = len(compu_jobs) + len(indeed_jobs)
    print("RESUMEN FINAL:")
    print(f"Total trabajos scrapeados: {total_jobs}")
    print(f"   - Computrabajo (Requests): {len(compu_jobs)}")
    print(f"   - Indeed (Selenium): {len(indeed_jobs)}")
    
except Exception as e:
    print(f"ERROR general: {e}")
    import traceback
    traceback.print_exc()

print("\nScript terminado")