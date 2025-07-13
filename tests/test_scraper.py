from scraper.web_scraper import WebScraper

def test_extract_structure_basic_html():
    scraper = WebScraper(engine="requests")  
    html = "<html><body><div class='card'>Item</div></body></html>"
    structure = scraper.extract_structure(html)
    assert "<div> class=card" in structure
    scraper.close()

def test_extract_data_fallback():
    scraper = WebScraper(engine="requests") 
    html = "<html><body><div>Test Listing</div></body></html>"
    data = scraper.extract_data(html)
    assert "Test Listing" in data
    scraper.close()