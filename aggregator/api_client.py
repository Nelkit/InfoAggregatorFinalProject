from entities.news_article import GNewsArticle, BBCArticle, NewsArticle, TheGuardianArticle, NYTArticle
from entities.user_input import UserInput
import requests
from datetime import datetime
import streamlit as st


class APIClient:
    """
    Base class for all news API clients.
    Provides common functionality and interface for fetching news articles.
    """
    def __init__(self, api_key, base_url):
        self.api_key = api_key  # API access key
        self.base_url = base_url  # Base URL for API requests

    def fetch_articles(self, source: str, category: str) -> list[NewsArticle]:
        """
        Simulates fetching articles (dummy implementation).
        Returns a list of dummy news articles for testing purposes.
        """
        news = []
        for i in range(10):
            article = NewsArticle(
                title=f"Article {i + 1}",
                feature_image_url="https://example.com/image.jpg",
                content=f"This is the content of article {i + 1}.",
                summary=f"Summary of article {i + 1}",
                author="Author Name",
                source="Dummy",
                date="2023-10-01",
                url=f"https://example.com/article-{i + 1}",
            )
            news.append(article)

        return news

    def fetch_sources(self) -> list[str]:
        """
        Returns a list of available news sources.
        """
        return [
            "All",
            "BBC News",
            "GNews",
            "The Guardian",
            "New York Times",
        ]

    def fetch_categories(self) -> list[str]:
        """
        Returns a list of available news categories.
        """
        return [
            "Technology",
            "World",
            "Business",
            "Politics",
            "Science",
            "Culture"
        ]


class TheGuardianApi(APIClient):
    @st.cache_data
    def fetch_articles(_self, category: str, _page_size: int = 10) -> list[TheGuardianArticle]:
        """
        Fetches the latest news articles from The Guardian API.

        Args:
            category (str): The news category to fetch articles for.
            _page_size (int, optional): The number of articles to fetch. Defaults to 10.

        Returns:
            list[TheGuardianArticle]: A list of TheGuardianArticle objects.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
            KeyError: If the response JSON is missing expected keys.
        """
        params = {
            "api-key": _self.api_key,
            "page-size": _page_size,
            "show-fields": "all",
        }

        section = category
        params["section"] = section.lower()

        try:
            url = f"{_self.base_url}search"

            response = requests.get(url, params=params)
            response.raise_for_status()
            response_json = response.json()

            if "response" not in response_json or "results" not in response_json["response"]:
                raise KeyError("Unexpected response structure from The Guardian API.")

            response = response_json["response"]
            articles = [TheGuardianArticle(**item) for item in response["results"]]

            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")

class BBCApi(APIClient):
    @st.cache_data
    def fetch_articles(_self, source: str, category: str, page_size: int = 3) -> list[BBCArticle]:
        """
        Fetches news articles from BBC News using the NewsAPI.org service.

        Args:
            source (str): The news source identifier.
            category (str): The news category to fetch articles for.
            page_size (int, optional): Number of articles to fetch. Defaults to 3.

        Returns:
            list[BBCArticle]: A list of BBCArticle objects.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
            KeyError: If the response JSON is missing expected keys.
        """
        try:
            params = {
                "apiKey": _self.api_key,
                "q": category,
                "language": "en",
                "pageSize": 10,
                "sources": "bbc-news"
            }

            response = requests.get("https://newsapi.org/v2/everything", params=params)
            response.raise_for_status()
            response_json = response.json()

            if "articles" not in response_json:
                raise KeyError("Unexpected response structure from NewsAPI.org.")

            articles_data = response_json["articles"]
            articles = []
            for item in articles_data:
                article_dict = {
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "url": item.get("url", ""),
                    "image_url": item.get("urlToImage", ""),
                    "published_at": item.get("publishedAt", ""),
                    "source": item.get("source", {}).get("name", "BBC News")
                }
                articles.append(BBCArticle.from_dict(article_dict))

            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")

class NYTNewsApi(APIClient):
    @st.cache_data
    def fetch_articles(_self, category: str) -> list[NYTArticle]:
        """
        Fetches the latest news articles from The New York Times API.

        Args:
            category (str): The news category to fetch articles for.

        Returns:
            list[NYTArticle]: A list of NYTArticle objects.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
            KeyError: If the response JSON is missing expected keys.
        """
        parameters = {
            "api-key": _self.api_key,
            "q": category,
            "sort": "best",
            "begin_date": "20200101",
            "end_date": datetime.today().strftime("%Y%m%d"),
            "fq": 'type:("Article")'
        }
        headers = {
            "Accept": "application/json"
        }
        try:
            response = requests.get(
                url=f"{_self.base_url}articlesearch.json",
                params=parameters,
                headers=headers
            )
            response.raise_for_status()
            response_json = response.json()

            if "response" not in response_json or "docs" not in response_json["response"]:
                raise KeyError("Unexpected response structure from The NYT API.")

            articles = [NYTArticle(**art) for art in response_json["response"]["docs"]]
            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")

class GNewsApi(APIClient):
    @st.cache_data
    def fetch_articles(_self, category: str, page_size: int = 10) -> list[GNewsArticle]:
        """
        Fetches the latest news articles from GNews API.

        Args:
            category (str): The news category to fetch articles for.
            page_size (int, optional): The number of articles to fetch. Defaults to 10.

        Returns:
            list[GNewsArticle]: A list of GNewsArticle objects.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
            KeyError: If the response JSON is missing expected keys.
        """
        category = category.lower()

        try:
            url = f"{_self.base_url}top-headlines?category={category}&apikey={_self.api_key}&lang=en"

            response = requests.get(url)
            response.raise_for_status()
            response_json = response.json()

            if "articles" not in response_json:
                raise KeyError("Unexpected response structure from GNews API.")

            articles = [GNewsArticle(**item) for item in response_json["articles"]]
            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")