import gradio as gr
from gradio.themes.base import Base
from gradio.themes.soft import Soft
from gradio.themes.monochrome import Monochrome
import os

def create_ui(cfg, run_scraper_fn, update_config_fn):
    llm_cfg = cfg.get("llm", {})

    with gr.Blocks() as demo:
        gr.Markdown("## 🕷️ ChatCrawler")

        gr.HTML("""
                <style>
                    body, .gradio-container {
                        background-color: #898989 !important;
                        color: #f0f0f0 !important;
                    }
                </style>
                """)

        with gr.Tab("Run Crawler"):
            with gr.Row():
                url_input = gr.Text(label="Website URL", value=cfg.get("URL", "https://example.com/"))

            with gr.Row():
                prompt_input = gr.Textbox(
                    label="Prompt Template",
                    lines=6,
                    value=cfg.get("PROMPT", "Extract key property details:\n\n{data}")
                )

            # Row 1: Engine + Headless
            with gr.Row():
                with gr.Column(scale=3):
                    engine_choice = gr.Dropdown(["requests", "selenium", "playwright"], value="playwright", label="Scraper Engine")
                with gr.Column(scale=1):
                    headless_toggle = gr.Checkbox(value=True, label="Run Headless")

            # Row 2: Retries + Listings
            with gr.Row():
                retry_slider = gr.Slider(minimum=1, maximum=5, value=3, label="Retries")
                listing_slider = gr.Slider(minimum=1, maximum=20, value=5, step=1, label="🔢 Listings to Analyze")

            # Row 3: Buttons side by side
            with gr.Row(equal_height=True):
                run_button = gr.Button("🚀 Start Scraper", scale=1)
                reset_button = gr.Button("🔁 Reset", scale=1)

            # Row 4: Logs and AI preview
            with gr.Row():
                logs_box = gr.Textbox(label="📜 Logs", lines=10)
                output_box = gr.Textbox(label="📦 AI Output (Preview)", lines=10)

            # Row 5: CSV + Stats
            with gr.Row():
                download_button = gr.File(label="📅 Download CSV", visible=True)
                stats_box = gr.Textbox(label="📊 Stats", interactive=False)

            # Function to wrap scraper output
            def wrapper_run_scraper(*args):
                for logs, output, path in run_scraper_fn(*args):
                    stats = f"{output.count(chr(10))} CSV lines generated (including header)." if output else "No output generated."
                    download = path if path and os.path.exists(path) else None
                    yield logs, output, download, stats

            # Hook run button
            run_button.click(
                fn=wrapper_run_scraper,
                inputs=[url_input, prompt_input, engine_choice, headless_toggle, retry_slider, listing_slider],
                outputs=[logs_box, output_box, download_button, stats_box]
            )

            # Reset button clears everything
            reset_button.click(
                fn=lambda: ("", "", None, ""),
                inputs=[],
                outputs=[logs_box, output_box, download_button, stats_box]
            )

        with gr.Tab("⚙️ Settings"):
            api_key_input = gr.Text(label="OpenAI API Key", value=cfg.get("OPENAI_API_KEY", ""), type="password")

            llm_type_input = gr.Dropdown(["OpenAI", "Ollama"], value=llm_cfg.get("model_type", "OpenAI"), label="LLM Type")
            openai_model_input = gr.Text(label="OpenAI Model", value=llm_cfg.get("openai_model_name", "gpt-4"))
            ollama_model_input = gr.Text(label="Ollama Model", value=llm_cfg.get("ollama_model_name", "llama3"))
            ollama_url_input = gr.Text(label="Ollama API URL", value=llm_cfg.get("ollama_api_url", "http://localhost:11434"))

            login_url_input = gr.Text(label="Login URL", value=cfg.get("LOGIN_URL", ""))
            user_input = gr.Text(label="Username", value=cfg.get("USERNAME", ""))
            pw_input = gr.Text(label="Password", value=cfg.get("PASSWORD", ""), type="password")

            save_btn = gr.Button("📏 Save Config")
            status_msg = gr.Textbox(label="Status", interactive=False)

            save_btn.click(
                fn=update_config_fn,
                inputs=[
                    api_key_input,
                    llm_type_input,
                    openai_model_input,
                    ollama_model_input,
                    ollama_url_input,
                    login_url_input,
                    user_input,
                    pw_input
                ],
                outputs=status_msg
            )

    return demo
