from scraping.job_scrapers.base_job_scraper import BaseJobScraper
from datetime import datetime,timezone
from urllib.parse import quote_plus

class ComputrabajoScraper(BaseJobScraper):
    def __init__(self):
        super().__init__("https://co.computrabajo.com")

    def scrape(self,query="desarrollador",location="Colombia",pages=1):
        all_jobs=[]
        search_location = location

        for page in range(pages):
            url = (f"{self.base_url}/trabajo-de-{quote_plus(query)}-en-{quote_plus(search_location)}?p={page+1}")

            soup = self.get_soup(url)

            if not soup:
                print(f"No se pudo acceder a Computrabajo página {page+1}")
                continue

            jobs = soup.select("article.box_offer")

            if not jobs:
                print(f"No se encontraron trabajos en Computrabajo página {page+1}")

                break

            print(f"Encontrados {len(jobs)} trabajos en Computrabajo página {page+1}")

            page_saved = 0
            for job in jobs:
                job_data = self.extract_job_data(job, query, search_location)
                if job_data:
                    if self.save_job(job_data):
                        all_jobs.append(job_data)
                        page_saved += 1
             
            print(f"Computrabajo - Página {page+1}:{page_saved}/{len(jobs)} trabajos guardados")

        print(f"Computrabajo completado: {len(all_jobs)} trabajos encontrados")
        return all_jobs
    
    def extract_job_data(self, job_element, query, search_location):
        title = job_element.select_one("h2 a")
        company = job_element.select_one("p.dFlex a")
        job_location = job_element.select_one("p.fs16 span")

        current_time = self.get_current_utc_time()

        location_text = job_location.get_text(strip=True) if job_location else "N/A"
        if location_text and any(c.isdigit() for c in location_text) and ',' in location_text:
            location_text = "N/A"
        
        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "company": company.get_text(strip=True) if company else "N/A",
            "location": job_location.get_text(strip=True) if job_location else "N/A",
            "source": "Computrabajo",
            "query": query,
            "search_location": search_location,
            "posted_at": current_time.isoformat(),
            "scraped_at": current_time.isoformat()
        }
