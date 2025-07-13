import os
import time
import pickle
from config import USERNAME, PASSWORD, LOGIN_URL, USERNAME_FIELD, PASSWORD_FIELD, JS_WAIT_SELECTOR
from logger import logger
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright

from scraper.strategy_base import ScrapingStrategy, ScrapingStrategyFactory

class RequestsStrategy(ScrapingStrategy):
    COOKIE_PATH = "output/cookies/requests_session.pkl"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": UserAgent().random})
        self.load_session()

    def load_session(self):
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH, "rb") as f:
                self.session.cookies.update(pickle.load(f))
            logger.info("Requests session cookies loaded.")

    def save_session(self):
        os.makedirs("output/cookies", exist_ok=True)
        with open(self.COOKIE_PATH, "wb") as f:
            pickle.dump(self.session.cookies, f)

    def login(self):
        if not LOGIN_URL or LOGIN_URL.startswith("${"):
            logger.info('No valid LOGIN_URL provided, skipping login.')
            return
        data = {USERNAME_FIELD: USERNAME, PASSWORD_FIELD: PASSWORD}
        r = self.session.post(LOGIN_URL, data=data, allow_redirects=True)
        if r.status_code == 200:
            logger.info("Requests login success.")
            self.save_session()
        else:
            raise Exception(f"Requests login failed with status {r.status_code}.")

    def fetch_html(self, url):
        r = self.session.get(url)
        r.raise_for_status()
        return r.text

    def close(self):
        pass

class RequestsStrategyFactory(ScrapingStrategyFactory):
    def create(self) -> ScrapingStrategy:
        return RequestsStrategy()

class SeleniumStrategy(ScrapingStrategy):
    COOKIE_PATH = "output/cookies/selenium_cookies.pkl"

    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_argument(f"user-agent={UserAgent().random}")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)

    def save_cookies(self):
        os.makedirs("output/cookies", exist_ok=True)
        with open(self.COOKIE_PATH, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)

    def load_cookies(self):
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH, "rb") as f:
                cookies = pickle.load(f)
            self.driver.get("about:blank")
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            logger.info("Selenium cookies loaded.")

    def login(self):
        if not LOGIN_URL or LOGIN_URL.startswith("${"):
            logger.info('No valid LOGIN_URL provided, skipping login.')
            return
        self.driver.get(LOGIN_URL)
        self._auto_fill_field(USERNAME_FIELD, USERNAME)
        self._auto_fill_field(PASSWORD_FIELD, PASSWORD)
        self._click_login_button()
        time.sleep(2)
        self.save_cookies()

    def _auto_fill_field(self, name, value):
        try:
            el = self.driver.find_element(By.NAME, name)
            el.clear()
            el.send_keys(value)
        except Exception as e:
            logger.warning(f"Field {name} not found or error: {e}")

    def _click_login_button(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'],input[type='submit']")
            btn.click()
        except Exception as e:
            logger.warning(f"Login button not found or click failed: {e}")

    def fetch_html(self, url):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, JS_WAIT_SELECTOR))
            )
        except Exception:
            logger.warning(f"Timeout waiting for JS content: {JS_WAIT_SELECTOR}")
        return self.driver.page_source

    def close(self):
        self.driver.quit()

class SeleniumStrategyFactory(ScrapingStrategyFactory):
    def __init__(self, headless=True):
        self.headless = headless

    def create(self) -> ScrapingStrategy:
        return SeleniumStrategy(headless=self.headless)

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


def get_factory(engine, headless=True) -> ScrapingStrategyFactory:
    if engine == "requests":
        return RequestsStrategyFactory()
    elif engine == "selenium":
        return SeleniumStrategyFactory(headless=headless)
    elif engine == "playwright":
        return PlaywrightStrategyFactory(headless=headless)
    else:
        raise ValueError(f"Unknown scraping engine: {engine}")