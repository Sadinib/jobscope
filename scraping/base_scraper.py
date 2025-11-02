import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import time
import random


class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.setup_hearders()

    def setup_hearders(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })


    def get_soup(self, url, delay=True):
        try:
            # Rotar User-Agent
            current_ua = random.choice(self.user_agents)
            self.session.headers.update({'User-Agent': current_ua})
            
            # Delay aleatorio entre requests
            if delay:
                time.sleep(random.uniform(2, 4))
            
            response = self.session.get(url, timeout=10)
            
            # Si recibimos 403, intentar con diferentes headers
            if response.status_code == 403:
                print("Recibido 403, intentando con headers alternativos...")
                return self._retry_with_alternative_headers(url)
                
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
            
        except HTTPError as e:
            print(f"Error HTTP {response.status_code}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {url}: {e}")
            return None

    def _retry_with_alternative_headers(self, url):
        alternative_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            time.sleep(5)  # Esperar más antes del reintento
            response = requests.get(url, headers=alternative_headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error también con headers alternativos: {e}")
            return None