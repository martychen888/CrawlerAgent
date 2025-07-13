import os
from playwright.sync_api import sync_playwright
from config import USERNAME, PASSWORD, LOGIN_URL, USERNAME_FIELD, PASSWORD_FIELD, JS_WAIT_SELECTOR
from logger import logger
from scraper.strategies import register_strategy
from scraper.strategies.base import ScrapingStrategy, ScrapingStrategyFactory

class PlaywrightStrategy(ScrapingStrategy):
    STORAGE_STATE = "output/cookies/playwright_state.json"

    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = None
        self.page = None
        if os.path.exists(self.STORAGE_STATE):
            self.context = self.browser.new_context(storage_state=self.STORAGE_STATE)
            self.page = self.context.new_page()
            logger.info("Playwright session loaded from storage state.")
        else:
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

    def login(self):
        if not LOGIN_URL or LOGIN_URL.startswith("${"):
            logger.info('No valid LOGIN_URL provided, skipping login.')
            return
        if os.path.exists(self.STORAGE_STATE):
            logger.info("Playwright login skipped, storage state exists.")
            return
        self.page.goto(LOGIN_URL)
        self.page.fill(f'input[name="{USERNAME_FIELD}"]', USERNAME)
        self.page.fill(f'input[name="{PASSWORD_FIELD}"]', PASSWORD)
        self.page.click('button[type="submit"], input[type="submit"]')
        self.page.wait_for_timeout(2000)
        self.context.storage_state(path=self.STORAGE_STATE)
        logger.info("Playwright login + session stored.")

    def fetch_html(self, url):
        self.page.goto(url)
        try:
            self.page.wait_for_selector(JS_WAIT_SELECTOR, timeout=5000)
        except Exception:
            logger.warning(f"Timeout waiting for JS content: {JS_WAIT_SELECTOR}")
        return self.page.content()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

class PlaywrightStrategyFactory(ScrapingStrategyFactory):
    def __init__(self, headless=True):
        self.headless = headless

    def create(self) -> ScrapingStrategy:
        return PlaywrightStrategy(headless=self.headless)
    
register_strategy("playwright", PlaywrightStrategyFactory)