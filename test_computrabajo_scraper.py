# test_computrabajo_scraper.py
from scraping.job_scrapers.computrabajo_scraper import ComputrabajoScraper

def main():
    print("🚀 Probando ComputrabajoScraper con Requests...")
    
    scraper = ComputrabajoScraper()
    try:
        jobs = scraper.scrape("python", "Colombia", pages=1)
        print(f"Scraping completado: {len(jobs)} trabajos encontrados")
        
        # Mostrar los trabajos encontrados
        for i, job in enumerate(jobs):
            print(f"\n--- Trabajo {i+1} ---")
            print(f"Título: {job['title']}")
            print(f"Empresa: {job['company']}")
            print(f"Ubicación: {job['location']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()