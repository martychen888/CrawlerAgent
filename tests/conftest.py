import pytest
from unittest.mock import MagicMock
from scraper.web_scraper import WebScraper
from scraper.strategies.base import ScrapingStrategy

class MockStrategy(ScrapingStrategy):
    def login(self):
        pass

    def fetch_html(self, url):
        return "<html><body><div class='mock'>Mock Data</div></body></html>"

    def close(self):
        pass

@pytest.fixture
def mock_scraper():
    scraper = WebScraper(engine="requests")
    scraper.strategy = MockStrategy()  # Inject mock
    return scraper