# test_indeed_selenium.py
from scraping.job_scrapers.indeed_scraper import IndeedScraper

def main():
    print("🚀 Probando IndeedScraper con Selenium...")
    
    scraper = IndeedScraper()
    try:
        jobs = scraper.scrape("python", "Medellín", pages=1)
        print(f"Scraping completado: {len(jobs)} trabajos encontrados")
        
        # Mostrar los trabajos encontrados
        for i, job in enumerate(jobs):
            print(f"\n--- Trabajo {i+1} ---")
            print(f"Título: {job['title']}")
            print(f"Empresa: {job['company']}")
            print(f"Ubicación: {job['location']}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.selenium_scraper.close()

if __name__ == "__main__":
    main()