import os
from bs4 import BeautifulSoup
from scraper.strategies import get_strategy
from logger import logger
from config import LISTING_SELECTORS

class WebScraper:
    def __init__(self, engine="requests", headless=True):
        self.engine_name = engine
        self.headless = headless
        self.strategy = get_strategy(engine, headless)

    def login(self):
        self.strategy.login()

    def get_html(self, url, filename_prefix=""):
        html = self.strategy.fetch_html(url)
        if filename_prefix:
            os.makedirs("output/html", exist_ok=True)
            file_path = f"output/html/{filename_prefix}.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"Saved HTML snapshot to {file_path}")
        return html

    def extract_structure(self, html):
        soup = BeautifulSoup(html, "lxml")
        structure_lines = []
        for tag in soup.find_all(["div", "section", "article", "ul", "li"], recursive=True):
            cls = tag.get("class")
            if cls:
                line = f"<{tag.name}> class={' '.join(cls)}"
                if line not in structure_lines:
                    structure_lines.append(line)
        return "\n".join(structure_lines[:20])

    def extract_data(self, html):
        soup = BeautifulSoup(html, "lxml")
        selector_str = ", ".join(LISTING_SELECTORS)
        listing_tags = soup.select(selector_str)
        if not listing_tags:
            listing_tags = soup.find_all("div")

        extracted = []
        seen = set()
        for tag in listing_tags:
            if tag.name in ["script", "style"]:
                continue
            text = tag.get_text(separator=" | ", strip=True)
            if text and text not in seen:
                seen.add(text)
                extracted.append(text)
        return extracted

    def close(self):
        self.strategy.close()