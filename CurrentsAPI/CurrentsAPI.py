import requests
from CurrentsAPI.NewsResponse import NewsResponse
from CurrentsAPI.NewsItem import NewsItem

class CurrentsAPI:
	def __init__(self, api_key):
		self.api_key = api_key
		self.base_url = "https://api.currentsapi.services/v1/latest-news"

	def get_latest_news(self, category=None, language=None):
		params = {
			'apiKey': self.api_key,
			'category': category,
			'language': language
		}
		response = requests.get(self.base_url, params=params)
		if response.status_code != 200:
			raise Exception(f"Error fetching news: {response.status_code} - {response.text}")

		news_data = response.json()
		news_items = [NewsItem(**item) for item in news_data['news']]
		parser_response = NewsResponse(status=news_data['status'], news=news_items)

		return parser_response

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