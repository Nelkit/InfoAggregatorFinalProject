import unittest
from datetime import datetime
from entities.news_article import NewsArticle, TheGuardianArticle, NYTArticle, BBCArticle, GNewsArticle

class TestNewsArticle(unittest.TestCase):
    def setUp(self):
        """Set up test data for base NewsArticle class"""
        self.article = NewsArticle(
            title="Test Article",
            feature_image_url="https://example.com/image.jpg",
            content="This is the full content of the article.",
            summary="This is a summary",
            author="John Doe",
            source="Test Source",
            date="2024-03-20",
            url="https://example.com/article"
        )

    def test_article_initialization(self):
        """Test that article is initialized with correct attributes"""
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.feature_image_url, "https://example.com/image.jpg")
        self.assertEqual(self.article.content, "This is the full content of the article.")
        self.assertEqual(self.article.summary, "This is a summary")
        self.assertEqual(self.article.author, "John Doe")
        self.assertEqual(self.article.source, "Test Source")
        self.assertEqual(self.article.date, "2024-03-20")
        self.assertEqual(self.article.url, "https://example.com/article")

    def test_get_id(self):
        """Test that get_id returns the correct URL"""
        self.assertEqual(self.article.get_id(), "https://example.com/article")

    def test_get_article_preview_md(self):
        """Test that article preview is generated correctly"""
        preview = self.article.get_article_preview_md(limit=50)
        self.assertIn("### Test Article", preview)
        self.assertIn("**Source:** Test Source", preview)
        self.assertIn("**Date:** 2024-03-20", preview)
        self.assertIn("This is a summary...", preview)

    def test_get_article_full_md(self):
        """Test that full article markdown is generated correctly"""
        full_md = self.article.get_article_full_md()
        self.assertIn("**Source:** Test Source", full_md)
        self.assertIn("**Date:** 2024-03-20", full_md)
        self.assertIn("This is the full content of the article.", full_md)

class TestTheGuardianArticle(unittest.TestCase):
    def setUp(self):
        """Set up test data for TheGuardianArticle class"""
        self.fields = {
            'thumbnail': 'https://example.com/guardian.jpg',
            'body': 'Guardian article content',
            'byline': 'Guardian Author'
        }
        self.article = TheGuardianArticle(
            id="guardian-123",
            type="article",
            sectionId="world",
            sectionName="World",
            webPublicationDate="2024-03-20",
            webTitle="Guardian Test Article",
            webUrl="https://guardian.com/article",
            apiUrl="https://guardian.com/api/article",
            fields=self.fields,
            isHosted=True
        )

    def test_guardian_initialization(self):
        """Test that Guardian article is initialized with correct attributes"""
        self.assertEqual(self.article.id, "guardian-123")
        self.assertEqual(self.article.type, "article")
        self.assertEqual(self.article.sectionName, "World")
        self.assertEqual(self.article.source, "The Guardian")
        self.assertEqual(self.article.author, "Guardian Author")

    def test_guardian_repr(self):
        """Test that Guardian article string representation is correct"""
        expected = "TheGuardianArticle(title='Guardian Test Article', section='World', date='2024-03-20')"
        self.assertEqual(repr(self.article), expected)

class TestNYTArticle(unittest.TestCase):
    def setUp(self):
        """Set up test data for NYTArticle class"""
        self.article = NYTArticle(
            abstract="NYT article summary",
            byline={"original": "NYT Author"},
            document_type="article",
            headline={"print_headline": "NYT Test Article", "main": "Main Headline", "kicker": "Kicker"},
            _id="nyt-123",
            keywords=[],
            multimedia={"default": {"url": "https://example.com/nyt.jpg"}},
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
            web_url="https://nyt.com/article",
            word_count=500
        )

    def test_nyt_initialization(self):
        """Test that NYT article is initialized with correct attributes"""
        self.assertEqual(self.article.title, "NYT Test Article")
        self.assertEqual(self.article.source, "New York Times")
        self.assertEqual(self.article.author, "NYT Author")
        self.assertEqual(self.article.main, "Main Headline")
        self.assertEqual(self.article.kicker, "Kicker")

class TestBBCArticle(unittest.TestCase):
    def setUp(self):
        """Set up test data for BBCArticle class"""
        self.article = BBCArticle(
            uuid="bbc-123",
            title="BBC Test Article",
            description="BBC article description",
            url="https://bbc.com/article",
            image_url="https://example.com/bbc.jpg",
            published_at="2024-03-20",
            source="BBC News",
            content="BBC article content",
            body="Full BBC article body"
        )

    def test_bbc_initialization(self):
        """Test that BBC article is initialized with correct attributes"""
        self.assertEqual(self.article.uuid, "bbc-123")
        self.assertEqual(self.article.title, "BBC Test Article")
        self.assertEqual(self.article.source, "BBC News")
        self.assertEqual(self.article.body, "Full BBC article body")

    def test_bbc_from_dict(self):
        """Test that BBC article can be created from dictionary"""
        article_dict = {
            "uuid": "bbc-123",
            "title": "BBC Test Article",
            "description": "BBC article description",
            "url": "https://bbc.com/article",
            "image_url": "https://example.com/bbc.jpg",
            "published_at": "2024-03-20",
            "source": "BBC News",
            "content": "BBC article content",
            "body": "Full BBC article body"
        }
        article = BBCArticle.from_dict(article_dict)
        self.assertEqual(article.uuid, "bbc-123")
        self.assertEqual(article.title, "BBC Test Article")

class TestGNewsArticle(unittest.TestCase):
    def setUp(self):
        """Set up test data for GNewsArticle class"""
        self.article = GNewsArticle(
            title="GNews Test Article",
            description="GNews article description",
            content="GNews article content",
            url="https://gnews.com/article",
            image="https://example.com/gnews.jpg",
            publishedAt="2024-03-20",
            source="GNews"
        )

    def test_gnews_initialization(self):
        """Test that GNews article is initialized with correct attributes"""
        self.assertEqual(self.article.title, "GNews Test Article")
        self.assertEqual(self.article.source, "GNews")
        self.assertEqual(self.article.description, "GNews article description")
        self.assertEqual(self.article.image, "https://example.com/gnews.jpg")

    def test_gnews_repr(self):
        """Test that GNews article string representation is correct"""
        expected = "GNewsArticle(title='GNews Test Article', date='2024-03-20')"
        self.assertEqual(repr(self.article), expected)

if __name__ == '__main__':
    unittest.main() 