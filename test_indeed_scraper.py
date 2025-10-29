# test_indeed.py
from scraping.job_scrappers.indeed_scraper import IndeedScraper

if __name__ == "__main__":
    scraper = IndeedScraper()
    
    print("Probando IndeedScraper")
    jobs = scraper.scrape("python", "Medellín", pages=1)
    
    print(f"Encontrados {len(jobs)} trabajos")
    
    # Probar limpieza también
    scraper.clean_expired_jobs()