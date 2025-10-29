import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        }

    def get_soup(self, url):
        try:
            response = self.session.get(url, timeout = 10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except HTTPError as e:
            print(f"Error HTTP {response.status_code}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {url}: {e}")
            return None