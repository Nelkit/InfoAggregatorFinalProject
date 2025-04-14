import unittest
from aggregator.api_client import NewsAPIClient

class TestNewsAPIClient(unittest.TestCase):
    def test_fetch_articles(self):
        client = NewsAPIClient()
        results = client.fetch_articles({
            "category": "Tech",
            "source": "",
            "limit": 5
        })
        self.assertIsInstance(results, list)