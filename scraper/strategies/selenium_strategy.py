import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from config import USERNAME, PASSWORD, LOGIN_URL, USERNAME_FIELD, PASSWORD_FIELD, JS_WAIT_SELECTOR
from logger import logger
from scraper.strategies import register_strategy
from scraper.strategies.base import ScrapingStrategy, ScrapingStrategyFactory

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

register_strategy("selenium", SeleniumStrategyFactory)