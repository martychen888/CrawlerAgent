import json
import os

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

cfg = load_config()

# Flat config values
OPENAI_API_KEY = cfg.get("OPENAI_API_KEY", "")
USERNAME = cfg.get("USERNAME", "")
PASSWORD = cfg.get("PASSWORD", "")
LOGIN_URL = cfg.get("LOGIN_URL", "")
USERNAME_FIELD = cfg.get("USERNAME_FIELD", "username")
PASSWORD_FIELD = cfg.get("PASSWORD_FIELD", "password")
JS_WAIT_SELECTOR = cfg.get("JS_WAIT_SELECTOR", "div.dynamic-section")
RETRY_COUNT = int(cfg.get("RETRY_COUNT", 3))
MAX_PAGES = int(cfg.get("MAX_PAGES", 3))

LISTING_SELECTORS = cfg.get("LISTING_SELECTORS", [
    "div[class*='card']",
    "article",
    "li[class*='listing']"
])

# LLM block values
LLM_CONFIG = cfg.get("llm", {})
LLM_TYPE = LLM_CONFIG.get("model_type", "OpenAI")  # "OpenAI" or "Ollama"
OPENAI_MODEL = LLM_CONFIG.get("openai_model_name", "gpt-4")
OLLAMA_MODEL = LLM_CONFIG.get("ollama_model_name", "llama3")
OLLAMA_API_URL = LLM_CONFIG.get("ollama_api_url", "http://localhost:11434")