import pytest
from scraper.strategies.base import ScrapingStrategy, ScrapingStrategyFactory
from scraper.web_scraper import WebScraper

class MockStrategy(ScrapingStrategy):
    def __init__(self):
        self.logged_in = False

    def login(self):
        self.logged_in = True

    def fetch_html(self, url):
        return "<html><body><div class='listing'>Mock Listing</div></body></html>"

    def close(self):
        pass

class MockStrategyFactory(ScrapingStrategyFactory):
    def create(self) -> ScrapingStrategy:
        return MockStrategy()

def test_web_scraper_with_mock_strategy():
    scraper = WebScraper(factory=MockStrategyFactory())
    scraper.login()
    html = scraper.get_html("http://example.com")
    data = scraper.extract_data(html)
    assert "Mock Listing" in data[0]
    scraper.close()