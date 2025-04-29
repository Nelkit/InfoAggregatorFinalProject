from entities.news_article import NewsArticle, NYTArticle
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
            "GNews": self.scraping_cnn,
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
                    enriched_data = scraper(article)

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

    def scraping_guardian(self, article: NewsArticle) -> dict:
        # Realiza scraping de un artículo de The Guardian
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        return {
            #"title": ""
            #"author": "",
            "content": soup.find('div', class_='article-body-viewer-selector').text.strip() if soup.find('div', class_='article-body-viewer-selector') else None,
            #"feature_image_url": "",
        }

    def scraping_nytimes(self, article: NYTArticle) -> dict:
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # creating a dictionary that contains the neccessary information from the article
        scrapping_results = {}
        # scrapping the author
        if article.author is None or article.author == '':
            scrapping_results["author"] = ' '.join([a.text.strip().title() for a in soup.find_all(attrs = {"itemprop" : "name"})])
        # scrapping the content
        if article.content is None or article.content == '':
            article_tag = soup.find('article')
            if article_tag:
                scrapping_results['content'] = ' '.join(p.text.strip() for p in article_tag.find_all('p'))
            else:
                scrapping_results['content'] = ' '.join(p.text.strip() for p in soup.find_all('p'))
        # scrappting title
        if article.title is None or article.title == '':
            if article.main != '':
                scrapping_results['title'] = article.main
            else:
                scrapping_results['title'] = soup.find('h1', attrs = {'data-testid' : 'headline'}).text.strip()
        # scrapping images
        if article.feature_image_url is None or article.feature_image_url == '':
            scrapping_results['feature_image_url'] = soup.find('img').get('src')
        return scrapping_results      

    def scraping_cnn(self, article: NewsArticle) -> dict:
        # Realiza scraping de un artículo de CNN
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

        }

    def scraping_bbc(self, article: NewsArticle) -> dict:
        # Realiza scraping de un artículo de BBC
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

        }