from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium. webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random

class SeleniumScraper:
    def __init__(self):
        self._setup_driver()

    def _setup_driver(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = chrome_options
        )

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_soup_selenium(self, url):
        try:
            print(f"Selenium accediendo a: {url}")
            self.driver.get(url)
            
            # Comportamiento más humano - scroll y delays aleatorios
            time.sleep(random.uniform(3, 6))
            
            # Hacer scroll para cargar contenido
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(2, 4))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            
            # DEBUG: Ver qué hay realmente en la página
            page_title = self.driver.title
            page_source = self.driver.page_source
            print(f"Título de la página: {page_title}")
            print(f"Longitud del HTML: {len(page_source)} caracteres")
            
            # Buscar diferentes selectores posibles
            selectors_to_try = [
                "div.job_seen_beacon",
                "div[data-testid='slider_item']", 
                "div.cardOutline",
                "div.result",
                ".jobsearch-SerpJobCard"
            ]
            
            for selector in selectors_to_try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Encontrados {len(elements)} elementos con selector: {selector}")
                    break
            else:
                print("No se encontraron elementos con ningún selector")
                # DEBUG: Guardar HTML para análisis
                with open("debug_page.html", "w", encoding="utf-8") as f:
                    f.write(page_source)
                print("HTML guardado en debug_page.html para análisis")
            
            return BeautifulSoup(page_source, "lxml")
            
        except Exception as e:
            print(f"Error con Selenium: {e}")
            return None
        
    def close(self):
        if self.driver:
            self.driver.quit()