from agent.lang_processor import langchain_process

class MockLLM:
    def generate_response(self, prompt):
        return f"Mocked response for: {prompt}"

def test_langchain_process(monkeypatch):
    monkeypatch.setattr("agent.lang_processor.LLMHandler", lambda: MockLLM())
    scraped = ["Listing 1", "Listing 2"]
    prompt = "Summarize: {data}"
    result = langchain_process(scraped, prompt)
    assert "Mocked response" in result