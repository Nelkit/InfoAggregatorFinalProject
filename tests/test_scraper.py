import unittest
from unittest.mock import patch
from aggregator.scraper import ArticleScraper
from entities.news_article import NewsArticle

class TestArticleScraper(unittest.TestCase):

    def setUp(self):
        self.article = NewsArticle(
            title="",
            url="https://example.com",
            source="The Guardian",
            content="Some content",
            author="Someone",
            feature_image_url="None",
            summary="",
            date="2023-10-01",
        )
        self.scraper = ArticleScraper(articles=[self.article])

    @patch.object(ArticleScraper, 'scraping_guardian')
    def test_enrich_articles_with_valid_scraper(self, mock_scraping):

        self.scraper.enrich_articles()
        self.articles = self.scraper.get_enriched_articles()

        self.assertIsInstance(self.articles, list)



