from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from config import OPENAI_API_KEY, OPENAI_MODEL

def langchain_process(scraped_data, prompt_text):
    # Join the scraped listing data passed from the caller (already sliced by max_listings)
    content = "\n".join(scraped_data)

    # Build the enhanced prompt for GPT
    enhanced_prompt = (
        prompt_text.strip()
        + "\n\nFormat the result as a CSV table. Only output the CSV rows and headers.\n"
        + "If data is insufficient, output a valid CSV header row anyway.\n"
        + "Avoid explanations or markdown.\n"
    )

    # Replace {data} in prompt template with actual listing content
    prompt = PromptTemplate.from_template(enhanced_prompt).format(data=content)

    # Call OpenAI's chat model
    llm = ChatOpenAI(
        temperature=0,
        model=OPENAI_MODEL,
        openai_api_key=OPENAI_API_KEY
    )
    response = llm.invoke([HumanMessage(content=prompt)])

    # Return clean result
    return response.content.strip()