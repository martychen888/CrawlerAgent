def test_mock_strategy_injection(mock_scraper):
    html = mock_scraper.get_html("http://example.com")
    assert "Mock Data" in html

    structure = mock_scraper.extract_structure(html)
    assert "<div> class=mock" in structure

    data = mock_scraper.extract_data(html)
    assert "Mock Data" in data