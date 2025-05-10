from entities.news_article import NewsArticle, NYTArticle
from bs4 import BeautifulSoup
import requests

class ArticleScraper:
    """
    Class responsible for enriching news articles with additional content through web scraping.
    Supports multiple news sources including The Guardian, New York Times, GNews, and BBC News.
    """

    def __init__(self, articles: list[NewsArticle]):
        """
        Initialize the ArticleScraper with a list of articles to enrich.

        Args:
            articles (list[NewsArticle]): List of news articles to be enriched with additional content
        """
        self.articles: list[NewsArticle] = articles

        # Dictionary mapping news sources to their respective scraping functions
        self.scrapers = {
            "The Guardian": self.scraping_guardian,
            "New York Times": self.scraping_nytimes,
            "GNews": self.scraping_GNews,
            "BBC News": self.scraping_bbc
        }

        self.enrich_articles()

    def enrich_articles(self):
        """
        Enriches all articles with additional content by applying the appropriate scraping function
        based on the article's source.
        """
        for article in self.articles:
            scraper = self.scrapers.get(article.source)

            if scraper:
                try:
                    # Apply scraping function to get enriched data
                    enriched_data = scraper(article)

                    # Update article attributes with enriched data
                    for key, value in enriched_data.items():
                        setattr(article, key, value)
                except Exception as e:
                    print(f"Error scraping {article.source} ({article.url}): {e}")
            else:
                print(f"No scraper available for source: {article.source}")

    def get_enriched_articles(self) -> list[NewsArticle]:
        """
        Returns the list of enriched articles.

        Returns:
            list[NewsArticle]: List of articles with enriched content
        """
        return self.articles

    def scraping_guardian(self, article: NewsArticle) -> dict:
        """
        Scrapes content from a The Guardian article.

        Args:
            article (NewsArticle): The article to scrape

        Returns:
            dict: Dictionary containing the scraped content
        """
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        return {
            "content": soup.find('div', class_='article-body-viewer-selector').text.strip() 
                      if soup.find('div', class_='article-body-viewer-selector') else None,
        }

    def scraping_nytimes(self, article: NYTArticle) -> dict:
        """
        Scrapes content from a New York Times article.

        Args:
            article (NYTArticle): The article to scrape

        Returns:
            dict: Dictionary containing the scraped content including author, content, title, and image
        """
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        scrapping_results = {}

        # Scrape author if not available
        if article.author is None or article.author == '':
            scrapping_results["author"] = ' '.join([a.text.strip().title() 
                                                  for a in soup.find_all(attrs={"itemprop": "name"})])

        # Scrape content if not available
        if article.content is None or article.content == '':
            article_tag = soup.find('article')
            if article_tag:
                scrapping_results['content'] = ' '.join(p.text.strip() for p in article_tag.find_all('p'))
            else:
                scrapping_results['content'] = ' '.join(p.text.strip() for p in soup.find_all('p'))

        # Scrape title if not available
        if article.title is None or article.title == '':
            if article.main != '':
                scrapping_results['title'] = article.main
            else:
                scrapping_results['title'] = soup.find('h1', attrs={'data-testid': 'headline'}).text.strip()

        # Scrape image if not available
        if article.feature_image_url is None or article.feature_image_url == '':
            scrapping_results['feature_image_url'] = soup.find('img').get('src')

        return scrapping_results

    def scraping_GNews(self, url: str) -> dict:
        """
        Scrapes content from a GNews article.

        Args:
            url (str): URL of the article to scrape

        Returns:
            dict: Dictionary containing the scraped content
        """
        return {}

    def scraping_bbc(self, article: NewsArticle) -> dict:
        """
        Scrapes content from a BBC News article.

        Args:
            article (NewsArticle): The article to scrape

        Returns:
            dict: Dictionary containing the scraped content including title, description, image, and body
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(article.url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract meta information
            title = soup.find("meta", property="og:title") or soup.find("title")
            title_text = title["content"] if title else "No title found"

            description = soup.find("meta", property="og:description") or soup.find("meta", name="description")
            description_text = description["content"] if description else "No description found"

            image = soup.find("meta", property="og:image")
            image_url = image["content"] if image else "No image found"

            # Extract article body
            body = soup.find("div", {"data-component": "text-block"})
            paragraphs = body.find_all("p") if body else []
            body_text = "\n".join([p.get_text() for p in paragraphs])

            return {
                "title": title_text,
                "description": description_text,
                "image_url": image_url,
                "body": body_text
            }

        except requests.RequestException as e:
            print(f"Error fetching BBC article: {e}")
            return {
                "title": None,
                "description": None,
                "image_url": None,
                "body": None
            }