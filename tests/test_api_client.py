import unittest

import requests

from aggregator.api_client import APIClient, TheGuardianApi, NYTNewsApi
from unittest.mock import patch, MagicMock

from entities.news_article import TheGuardianArticle, NYTArticle


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(api_key="dummy_key", base_url="https://example.com")
        self.the_guardian_api = TheGuardianApi(
            api_key="f6f96e89-7097-46c0-9266-5d2001202068",
            base_url="https://content.guardianapis.com/",
        )
        # added nyt api
        self.nyt_api = NYTNewsApi(
            api_key = 'zv2dhOM3UJMipTtusff6f1dD3GSxnEXe',
            base_url = 'https://api.nytimes.com/svc/search/v2/'
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
    def test_fetch_articles_sucess_nty(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "copyright": "Copyright (c) 2025 The New York Times Company. All Rights Reserved.",
            "response": {
                "docs": [
                    {
                        "abstract": "Extreme weather events",
                        "byline": {
                            "original": "By David Gelles and Austyn Gaffney"
                        },
                        "document_type": "article",
                        "headline": {
                            "main": "How Climate Change Is Supercharging Disasters",
                            "kicker": "",
                            "print_headline": "How Climate Change Is Supercharging Disasters"
                        },
                        "_id": "nyt://article/a09b3cd3-63b9-5df7-8563-a88bde75361f",
                        "keywords": [
                            {
                                "name": "Subject",
                                "value": "Wildfires",
                                "rank": 1
                            }
                        ],
                        "multimedia": {
                            "caption": "By Friday, the fires in California had consumed more than 30,000 acres and destroyed thousands of buildings.",
                            "credit": "Ariana Drehsler for The New York Times",
                            "default": {
                                "url": "https://static01.nyt.com/images/2025/01/10/multimedia/00CLI-LAFIRE-CLIMATE-sub-hkvw/00CLI-LAFIRE-CLIMATE-sub-hkvw-articleLarge.jpg",
                                "height": 400,
                                "width": 600
                            },
                            "thumbnail": {
                                "url": "https://static01.nyt.com/images/2025/01/10/multimedia/00CLI-LAFIRE-CLIMATE-sub-hkvw/00CLI-LAFIRE-CLIMATE-sub-hkvw-thumbStandard.jpg",
                                "height": 75,
                                "width": 75
                            }
                        },
                        "news_desk": "Climate",
                        "print_page": "1",
                        "print_section": "A",
                        "pub_date": "2025-01-10T19:54:24Z",
                        "section_name": "Climate",
                        "snippet": "Extreme weather events deadly heat waves, floods, fires and hurricanes",
                        "source": "The New York Times",
                        "subsection_name": "",
                        "type_of_material": "News",
                        "uri": "nyt://article/a09b3cd3-63b9-5df7-8563-a88bde75361f",
                        "web_url": "https://www.nytimes.com/2025/01/10/climate/california-fires-climate-change-disasters.html",
                        "word_count": 1609
                    }
                ],
                "metadata": {
                    "hits": 10000,
                    "offset": 0,
                    "time": 154
                }
            }
        }
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        # Run method
        articles = self.nyt_api.fetch_articles(
            category="Technology",
        )
        # Assertions
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 1)
        self.assertIsInstance(articles[0], NYTArticle)
        self.assertEqual(articles[0].title, "How Climate Change Is Supercharging Disasters")

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

