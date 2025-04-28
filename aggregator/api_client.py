from entities.news_article import NewsArticle, TheGuardianArticle, BBCArticle, NYTArticle, CNNArticle
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
            user_input (UserInput): The user input containing category and source.
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
    @st.cache_data
    def fetch_articles(_self, source: str, category:str, page_size: int = 3) -> list[BBCArticle]:
        try:
            params = {
                "api_token": _self.api_key,
                "search": f"{source}, {category}",
                "language": "en",
                "limit": page_size
            }

            response = requests.get(f"{_self.base_url}news/all", params=params)
            response.raise_for_status()

            response_json = response.json()

            # Debug: imprimir la respuesta completa
            import json
            print("📦 Respuesta de la API:")
            print(json.dumps(response_json, indent=2))

            articles_data = response_json.get("data")
            if not isinstance(articles_data, list):
                print("⚠️ 'data' no es una lista válida.")
                return []

            articles = []
            for item in articles_data:
                try:
                    article = BBCArticle.from_dict(item)
                    articles.append(article)
                except Exception as e:
                    print(f"⚠️ Error construyendo BBCArticle: {e}")
                    continue

            return articles
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")

class NYTNewsApi(APIClient):
    @st.cache_data
    def fetch_articles(
        _self,
        category: str,
    ) -> list[NYTArticle]:
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
            "api-key" : _self.api_key,
            "q" : category, # what are the articles about?
            "sort" : "best", # available options: best (default), newest, oldest, relevance
            "begin_date" : "20200101", # format (YYYYMMDD)
            "end_date" : datetime.today().strftime("%Y%m%d"),
            # "page" : 1, # optional parameter
            "fq" : 'type:("Article")' # special parameters that allows granular filters
            # types of fields can be found in https://developer.nytimes.com/docs/articlesearch-product/1/overview
        }
        headers = {
            "Accept" : "application/json"
        }
        try:
            response = requests.get(
                url = f"{_self.base_url}articlesearch.json",
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
            filtered_results = list(filter(lambda r: requests.get(r.get('link')).status_code == 200, google_results))
            if len(filtered_results) == 0:
                raise Exception(f"There are no available links for the criteria '{search_criteria}'")
            # changing the original attribute
            troublesome_article.url = filtered_results[0].get('link')
            return troublesome_article
        except Exception as e:
            raise e

class CNNNewsApi(APIClient):
    @st.cache_data
    def fetch_articles(_self, category: str, page_size: int = 10) -> list[CNNArticle]:
        """
        Fetches the latest news articles from The Guardian API.

        Args:
            user_input (UserInput): The user input containing category and source.
            page_size (int, optional): The number of articles to fetch. Defaults to 10.

        Returns:
            list[CNNArticle]: A list of CNNArticle objects.

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
                raise KeyError("Unexpected response structure from GNEWS API.")

            # create TheGuardianArticle objects
            print(response_json)
            articles = [CNNArticle(**item) for item in response_json["articles"]]

            return articles

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.HTTPError(f"Error fetching news: {e}")
        except KeyError as e:
            raise KeyError(f"Error parsing API response: {e}")