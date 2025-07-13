import os
import pickle
import requests
from fake_useragent import UserAgent
from config import USERNAME, PASSWORD, LOGIN_URL, USERNAME_FIELD, PASSWORD_FIELD
from logger import logger
from scraper.strategies import register_strategy
from scraper.strategies.base import ScrapingStrategy, ScrapingStrategyFactory

class RequestsStrategy(ScrapingStrategy):
    COOKIE_PATH = "output/cookies/requests_session.pkl"

    def __init__(self, headless=True):
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
    def __init__(self, headless=True):
        self.headless = headless

    def create(self) -> ScrapingStrategy:
        return RequestsStrategy(headless=self.headless)

register_strategy("requests", RequestsStrategyFactory)