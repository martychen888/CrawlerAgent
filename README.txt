📘 README.txt — How to Use ChatCrawler
=====================================

🌐 What Is ChatCrawler?
-----------------------
ChatCrawler is a smart, AI-driven web scraper that:
- Extracts structured data (e.g. property listings, jobs, cars) from dynamic websites  
- Uses OpenAI (GPT) to transform raw scraped HTML into clean, tabular CSV output  
- Supports `requests`, `selenium`, or `playwright` scraping engines  
- Supports login-based scraping if needed  

🚀 How to Use
=============

2. Input Fields in the UI
--------------------------

🔗 Website URL  
Paste the **full target URL** (e.g.,  
`https://www.trademe.co.nz/a/property/residential/sale/auckland`)

🧾 Prompt Template  
Below is a list of property listing descriptions.

Extract the following fields from each:
- Title (or address)
- Price (sale or rent)
- Number of Bedrooms
- Number of Bathrooms
- Location
- Listing URL (if available)

Format the result as a CSV table with the following columns:
Title,Price,Beds,Baths,Location,URL

{data}

> NOTE: The `{data}` placeholder is required — it gets replaced with the scraped HTML content.

3. Engine Options
------------------
⚙️ Scraper Engine  
Choose one:
- `requests` – Fastest, but no JavaScript support
- `selenium` – Slower but supports JS rendering
- `playwright` – Best for modern JS sites (✅ recommended for Trade Me)

✅ Headless  
Toggle on to hide browser window (true by default).

🔄 Retries  
Set the number of times to retry fetching a page in case of failure (1–5).

🔢 Listings to Analyze  
Choose how many top listings to send to the AI (start with 3–5 to avoid GPT token limits).

🤖 LLM Model Selection (OpenAI vs. Ollama)

Settings Tab

Use the Settings tab to configure which LLM backend to use:

Option 1: OpenAI (Cloud)

Requires an OpenAI API Key

Model is set to gpt-4 or gpt-3.5-turbo

Best when scraping complex content or when using AI from anywhere

Option 2: Ollama (Local Models)

Select "Ollama" from LLM Type

Set the local model name (e.g., llama3, gemma, mistral)

Requires Ollama installed locally:

ollama run llama3

Ensure ollama is running on http://localhost:11434

Works entirely offline with downloaded models

When to Use Ollama:

When you want data privacy

When you need full offline AI scraping

When running on servers or dev machines with GPUs

When to Use OpenAI:

When highest accuracy or context size is needed

When you want minimal local setup

💡 Tips

Save your config.json to reuse OpenAI keys or scraping settings.

Adjust LISTING_SELECTORS in config.json to control which HTML blocks the AI sees.

You can preview the cleaned input fed to the LLM in output/llm_input.txt.

Output is saved to output/ai_output.csv

🛠️ Advanced Features

Supports login via LOGIN_URL, USERNAME, and PASSWORD fields in config.

Supports scraping multiple pages via MAX_PAGES

Uses prompt templating ({data} placeholder)

📅 UI Walkthrough

Left section: Input, prompt, scraper settings

Right section: Logs, AI output, CSV download

Tabs: Switch between scraping and settings

🔑 Credentials (Optional)  
If login is required, fill in:
- `LOGIN_URL`
- `USERNAME`
- `PASSWORD`  
(Password will be encrypted and stored securely.)

🕐 JS_WAIT_SELECTOR  
This is a CSS selector that tells Playwright/Selenium to wait for the page to fully load JS content.  
Set this to a meaningful tag like `.listing`, `.property-card`, or `.tm-property-search-card`.

📦 Output
=========
After scraping and AI processing:
- Output will be saved to:
  `output/ai_output.csv`

❓ Troubleshooting
==================
- **Empty Output?**  
  Ensure you are using `playwright` and the correct wait selector (`JS_WAIT_SELECTOR`).

- **Too Many Tokens Error?**  
  Reduce the **Listings to Analyze** slider or prompt complexity.

- **Website Requires Login?**  
  Provide login URL, username, and password under the **Settings** tab.

🧪 Example
==========
**URL:**  
`https://www.trademe.co.nz/a/property/residential/sale/auckland`

**Prompt:**  
Extract each property's Title, Price, Location, Bedrooms, and Listing URL. Output as a CSV:

{data}

🧪 Unit Test
==========

Python -m pytest
