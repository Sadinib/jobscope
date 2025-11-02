from abc import ABC, abstractmethod
from scraping.base_scraper import BaseScraper
from db.db import db
from datetime import datetime, timezone, timedelta
from urllib.parse import quote_plus

class BaseJobScraper(BaseScraper, ABC):
    def __init__(self, base_url):
        super().__init__(base_url)

    def get_current_utc_time(self):
        return datetime.now(timezone.utc)
    
    def save_job(self, job_data):
        try:
            current_time = self.get_current_utc_time()
            job_data["scraped_at"] = current_time
            job_data.setdefault("posted_at", current_time.isoformat())

            existing = db.jobs.find_one({
                "title": job_data["title"],
                "company": job_data["company"],
                "source": job_data["source"]
            })

            if not existing:
                db.jobs.insert_one(job_data)
                return True
            return False
        except Exception as e:
            print(f"Error guardando trabajos: {e}")
            return False
        
    def clean_expired_jobs(self):
        try:
            limit_date = self.get_current_utc_time() - timedelta(days=3)

            delete = db.jobs.delete_many({
                "scraped_at": {"$lt": limit_date}
            })
            print(f"Eliminados {delete.deleted_count} trabajos antiguos")

            if delete.acknowledged:
                print ("Operacion confirmada por MongoDB")
            else:
                print ("Operacion invalida")

        except Exception as e:
            print (f"Error la operación {e} no confirmada")
            return None

        
    @abstractmethod
    def scrape(self, query, location, pages):
        pass