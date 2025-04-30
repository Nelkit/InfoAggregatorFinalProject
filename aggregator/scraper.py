
from entities.news_article import NewsArticle
from entities.news_article import NewsArticle, NYTArticle,BBCArticle
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
            "GNews": self.scraping_GNews,
            "BBC News": self.scraping_bbc

        }

    def enrich_articles(self):
        for article in self.articles:
            # Try to find a scraper for the article's source
            scraper = self.scrapers.get(article.source)
            
            # If a scraper is available for the article's source
            if scraper:
                try:
                    # Execute the scraper function to get enriched data
                    enriched_data = scraper(article)

                    # Assign each enriched data value to the corresponding article attribute
                    for key, value in enriched_data.items():
                        setattr(article, key, value)

                except Exception as e:
                    # Handle any errors during the scraping process
                    print(f"Error scraping {article.source} ({article.url}): {e}")
            else:
                # If no scraper is available for the article's source, print a warning
                print(f"No scraper available for source: {article.source}")

    def get_enriched_articles(self) -> list[NewsArticle]:
        # Return the list of enriched articles
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


    def scraping_cnn(self, url: str) -> dict:
        # Realiza scraping de un artículo de CNN

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)

        # Extrae el contenido del artículo: adaptenlo según la estructura real de la página
        return {

    
            }
    def scraping_bbc(self, article: NewsArticle) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(article.url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract meta info
            title = soup.find("meta", property="og:title") or soup.find("title")
            title_text = title["content"] if title else "No title found"

            # Extract description from meta tags
            description = soup.find("meta", property="og:description") or soup.find("meta", name="description")
            description_text = description["content"] if description else "No description found"

            # Extract image URL from meta tags
            image = soup.find("meta", property="og:image")
            image_url = image["content"] if image else "No image found"

            # Extract article body (look for div with the text-block component)
            body = soup.find("div", {"data-component": "text-block"})
            paragraphs = body.find_all("p") if body else []
            body_text = "\n".join([p.get_text() for p in paragraphs])
            
            return {
                "title": title_text,
                "description": description_text,
                "image_url": image_url,
                "body": body_text  # Add this to pass to BBCArticle
            }

        except requests.RequestException as e:
            print(f"Error fetching BBC article: {e}")
            return {
                "title": None,
                "description": None,
                "image_url": None,
                "body": None
            }