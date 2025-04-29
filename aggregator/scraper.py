<<<<<<< Updated upstream
<<<<<<< Updated upstream
from entities.news_article import NewsArticle
=======
from entities.news_article import NewsArticle, NYTArticle
>>>>>>> Stashed changes
=======
from entities.news_article import NewsArticle
from entities.news_article import NewsArticle, NYTArticle
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
            "CNN News": self.scraping_cnn,
<<<<<<< Updated upstream
=======
            "GNews": self.scraping_GNews,
>>>>>>> Stashed changes
            "BBC News": self.scraping_bbc
=======
            "GNews": self.scraping_GNews,
            "BBC News (bbc-news)": self.scraping_bbc
>>>>>>> Stashed changes
        }

    def enrich_articles(self):
        # Itera sobre todos los artículos agregados
        for article in self.articles:
            # Obtiene la función de scraping según la fuente del artículo
            scraper = self.scrapers.get(article.source)

            if scraper:
                try:
                    # Ejecuta la función de scraping para obtener los datos enriquecidos
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                    enriched_data = scraper(article.url)
=======
                    enriched_data = scraper(article)
>>>>>>> Stashed changes
=======
                    enriched_data = scraper(article.url)
                    enriched_data = scraper(article)
>>>>>>> Stashed changes

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

    def scraping_nytimes(self, article: NewsArticle) -> dict:
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # getting the content
        article_tag = soup.find('article')
        if article_tag:
            content = ' '.join(p.text.strip() for p in article_tag.find_all('p'))
        else:
            # Fallback to all <p> tags
            content = ' '.join(p.text.strip() for p in soup.find_all('p'))
        # getting the title
        if soup.title and soup.title.text:
            title = soup.title.text.title().strip() # needs verification before adding it
        return {
            "content" : content,
            # "title" : title
        }        


    def scraping_GNews(self, url: str) -> dict:
        # Realiza scraping de un artículo de GNews
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(url)

        return {

        }

    def scraping_bbc(self, url: str) -> dict:
        # Realiza scraping de un artículo de BBC
<<<<<<< Updated upstream
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

<<<<<<< Updated upstream
        }

    def scraping_cnn(self, url: str) -> dict:
        # Realiza scraping de un artículo de CNN
=======
>>>>>>> Stashed changes
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

        }

<<<<<<< Updated upstream
    def scraping_bbc(self, url: str) -> dict:
        # Realiza scraping de un artículo de BBC
=======
    def scraping_cnn(self, url: str) -> dict:
        # Realiza scraping de un artículo de CNN
>>>>>>> Stashed changes
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        }
=======
        }

    def scraping_bbc(self, url: str) -> dict:
        print(f"Starting BBC scraping for URL: {url}")
        

        response = requests.get(url)
        print(f"Response status: {response.status_code}")
            
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content
            content_blocks = soup.find_all(['p', 'h2'], class_=['ssrcss-1q0x1qg-Paragraph', 'ssrcss-1f3bvyz-StyledHeading'])
            content = "\n".join([block.get_text().strip() for block in content_blocks])
            print(f"Content found: {bool(content)}")
                
                # Extract image
            image_url = None
            image_element = soup.find('img', class_='ssrcss-evoj7m-Image')
            if image_element and image_element.get('src'):
                    image_url = image_element.get('src')
                    print(f"Found image with class: {image_url}")
            else:
                    image_tag = soup.find('img')
                    if image_tag and image_tag.get('src'):
                        image_url = image_tag['src']
                        print(f"Found generic image: {image_url}")
                    else:
                        print("No image found")
                
            return {
                    "content": content,
                    "feature_image_url": image_url
                }
            
>>>>>>> Stashed changes
