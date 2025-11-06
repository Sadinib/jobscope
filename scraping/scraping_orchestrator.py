from scraping.job_scrapers.computrabajo_scraper import ComputrabajoScraper
from scraping.job_scrapers.indeed_scraper import IndeedScraper

class ScrapingOrchestrator:
    @staticmethod
    def run_full_scraping(query="python", location="Colombia", pages=1):
        job_count =0
        jobs = []

        #Computrabajo
        compu_scraper = ComputrabajoScraper()
        compu_jobs = compu_scraper.scrape(query, location, pages)
        job_count += len(compu_jobs)
        jobs.extend(compu_jobs)
        print(f"Computrbajo: {len(compu_jobs)} trabajos")

        #Indeed
        indeed_scraper = IndeedScraper()
        indeed_jobs = indeed_scraper.scrape(query, location, pages)
        job_count += len(indeed_jobs)
        jobs.extend(indeed_jobs)
        indeed_scraper.selenium_scraper.close()
        print(f"Indeed: {len(indeed_jobs)} trabajos")

        return job_count, jobs
    
    @staticmethod
    def clean_old_jobs():
        from scraping.job_scrapers.base_job_scraper import BaseJobScraper
        deleted_count = BaseJobScraper.clean_expired_jobs()
        print(f"Limpieza completada: {deleted_count} trabajos eliminados")
        return deleted_count

