import requests
from langchain.schema import HumanMessage
from config import (
    LLM_TYPE,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OLLAMA_MODEL,
    OLLAMA_API_URL,
    cfg
)

class LLMHandler:
    def __init__(self):
        self.llm_type = LLM_TYPE.lower()

    def _call_deepseek_api(self, prompt, model_name, api_key):
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def _get_langchain_llm(self):
        if self.llm_type == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                temperature=0,
                model=OPENAI_MODEL,
                openai_api_key=OPENAI_API_KEY
            )
        elif self.llm_type == "ollama":
            from langchain_community.chat_models import ChatOllama
            return ChatOllama(
                temperature=0,
                model=OLLAMA_MODEL,
                base_url=OLLAMA_API_URL
            )
        else:
            raise ValueError(f"Unsupported LangChain-based LLM type: {self.llm_type}")

    def generate_response(self, prompt: str) -> str:
        if self.llm_type == "deepseek":
            model = cfg.get("llm", {}).get("deepseek_model_name", "deepseek-chat")
            key = cfg.get("llm", {}).get("deepseek_api_key", "")
            return self._call_deepseek_api(prompt, model, key)
        else:
            llm = self._get_langchain_llm()
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
