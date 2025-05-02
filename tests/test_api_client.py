import unittest

import requests

from aggregator.api_client import APIClient, TheGuardianApi
from unittest.mock import patch, MagicMock

from entities.news_article import TheGuardianArticle


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(api_key="dummy_key", base_url="https://example.com")
        self.the_guardian_api = TheGuardianApi(
            api_key="f6f96e89-7097-46c0-9266-5d2001202068",
            base_url="https://content.guardianapis.com/",
        )

    def test_fetch_sources_returns_expected_list(self):
        expected = ["All", "BBC News", "GNews", "The Guardian", "New York Times"]
        self.assertEqual(self.client.fetch_sources(), expected)

    def test_fetch_categories_returns_expected_list(self):
        expected = ["Technology", "World", "Business", "Politics", "Science", "Culture"]
        self.assertEqual(self.client.fetch_categories(), expected)

    #TODO Repetir estas tres pruebas para cada API
    # - BBCApi
    # - NYTNewsApi
    # - GNewsApi
    @patch("aggregator.api_client.requests.get")
    def test_fetch_articles_success(self, mock_get):
        # Mocking the API response JSON
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": {
                "status": "ok",
                "results": [
                    {
                        "id": "news/article1",
                        "type": "article",
                        "sectionId": "news",
                        "webTitle": "Sample Article",
                        "webUrl": "https://guardian.co.uk/article1",
                        "sectionName": "News",
                        "webPublicationDate": "2023-10-01T12:00:00Z",
                        "apiUrl": "https://content.guardianapis.com/news/article1",
                        "isHosted": False,
                        "fields": {
                            "bodyText": "Some content here"
                        }
                    }
                ]
            }
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Run method
        articles = self.the_guardian_api.fetch_articles(
            category="Technology",
        )

        # Assertions
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 1)
        self.assertIsInstance(articles[0], TheGuardianArticle)
        self.assertEqual(articles[0].title, "Sample Article")

    @patch("aggregator.api_client.requests.get")
    def test_fetch_articles_bad_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad request")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.the_guardian_api.fetch_articles(category="Technology")

    @patch("aggregator.api_client.requests.get")
    def test_fetch_articles_invalid_json_structure(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {}  # Missing expected keys
        mock_get.return_value = mock_response

        with self.assertRaises(KeyError):
            self.the_guardian_api.fetch_articles(category="Technology")

