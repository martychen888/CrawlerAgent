
import gradio as gr
import json
import os
import validators
from cryptography.fernet import Fernet

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
    engine = engine or auto_select_engine(url)
    if not url or not url.startswith("http"):
        yield "❌ Invalid URL. Please enter a valid website starting with http/https.", ""
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

        log.append(f"✅ Scraping done. Found {len(data)} listings.")
        trimmed_data = data[:max_listings]

        log.append(f"🧠 Analyzing top {len(trimmed_data)} listings with LLM...")

        ai_output = langchain_process(trimmed_data, prompt)

        output_path = "output/ai_output.csv"
        os.makedirs("output", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ai_output)

        log.append(f"📁 Output saved to {output_path}")
        yield "\n".join(log), ai_output
    except Exception as e:
        logger.exception("Scraper error")
        yield f"❌ Error: {str(e)}", ""

# ===============================
# ⚙️ Save Config Action
# ===============================
def update_config(api_key, model, login_url, user, pw):
    cfg = {
        "OPENAI_API_KEY": api_key.strip(),
        "OPENAI_MODEL": model.strip(),
        "LOGIN_URL": login_url.strip(),
        "USERNAME": user.strip(),
        "PASSWORD": pw.strip()
    }
    save_config(cfg)
    return "✅ Config saved!"

# ===============================
# 🧪 UI Setup
# ===============================
cfg = load_config()

with gr.Blocks() as demo:
    gr.Markdown("## 🕷️ ChatCrawler")

    with gr.Tab("Run Crawler"):
        with gr.Row():
            url_input = gr.Text(label="Website URL", value=cfg.get("URL", "https://example.com/"))
            prompt_input = gr.Textbox(label="Prompt Template", lines=6, value=cfg.get("PROMPT", "Extract key property details from:\n\n{data}"))
        with gr.Row():
            engine_choice = gr.Dropdown(["requests", "selenium", "playwright"], value="playwright", label="Scraper Engine")
            headless_toggle = gr.Checkbox(value=True, label="Run Headless")
            retry_slider = gr.Slider(minimum=1, maximum=5, value=3, label="Retries")
            listing_slider = gr.Slider(minimum=1, maximum=20, value=5, step=1, label="🔢 Listings to Analyze")
        run_button = gr.Button("🚀 Start")
        logs_box = gr.Textbox(label="📜 Logs", lines=10)
        output_box = gr.Textbox(label="📦 AI Output", lines=10)
        run_button.click(
            fn=run_scraper_live,
            inputs=[url_input, prompt_input, engine_choice, headless_toggle, retry_slider, listing_slider],
            outputs=[logs_box, output_box]
        )

    with gr.Tab("⚙️ Settings"):
        api_key_input = gr.Text(label="OpenAI API Key", value=cfg.get("OPENAI_API_KEY", ""), type="password")
        model_input = gr.Text(label="OpenAI Model", value=cfg.get("OPENAI_MODEL", "gpt-4"))
        login_url_input = gr.Text(label="Login URL", value=cfg.get("LOGIN_URL", ""))
        user_input = gr.Text(label="Username", value=cfg.get("USERNAME", ""))
        pw_input = gr.Text(label="Password", value=cfg.get("PASSWORD", ""), type="password")
        save_btn = gr.Button("💾 Save Config")
        status_msg = gr.Textbox(label="Status", interactive=False)
        save_btn.click(fn=update_config, inputs=[api_key_input, model_input, login_url_input, user_input, pw_input], outputs=status_msg)

demo.queue().launch()
