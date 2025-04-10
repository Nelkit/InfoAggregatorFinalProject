import requests

from TheGuardianAPI.GuardianArticle import GuardianArticle
from TheGuardianAPI.GuardianResponse import GuardianResponse, ApiResponse


class TheGuardianAPI:
	"""
	The Guardian API class to interact with The Guardian's public API.
	"""

	def __init__(self, api_key):
		"""
		Initializes the TheGuardianAPI instance with the provided API key.

		Args:
			api_key (str): The API key for The Guardian API.
		"""
		self.api_key = api_key
		self.base_url = "https://content.guardianapis.com/"

	def get_latest_news(self, section=None, page_size=10):
		"""
		Fetches the latest news articles from The Guardian API.

		Args:
			section (str, optional): The section of news to fetch. Defaults to None.
			page_size (int, optional): The number of articles to fetch. Defaults to 10.
		"""
		params = {
			'api-key': self.api_key,
			'page-size': page_size,
			'show-fields': 'all'
		}
		if section:
			params['section'] = section

		response = requests.get(f"{self.base_url}search", params=params)
		if response.status_code != 200:
			raise Exception(f"Error fetching news: {response.status_code} - {response.text}")

		news_data = response.json()

		results = [GuardianArticle(**item) for item in news_data["response"]["results"]]
		response_data = GuardianResponse(results=results, **{k: v for k, v in news_data["response"].items() if k != "results"})
		api_response = ApiResponse(response=response_data)
		return api_response

	def get_categories(self):
		categories = [
			"business",
			"entertainment",
			"general",
			"health",
			"science",
			"sports",
			"technology"
		]
		return categories