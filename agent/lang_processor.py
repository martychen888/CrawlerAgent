from langchain.prompts import PromptTemplate
from agent.llm import LLMHandler

def langchain_process(scraped_data, prompt_text):
    content = "\n".join(scraped_data)
    prompt = PromptTemplate.from_template(prompt_text.strip()).format(data=content)
    return LLMHandler().generate_response(prompt)