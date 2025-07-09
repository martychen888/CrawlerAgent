
import json
import os

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

cfg = load_config()

OPENAI_API_KEY = cfg.get("OPENAI_API_KEY", "")
OPENAI_MODEL = cfg.get("OPENAI_MODEL", "gpt-4")
USERNAME = cfg.get("USERNAME", "")
PASSWORD = cfg.get("PASSWORD", "")
LOGIN_URL = cfg.get("LOGIN_URL", "")
USERNAME_FIELD = cfg.get("USERNAME_FIELD", "username")
PASSWORD_FIELD = cfg.get("PASSWORD_FIELD", "password")
JS_WAIT_SELECTOR = cfg.get("JS_WAIT_SELECTOR", "div.dynamic-section")
RETRY_COUNT = int(cfg.get("RETRY_COUNT", 3))
