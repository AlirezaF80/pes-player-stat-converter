import requests
from bs4 import BeautifulSoup


class Scraper:
    @staticmethod
    def __scrape(url: str):
        pass

    @staticmethod
    def get_page_souped(url: str) -> BeautifulSoup:
        if not str:
            raise Exception('URL string is None!')
        try:
            page = requests.get(url)
        except Exception as ex:
            raise Exception("{URL} request failed! " + str(ex))
        return BeautifulSoup(page.content, 'html.parser')
