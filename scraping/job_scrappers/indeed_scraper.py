from scraping.job_scrappers.base_job_scrapper import BaseJobScraper
from datetime import datetime, timezone  
from urllib.parse import quote_plus
import time

class IndeedScraper(BaseJobScraper):
    def __init__(self):
        super().__init__("https://co.indeed.com/jobs")
    
    def scrape(self, query="backend developer", location="Colombia", pages=1):
        all_jobs = []
        search_location = location
        
        for page in range(pages):
            start = page * 10
            url = f"{self.base_url}?q={quote_plus(query)}&l={quote_plus(search_location)}&start={start}"

            if page > 0:
                time.sleep(8)
            
            soup = self.get_soup(url)
            if not soup:
                print(f"No se pudo acceder a Indeed página {page + 1}")
                continue

            jobs = soup.select("div.job_seen_beacon")
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
    
    def extract_job_data(self, job_element, query, search_location):
        title = job_element.select_one("h2.jobTitle span")
        company = job_element.select_one("span.companyName")
        job_location = job_element.select_one("div.companyLocation")

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
