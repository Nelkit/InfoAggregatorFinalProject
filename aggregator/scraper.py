from entities.news_article import NewsArticle
from bs4 import BeautifulSoup
import requests

class ArticleScraper:
    def __init__(self, articles: list[NewsArticle]):
        # Lista para guardar los artículos a enriquecer
        self.articles: list[NewsArticle] = articles

        # Diccionario que asocia cada fuente con su respectiva función de scraping
        self.scrapers = {
            "The Guardian": self.scraping_guardian,
            "New York Times": self.scraping_nytimes,
            "CNN News": self.scraping_cnn,
            "BBC News": self.scraping_bbc
        }

    def enrich_articles(self):
        # Itera sobre todos los artículos agregados
        for article in self.articles:
            # Obtiene la función de scraping según la fuente del artículo
            scraper = self.scrapers.get(article.source)

            if scraper:
                try:
                    # Ejecuta la función de scraping para obtener los datos enriquecidos
                    enriched_data = scraper(article.url)

                    # Asigna cada dato enriquecido al atributo correspondiente del artículo
                    for key, value in enriched_data.items():
                        setattr(article, key, value)
                except Exception as e:
                    # En caso de error en la solicitud o parsing, se muestra el mensaje
                    print(f"Error scraping {article.source} ({article.url}): {e}")
            else:
                # Si no hay scraper definido para esa fuente, se muestra advertencia
                print(f"No scraper available for source: {article.source}")

    def get_enriched_articles(self) -> list[NewsArticle]:
        # Devuelve la lista de artículos enriquecidos
        return self.articles

    def scraping_guardian(self, url: str) -> dict:
        # Realiza scraping de un artículo de The Guardian
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)
        #print(soup.prettify())

        return {
            #"title": ""
            #"author": "",
            "content": soup.find('div', class_='article-body-viewer-selector').text.strip() if soup.find('div', class_='article-body-viewer-selector') else None,
            #"feature_image_url": "",
        }

    def scraping_nytimes(self, url: str) -> dict:
        # Realiza scraping de un artículo de The New York Times
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

        }

    def scraping_cnn(self, url: str) -> dict:
        # Realiza scraping de un artículo de CNN
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

        }

    def scraping_bbc(self, url: str) -> dict:
        # Realiza scraping de un artículo de BBC
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

        }