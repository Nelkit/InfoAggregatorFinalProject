

from entities.news_article import NewsArticle, TheGuardianArticle, NYTArticle
from entities.user_input import UserInput
import requests

class APIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    # Esta función simula la obtención de artículos de una API de noticias
    # TODO: implementar la funcion de obtener los articulos de la API de noticias real
    def fetch_articles(self, user_input: UserInput) -> list[NewsArticle]:
        category = user_input.category
        source = user_input.source

        news = []

        # Simulación de datos para la demostración
        for i in range(10):
            article = NewsArticle(
                title=f"Article {i + 1}",
                feature_image_url="",
                content=f"This is the content of article {i + 1}.",
                summary=f"Summary of article {i + 1}",
                author="Author Name",
                source=source,
                date="2023-10-01",
                url=f"https://example.com/article-{i + 1}",
            )
            news.append(article)

        # Implementar lógica de consumo del News API
        return news

    # Esta función simula la obtención de detalles de un artículo específico
    # TODO: implementar la funcion de obtener los detalles del articulo de la API de noticias
    def fetch_article_details(self, article_id):
        # Simulación de datos para la demostración
        article = NewsArticle(
            title=f"Article 1",
            feature_image_url="",
            content=f"This is the content of article 1.",
            summary=f"Summary of article 1",
            author="Author Name",
            source="source",
            date="2023-10-01",
            url=f"https://example.com/article-1",
        )
        return article

    def fetch_sources(self):
        # Simulación de fuentes para la demostración
        return [
            "All",
            "BBC News",
            "CNN News",
            "The Guardian",
            "New York Times",
        ]

    def fetch_categories(self):
        # Simulación de categorías para la demostración
        return [
            "Technology",
            "World",
            "Business",
            "Politics",
            "Science",
            "Culture"
        ]

#TODO Crear clases específicas para cada API de noticias
# -BBCNews
# -TheGuardian
# -newyorktimes
# -CNN
class TheGuardianApi(APIClient):

    def fetch_articles(self, user_input: UserInput, page_size: int = 10) -> list[TheGuardianArticle]:
        """
        Fetches the latest news articles from The Guardian API.

        Args:
            user_input (UserInput): The user input containing category and source.
            page_size (int, optional): The number of articles to fetch. Defaults to 10.

        Returns:
            list[TheGuardianArticle]: A list of TheGuardianArticle objects.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
            KeyError: If the response JSON is missing expected keys.
        """
        params = {
            "api-key": self.api_key,
            "page-size": page_size,
            "show-fields": "all",
        }
        if user_input.category:
            section = user_input.category
            params["section"] = section.lower()

        try:
            url = f"{self.base_url}search"

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

    def fetch_article_details(self, url):
        url = url.replace("https://www.theguardian.com/", self.base_url)
        params = {
            "api-key": self.api_key,
            "show-fields": "all",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        response_json = response.json()

        # Validate response structure
        if "response" not in response_json or "content" not in response_json["response"]:
            raise KeyError("Unexpected response structure from The Guardian API.")

        # Extract the relevant data
        response = response_json["response"]

        # create TheGuardianArticle objects
        item = response["content"]
        article = TheGuardianArticle(**item)

        return article

class BBCNewsApi(APIClient):

    def fetch_articles(self, user_input):
        # Implementar la lógica para obtener artículos de BBC News
        pass

    def fetch_article_details(self, article_id):
        # Implementar la lógica para obtener detalles de un artículo específico de BBC News
        pass

class NYTNewsArticles(APIClient):
    # override the fetch articles function
    def fetch_articles(
        self,
        user_input : UserInput
    ):
        """
        Fetches the lastests news articles from the NYT
        The API endpoint is the following: https://api.nytimes.com/svc/search/v2/articlesearch.json
        
        Args:
        - User input: class that contains the selected news source and category
        
        Returns:
        - List: list of 10 articles from the NYT
        
        Raises:
        - requests.exceptions.HTTPError: If the API request fails
        - KeyError: If the response JSON is missing "response" or "docs" in "response".
        """
        parameters = {
            "api-key" : self.api_key,
            "q" : user_input.category, # what are the articles about?
            "sort" : "newest", # available options: best (default), newest, oldest, relevance
            "begin_date" : "20200101", # format (YYYYMMDD)
            "end_date" : "20250401",
            "fq" : 'type:("Article")' # special parameters that allows granular filters
            # types of fields can be found in https://developer.nytimes.com/docs/articlesearch-product/1/overview
        }
        headers = {
            "Accept" : "application/json"
        }
        try:
            response = requests.get(
                url = self.base_url,
                params = parameters,
                headers = headers
            )
            response.raise_for_status()
            response_json = response.json()
            # Validate response structure
            if "response" not in response_json or "docs" not in response_json["response"]:
                raise KeyError("Unexpected response structure from The NYT API.")
            articles = [NYTArticle(**art) for art in response_json["response"]["docs"]]
            return articles
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")