
from entities.news_article import GNewsArticle,BBCArticle, NewsArticle, TheGuardianArticle, NYTArticle
from entities.user_input import UserInput
import requests

from entities.user_input import UserInput
import requests
from datetime import datetime
import streamlit as st

class APIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key            # Clave de acceso a la API
        self.base_url = base_url          # URL base de la API

    def fetch_articles(self, user_input: UserInput) -> list[NewsArticle]:

        # Simulación de artículos
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
        Devuelve una lista de fuentes disponibles (simuladas).
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
        Devuelve una lista de categorías disponibles (simuladas).
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
            category (str): The category of news to fetch.
            page_size (int, optional): The number of articles to fetch. Defaults to 10.
            page_size (int, optional): The number of articles to fetch. Defaults to 10.

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
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            response_json = response.json()

            # Validate response structure
            if "response" not in response_json or "results" not in response_json["response"]:
                raise KeyError("Unexpected response structure from The Guardian API.")

            # Extract the relevant data
            response = response_json["response"]

            # create TheGuardianArticle objects
            articles = [TheGuardianArticle(**item) for item in response["results"]]

            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")

class BBCApi(APIClient):
    def fetch_articles(self, category: str, page_size: int = 10) -> list[BBCArticle]:
        try:
            params = {
                "apikey": self.api_key,
                "category": category,
                "source" : "bbc-news",
                "language": "en",
                "pageSize": page_size
            }
            
            response = requests.get("https://newsapi.org/v2/everything?", params=params)
            response.raise_for_status()

            response_json = response.json()

            # Debug: imprimir la respuesta completa

            # Assuming you already have the response JSON object
            articles_data = response_json.get("articles")  # Access the 'articles' key

            articles_data = response_json.get("data")
            # Validate that 'articles' contains a list
            if not isinstance(articles_data, list):
                print("⚠️ 'data' no es una lista válida.")
                print("⚠️ 'articles' is not a valid list.")
                return []

           
            try:
                # Assuming BBCArticle accepts dictionary unpacking (**item)
                articles = [BBCArticle(**item) for item in articles_data]
                
                return articles
 
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")


class GoogleSearchArticles(APIClient):
    """
    This is a complementary class that searches google articles according to the title when not available for webscraping
    """
    def fetch_alternative_sources(self, troublesome_article : NYTArticle) -> NYTArticle:
        """
        Fetches the results of a google search based on an article that is not available due to paywall or other restrictions
        The API endpoint is the following: https://serpapi.com/search
        
        Args:
        - NYTArticle: class that contains the all the necessary fields for the search
        
        Returns:
        - NYTArticle: class that contains a different url for future webscrapping
        
        Raises:
        - requests.exceptions.HTTPError: If the API request fails
        - KeyError: If the response JSON is missing "organic_results", empty organic results, or not available links (response 200).
        
        """
        selected_attributes = ['title', 'main', 'kicker', 'summary']
        search_criteria = next((getattr(troublesome_article, attribute) for attribute in selected_attributes if getattr(troublesome_article, attribute) is not None), None)
        try:
            if search_criteria is None:
                raise Exception("There is no search criteria to filter")
            parameters = {
                "api_key" : self.api_key,
                "q" : search_criteria,
                "location" : "Sydney, Australia"
            }
            response = requests.get(
                url = self.base_url,
                params = parameters,
            )
            response.raise_for_status()
            response_json = response.json()
            if "organic_results" not in response_json or response_json['organic_results'] == []:
                raise KeyError("Unexpected response structure from SerpApi")
            # list that has all the results related to the query
            google_results = response_json['orginic_results']
            # filtered only the results that are accesible
            google_results = response_json['organic_results']
            if len(filtered_results) == 0:
                raise Exception(f"There are no available links for the criteria '{search_criteria}'")
            # changing the original attribute
            troublesome_article.url = filtered_results[0].get('link')
            return troublesome_article
        except Exception as e:
            raise e

class GNewsApi(APIClient):
    @st.cache_data
    def fetch_articles(_self, category: str, page_size: int = 10) -> list[GNewsArticle]:
        """
        Fetches the latest news articles from The Guardian API.

        Args:
            user_input (UserInput): The user input containing category and source.
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
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            response_json = response.json()

            # Validate response structure
            if "articles" not in response_json:
                raise KeyError("Unexpected response structure from GNews API.")

            # create TheGuardianArticle objects
            print(response_json)
            articles = [GNewsArticle(**item) for item in response_json["articles"]]

            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")