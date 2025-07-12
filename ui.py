import gradio as gr
from main import run_scraper_live, update_config, load_config


def create_ui(cfg, run_scraper_live_fn, update_config_fn):
    with gr.Blocks() as demo:
        gr.Markdown("## 🕷️ ChatCrawler")

        with gr.Tab("▶️ Run Crawler"):
            with gr.Row():
                url_input = gr.Text(label="Website URL", value=cfg.get("URL", "https://example.com/"))
                headless_toggle = gr.Checkbox(value=True, label="Run Headless")

            prompt_input = gr.Textbox(
                label="Prompt Template",
                lines=6,
                value=cfg.get("PROMPT", """From the following scraped HTML content, {data}"""),
            )

            with gr.Row():
                engine_choice = gr.Dropdown(
                    ["requests", "selenium", "playwright"],
                    value="playwright",
                    label="Scraper Engine"
                )
                retry_slider = gr.Slider(minimum=1, maximum=5, value=3, label="Retries")
                listing_slider = gr.Slider(minimum=1, maximum=20, value=5, step=1, label="🔢 Listings to Analyze")

            with gr.Row():
                run_button = gr.Button("🚀 Start Scraper")
                reset_btn = gr.Button("♻️ Reset", variant="secondary")
            
            with gr.Row():
                logs_box = gr.Textbox(label="📜 Logs", lines=10)
                output_box = gr.Textbox(label="📦 AI Output (CSV Preview Text)", lines=10)

            with gr.Row():  
                csv_table = gr.Dataframe(
                    headers=["Title", "Price", "Beds", "Baths", "Location", "URL"],
                    col_count=(6, "fixed"),
                    label="📄 CSV Table Preview",
                    interactive=False
                )
                download_link = gr.File(label="📁 Download CSV File")

            run_button.click(
                fn=run_scraper_live_fn,
                inputs=[url_input, prompt_input, engine_choice, headless_toggle, retry_slider, listing_slider],
                outputs=[logs_box, output_box, csv_table, download_link]
            )

            reset_btn.click(
                lambda: ("", "", [], None),
                inputs=[],
                outputs=[logs_box, output_box, csv_table, download_link]
            )

        with gr.Tab("⚙️ Settings"):
            with gr.Row():
                model_type_input = gr.Radio(
                    ["OpenAI", "Ollama", "DeepSeek"],
                    value=cfg.get("llm", {}).get("model_type", "OpenAI"),
                    label="LLM Provider"
                )

            with gr.Row(visible=True) as openai_row:
                api_key_input = gr.Text(label="OpenAI API Key", value=cfg.get("llm", {}).get("openai_api_key", ""), type="password")
                model_input = gr.Dropdown(
                    choices=["gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
                    value=cfg.get("llm", {}).get("openai_model_name", "gpt-4"),
                    label="OpenAI Model"
                )

            with gr.Row(visible=False) as ollama_row:
                ollama_model_input = gr.Dropdown(
                    choices=cfg.get("llm", {}).get("ollama_model_choices", ["llama3"]),
                    value=cfg.get("llm", {}).get("ollama_model_name", "llama3"),
                    label="Ollama Model"
                )
                ollama_url_input = gr.Text(label="Ollama API URL", value=cfg.get("llm", {}).get("ollama_api_url", "http://localhost:11434"))

            with gr.Row(visible=False) as deepseek_row:
                deepseek_model_input = gr.Text(label="DeepSeek Model", value=cfg.get("llm", {}).get("deepseek_model_name", "deepseek-chat"))
                deepseek_api_input = gr.Text(label="DeepSeek API Key", value=cfg.get("llm", {}).get("deepseek_api_key", ""), type="password")

            with gr.Row():
                login_url_input = gr.Text(label="Login URL", value=cfg.get("LOGIN_URL", ""))
                user_input = gr.Text(label="Username", value=cfg.get("USERNAME", ""))
                pw_input = gr.Text(label="Password", value=cfg.get("PASSWORD", ""), type="password")

            save_btn = gr.Button("📂 Save Config")
            status_msg = gr.Textbox(label="Status", interactive=False)

            def toggle_model_visibility(selected):
                return (
                    gr.update(visible=(selected == "OpenAI")),
                    gr.update(visible=(selected == "Ollama")),
                    gr.update(visible=(selected == "DeepSeek"))
                )

            model_type_input.change(
                fn=toggle_model_visibility,
                inputs=model_type_input,
                outputs=[openai_row, ollama_row, deepseek_row]
            )

            save_btn.click(
                fn=update_config_fn,
                inputs=[
                    api_key_input,
                    model_input,
                    ollama_model_input,
                    ollama_url_input,
                    login_url_input,
                    user_input,
                    pw_input,
                    model_type_input,
                    deepseek_model_input,
                    deepseek_api_input
                ],
                outputs=status_msg
            )

    return demo


cfg = load_config()
demo = create_ui(cfg, run_scraper_live, update_config)