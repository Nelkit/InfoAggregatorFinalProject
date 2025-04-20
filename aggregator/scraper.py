from entities.news_article import NewsArticle
from bs4 import BeautifulSoup
import requests

class ArticleScraper:
    def enrich_articles(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        for article in articles:
            # llamar cualquier funcion para hacer scraping
            if article.source == "The Guardian":
                pass
            elif article.source == "New York Times":
                pass
            elif article.source == "CNN News":
                pass
            elif article.source == "BBC News":
                pass

        return articles
