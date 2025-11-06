from scraping.scraping_orchestrator import ScrapingOrchestrator

def main():
    print("Iniciando JobScope Scrapers...")
    
    try:
        from db.db import db
        print("MongoDB conectado")
        
        #Limpiar antes de empezar (opcional)
        print("Limpiando trabajos anteriores...")
        result = db.jobs.delete_many({})
        print(f"Eliminados {result.deleted_count} trabajos anteriores")
        
        print("\n" + "="*50)
        print("Ejecutando scraping completo...")
        jobs_count, jobs = ScrapingOrchestrator.run_full_scraping()
        
        #Resumen
        print("\n" + "="*50)
        print("RESUMEN FINAL:")
        print(f"Total trabajos scrapeados: {jobs_count}")
        
    except Exception as e:
        print(f"ERROR general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()