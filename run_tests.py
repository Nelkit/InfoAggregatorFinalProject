import unittest
import warnings
from tests.test_scraper import TestArticleScraper
from tests.test_api_client import TestAPIClient

import logging
for name, l in logging.root.manager.loggerDict.items():
	l.disabled = True

# Carga ambos grupos de tests
scraper_suite = unittest.TestLoader().loadTestsFromTestCase(TestArticleScraper)
api_client_suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIClient)

# Combina ambas suites en una sola
combined_suite = unittest.TestSuite([scraper_suite, api_client_suite])

# Ejecuta la suite combinada
test_runner = unittest.TextTestRunner(verbosity=3)
test_runner.run(combined_suite)