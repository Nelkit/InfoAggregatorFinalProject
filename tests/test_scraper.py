import unittest
from unittest.mock import patch, Mock
from aggregator.scraper import ArticleScraper
from entities.news_article import NewsArticle, NYTArticle, BBCArticle


class TestArticleScraper(unittest.TestCase):
    
    def setUp(self):
        """Set up test data for ArticleScraper class"""
        # Create test articles for different sources
        self.guardian_article = NewsArticle(
            title="Guardian Test",
            feature_image_url="https://example.com/guardian.jpg",
            content=None,
            summary="Guardian summary",
            author="Guardian Author",
            source="The Guardian",
            date="2024-03-20",
            url="https://www.theguardian.com/australia-news/2025/may/10/what-next-for-teal-independent-candidates-after-2025-federal-election"
        )

        self.nyt_article = NYTArticle(
            abstract="NYT summary",
            byline={"original": None},
            document_type="article",
            headline={"print_headline": "NYT Test", "main": "Main Headline", "kicker": "Kicker"},
            _id="nyt-123",
            keywords=[],
            multimedia={"default": {"url": None}},
            news_desk="Foreign",
            print_page="1",
            print_section="A",
            pub_date="2024-03-20",
            section_name="World",
            snippet="NYT snippet",
            source="New York Times",
            subsection_name="",
            type_of_material="News",
            uri="nyt://article/123",
            web_url="https://www.nytimes.com/2025/05/10/business/us-china-talks-trump-tariffs.html",
            word_count=500
        )

        self.bbc_article = BBCArticle(
            uuid="bbc-123",
            title="BBC Test",
            description="BBC description",
            url="https://www.bbc.com/news/articles/c2e3d888p44o",
            image_url="",
            published_at="2024-03-20",
            source="BBC News",
            content="BBC content",
            body=""
        )

        self.test_articles = [
            self.guardian_article,
            self.nyt_article,
            self.bbc_article
        ]

    @patch('requests.get')
    def test_guardian_scraping(self, mock_get):
        """Test scraping of Guardian articles"""
        # Mock HTML response for Guardian
        mock_html = """
        <div class="article-body-viewer-selector">
            <p>This is the Guardian article content</p>
        </div>
        """
        mock_response = Mock()
        mock_response.content = mock_html
        mock_get.return_value = mock_response

        scraper = ArticleScraper([self.guardian_article])
        enriched_articles = scraper.get_enriched_articles()

        self.assertEqual(enriched_articles[0].content, "This is the Guardian article content")
        mock_get.assert_called_once_with(self.guardian_article.url)

    @patch('requests.get')
    def test_nyt_scraping(self, mock_get):
        """Test scraping of NYT articles"""
        # Mock HTML response for NYT
        mock_html = """
        <article>
            <p>This is the NYT article content</p>
        </article>
        <h1 data-testid="headline">NYT Headline</h1>
        <img src="https://example.com/nyt.jpg">
        <span itemprop="name">Nyt Author</span>
        """
        mock_response = Mock()
        mock_response.content = mock_html
        mock_get.return_value = mock_response

        scraper = ArticleScraper([self.nyt_article])
        enriched_articles = scraper.get_enriched_articles()

        self.assertEqual(enriched_articles[0].content, "This is the NYT article content")
        self.assertEqual(enriched_articles[0].author, "Nyt Author")
        self.assertEqual(enriched_articles[0].feature_image_url, "https://example.com/nyt.jpg")
        mock_get.assert_called_once_with(self.nyt_article.url)

    @patch('requests.get')
    def test_bbc_scraping(self, mock_get):
        """Test scraping of BBC articles"""
        # Mock HTML response for BBC
        mock_html = """
        <meta property="og:title" content="BBC Title">
        <meta property="og:description" content="BBC Description">
        <meta property="og:image" content="https://example.com/bbc.jpg">
        <div data-component="text-block">
            <p>This is the BBC article content</p>
            <p>More content here</p>
        </div>
        """
        mock_response = Mock()
        mock_response.content = mock_html
        mock_get.return_value = mock_response

        scraper = ArticleScraper([self.bbc_article])
        enriched_articles = scraper.get_enriched_articles()

        self.assertEqual(enriched_articles[0].title, "BBC Title")
        self.assertEqual(enriched_articles[0].description, "BBC Description")
        self.assertEqual(enriched_articles[0].image_url, "https://example.com/bbc.jpg")
        self.assertEqual(enriched_articles[0].body, "This is the BBC article content\nMore content here")

    @patch('requests.get')
    def test_scraping_error_handling(self, mock_get):
        """Test error handling during scraping"""
        # Mock a failed request
        mock_get.side_effect = Exception("Connection error")

        scraper = ArticleScraper(self.test_articles)
        enriched_articles = scraper.get_enriched_articles()

        # Verify that articles remain unchanged when scraping fails
        self.assertEqual(enriched_articles[0].content, None)
        self.assertEqual(enriched_articles[1].author, None)

if __name__ == '__main__':
    unittest.main()





