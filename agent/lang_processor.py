from langchain.prompts import PromptTemplate
from agent.llm import generate_response
import os

MAX_INPUT_CHARS = 8000

def langchain_process(scraped_data, prompt_text):
    # scraped_data now already contains clean plain-text blocks
    os.makedirs("output", exist_ok=True)
    with open("output/llm_input.txt", "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(scraped_data))

    content = "\n".join(scraped_data)
    if len(content) > MAX_INPUT_CHARS:
        content = content[:MAX_INPUT_CHARS]

    enhanced_prompt = (
        prompt_text.strip()
        + "\n\nFormat the result as a CSV table with the following headers:\n"
        + "Title,Price,Beds,Baths,Location,URL\n"
        + "Only output valid rows, no markdown or explanation.\n"
    )

    prompt = PromptTemplate.from_template(enhanced_prompt).format(data=content)

    print("🧠 Prompt preview sent to LLM:\n", prompt[:1000])

    return generate_response(prompt)