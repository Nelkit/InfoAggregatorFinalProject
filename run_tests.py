import os
# Disable Streamlit browser warning
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

import unittest
import warnings
from tests.test_scraper import TestArticleScraper
from tests.test_api_client import TestAPIClient
from tests.test_news_article import TestNewsArticle, TestTheGuardianArticle, TestNYTArticle, TestBBCArticle, TestGNewsArticle

import logging
# Disable all loggers to reduce noise during test execution
for name, l in logging.root.manager.loggerDict.items():
	l.disabled = True

# Filter out Streamlit-specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")
warnings.filterwarnings("ignore", category=FutureWarning, module="streamlit")

# Load test suites for each component
scraper_suite = unittest.TestLoader().loadTestsFromTestCase(TestArticleScraper)
api_client_suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIClient)
news_article_suite = unittest.TestLoader().loadTestsFromTestCase(TestNewsArticle)
the_guardian_article_suite = unittest.TestLoader().loadTestsFromTestCase(TestTheGuardianArticle)
nyt_article_suite = unittest.TestLoader().loadTestsFromTestCase(TestNYTArticle)
bbc_article_suite = unittest.TestLoader().loadTestsFromTestCase(TestBBCArticle)
gnews_article_suite = unittest.TestLoader().loadTestsFromTestCase(TestGNewsArticle)

# Combine all test suites into a single suite
combined_suite = unittest.TestSuite([
	scraper_suite,
	api_client_suite,
	news_article_suite,
	the_guardian_article_suite,
	nyt_article_suite,
	bbc_article_suite,
	gnews_article_suite
])

# Run the combined test suite with detailed output
test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(combined_suite)