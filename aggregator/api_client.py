

from entities.news_article import NewsArticle, TheGuardianArticle
from entities.user_input import UserInput
import requests

from entities.news_article import NewsArticle, TheGuardianArticle
from entities.user_input import UserInput
import requests

class APIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key            # Clave de acceso a la API
        self.base_url = base_url          # URL base de la API

    def fetch_articles(self, user_input: UserInput) -> list[NewsArticle]:
        """
        Obtiene una lista de artículos según la categoría y fuente proporcionadas por el usuario.
        Simula una llamada a la API (debes implementar la lógica real para producción).

        Args:
            user_input (UserInput): Entrada del usuario con filtros.

        Returns:
            list[NewsArticle]: Lista de artículos.
        """
        category = user_input.category
        source = user_input.source

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
            "CNN News",
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


class BBCNewsApi(APIClient):

    def fetch_articles(self, user_input):
        # Implementar la lógica para obtener artículos de BBC News
        pass

class CNNNewsApi(APIClient):

    def fetch_articles(self, user_input):
        # Implementar la lógica para obtener artículos de CNN News
        pass
