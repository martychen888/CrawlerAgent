from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from config import MODEL_TYPE, OPENAI_API_KEY, OPENAI_MODEL, OLLAMA_MODEL, OLLAMA_API_URL

def langchain_process(scraped_data, prompt_text):
    from langchain_core.messages import HumanMessage

    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        ChatOpenAI = None

    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError:
        ChatOllama = None

    content = "\n".join(scraped_data)
    prompt = PromptTemplate.from_template(prompt_text.strip()).format(data=content)

    if MODEL_TYPE == "Ollama":
        if ChatOllama is None:
            raise ImportError("LangChain Ollama not available. Install with `pip install langchain-community`.")
        llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_API_URL)
    else:
        if ChatOpenAI is None:
            raise ImportError("LangChain OpenAI not available. Install with `pip install langchain-openai`.")
        llm = ChatOpenAI(model=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY, temperature=0)

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()