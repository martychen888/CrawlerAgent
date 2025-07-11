from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from config import (
    LLM_TYPE,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OLLAMA_MODEL,
    OLLAMA_API_URL
)

def get_llm():
    if LLM_TYPE.lower() == "openai":
        return ChatOpenAI(
            temperature=0,
            model=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
    elif LLM_TYPE.lower() == "ollama":
        return ChatOllama(
            temperature=0,
            model=OLLAMA_MODEL,
            base_url=OLLAMA_API_URL
        )
    else:
        raise ValueError(f"Unsupported LLM type: {LLM_TYPE}")

def generate_response(prompt: str) -> str:
    llm = get_llm()
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()