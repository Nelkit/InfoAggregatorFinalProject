import unittest
from aggregator.api_client import APIClient, TheGuardianApi
from unittest.mock import patch, Mock


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(api_key="dummy_key", base_url="https://example.com")

    def test_fetch_sources_returns_expected_list(self):
        expected = ["All", "BBC News", "GNews", "The Guardian", "New York Times"]
        self.assertEqual(self.client.fetch_sources(), expected)

    def test_fetch_categories_returns_expected_list(self):
        expected = ["Technology", "World", "Business", "Politics", "Science", "Culture"]
        self.assertEqual(self.client.fetch_categories(), expected)


