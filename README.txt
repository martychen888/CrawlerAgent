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

🛠️ Advanced Configuration (in config.json)
==========================================

{
  "OPENAI_API_KEY": "your-key-here",
  "OPENAI_MODEL": "gpt-4",
  "LOGIN_URL": "https://example.com/login",
  "USERNAME": "your-username",
  "PASSWORD": "your-password",
  "JS_WAIT_SELECTOR": ".tm-property-search-card",
  "MAX_LISTINGS": 5
}

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
