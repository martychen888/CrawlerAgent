import json
import os

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

cfg = load_config()

# Global values
OPENAI_API_KEY = cfg.get("OPENAI_API_KEY", "")
USERNAME = cfg.get("USERNAME", "")
PASSWORD = cfg.get("PASSWORD", "")
LOGIN_URL = cfg.get("LOGIN_URL", "")
USERNAME_FIELD = cfg.get("USERNAME_FIELD", "username")
PASSWORD_FIELD = cfg.get("PASSWORD_FIELD", "password")
JS_WAIT_SELECTOR = cfg.get("JS_WAIT_SELECTOR", "div.dynamic-section")
RETRY_COUNT = int(cfg.get("RETRY_COUNT", 3))
MAX_PAGES = int(cfg.get("MAX_PAGES", 3))

# Listing selectors used for scraping repeated items
LISTING_SELECTORS = cfg.get("LISTING_SELECTORS", [
    "div[class*='card']",
    "article",
    "li[class*='listing']",
    ".tm-property-search-card"
])

# LLM Config
llm_cfg = cfg.get("llm", {})
LLM_TYPE = llm_cfg.get("model_type", "OpenAI")
MODEL_TYPE = llm_cfg.get("model_type", "OpenAI")
OPENAI_MODEL = llm_cfg.get("openai_model_name", "gpt-4")
OLLAMA_MODEL = llm_cfg.get("ollama_model_name", "llama3")
OLLAMA_API_URL = llm_cfg.get("ollama_api_url", "http://localhost:11434")