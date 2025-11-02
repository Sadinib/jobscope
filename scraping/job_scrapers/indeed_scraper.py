from scraping.job_scrapers.base_job_scraper import BaseJobScraper
from scraping.selenium_scraper import SeleniumScraper
from datetime import datetime, timezone  
from urllib.parse import quote_plus
import time

class IndeedScraper(BaseJobScraper):
    def __init__(self):
        super().__init__("https://co.indeed.com/jobs")
        self.selenium_scraper = SeleniumScraper()

    def get_soup_selenium(self, url):
        return self.selenium_scraper.get_soup_selenium(url)
    
    def scrape(self, query="backend developer", location="Colombia", pages=1):
        all_jobs = []
        search_location = location
        
        try:
            for page in range(pages):
                start = page * 10
                url = f"{self.base_url}?q={quote_plus(query)}&l={quote_plus(search_location)}&start={start}"

                if page > 0:
                    time.sleep(8)
                
                soup = self.get_soup_selenium(url)
                if not soup:
                    print(f"No se pudo acceder a Indeed página {page + 1}")
                    continue

                jobs = soup.select("div[data-testid='slider_item']")
                if not jobs:
                    print(f"No se encontraron trabajos en Indeed página {page + 1}")
                    break

                page_saved = 0
                for job in jobs:
                    job_data = self.extract_job_data(job, query, search_location)
                    if job_data:
                        if self.save_job(job_data):
                            all_jobs.append(job_data)
                            page_saved += 1

                print(f"Indeed - Página {page + 1}: {page_saved}/{len(jobs)} trabajos guardados")
        
            print(f"Indeed completado: {len(all_jobs)} trabajos encontrados")
            return all_jobs
        
        finally:
            self.selenium_scraper.close()

    def extract_job_data(self, job_element, query, search_location):
        title = job_element.select_one("h2 a span")
        company = job_element.select_one("[data-testid='company-name']")
        job_location = job_element.select_one("[data-testid='text-location']")

        current_time = self.get_current_utc_time()
        
        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "company": company.get_text(strip=True) if company else "N/A",
            "location": job_location.get_text(strip=True) if job_location else "N/A",
            "source": "Indeed",
            "query": query,
            "search_location": search_location,
            "posted_at": current_time.isoformat(),
            "scraped_at": current_time.isoformat()
        }
    
    def close(self): 
        if hasattr(self, 'selenium_scraper'):
            self.selenium_scraper.close()