import os
import json
from cryptography.fernet import Fernet
import gradio as gr

from scraper.web_scraper import WebScraper
from agent.lang_processor import langchain_process
from logger import logger

CONFIG_PATH = "config.json"
KEY_FILE = "secret.key"

# ===============================
# 🔐 Encryption Utilities
# ===============================
def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

fernet = Fernet(load_key())

def encrypt_password(pw): return fernet.encrypt(pw.encode()).decode()
def decrypt_password(enc_pw): return fernet.decrypt(enc_pw.encode()).decode() if enc_pw else ""

# ===============================
# ⚙️ Config I/O
# ===============================
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if cfg.get("PASSWORD"):
                cfg["PASSWORD"] = decrypt_password(cfg["PASSWORD"])
            return cfg
    return {}

def save_config(cfg):
    cfg = cfg.copy()
    if cfg.get("PASSWORD"):
        cfg["PASSWORD"] = encrypt_password(cfg["PASSWORD"])
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

# ===============================
# 🧠 Scraper Runner
# ===============================
def run_scraper_live(url, prompt, engine, headless, retries, max_listings):
    from agent.lang_processor import langchain_process
    from scraper.web_scraper import WebScraper
    from logger import logger
    import os
    import csv

    if not url or not url.startswith("http"):
        yield "❌ Invalid URL. Please enter a valid website starting with http/https.", "", [], None
        return

    log = []
    try:
        log.append(f"🌐 Scraping with {engine}...")
        scraper = WebScraper(engine=engine, headless=headless)
        scraper.login()
        html = scraper.get_html(url)
        structure = scraper.extract_structure(html)
        data = scraper.extract_data(html)
        scraper.close()

        log.append(f"✅ Scraping done. Found {len(data)} listings before trimming.")
        if data:
            log.append(f"🧪 Sample card preview: {data[0][:300]}...")

        trimmed_data = data[:max_listings]
        log.append(f"✂️ Trimmed to {len(trimmed_data)} listings for LLM.")
        log.append("🧠 Analyzing listings with LLM...")

        ai_output = langchain_process(trimmed_data, prompt)
        output_path = "output/ai_output.csv"
        os.makedirs("output", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ai_output)

        log.append(f"📁 Output saved to {output_path}")

        # Parse CSV to preview
        rows = []
        for line in ai_output.strip().splitlines():
            if "," in line:
                rows.append(line.split(","))

        headers = rows[0] if rows else []
        csv_data = rows[1:] if len(rows) > 1 else []

        yield "\n".join(log), ai_output, csv_data, output_path

    except Exception as e:
        logger.exception("Scraper error")
        yield f"❌ Error: {str(e)}", "", [], None

# ===============================
# ⚙️ Config Save Hook
# ===============================
def update_config(api_key, openai_model, ollama_model, ollama_url, login_url, user, pw, model_type, deepseek_model, deepseek_api_key):
    cfg = {
        "OPENAI_API_KEY": api_key.strip(),
        "llm": {
            "model_type": model_type.strip(),
            "openai_model_name": openai_model.strip(),
            "ollama_model_name": ollama_model.strip(),
            "ollama_api_url": ollama_url.strip()
        },
        "LOGIN_URL": login_url.strip(),
        "USERNAME": user.strip(),
        "PASSWORD": pw.strip()
    }
    save_config(cfg)
    return "✅ Config saved!"
