import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from utils.extract import (extract_fashion_data, 
                           fetch_page_content, 
                           scrape_fashion_data, 
                           scrape_multiple_pages)


tag_html = '''
<div class="collection-card">
  <div class="product-details">
    <h3 class="product-title">T-shirt Keren</h3>
    <span class="price">$199.99</span>
    <p>Rating: 4.5⭐</p>
    <p>3 Colors</p>
    <p>Size: L</p>
    <p>Gender: Men</p>
  </div>
</div>
'''

url = "https://fashion-studio.dicoding.dev"


def test_extract_fashion_data():
    soup = BeautifulSoup(tag_html, 'html.parser')
    card = soup.find('div', class_='collection-card')
    result = extract_fashion_data(card)

    assert result["Title"] == "T-shirt Keren"
    assert result["Price"] == "$199.99"
    assert result["Rating"] == 4.5
    assert result["Colors"] == 3
    assert result["Size"] == "L"
    assert result["Gender"] == "Men"

def test_fetch_page_content_success():
    with patch('utils.extract.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html></html>'
        mock_get.return_value = mock_response

        content = fetch_page_content(url)
        assert content == b'<html></html>'

def test_fetch_page_content_failure():
    with patch('utils.extract.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        content = fetch_page_content(url)
        assert content is None

def test_scrape_fashion_data():
    with patch('utils.extract.fetch_page_content', return_value=tag_html.encode()):
        data = scrape_fashion_data(url)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['Title'] == "T-shirt Keren"
        assert 'Timestamp' in data[0]

def test_scrape_multiple_pages():
    with patch('utils.extract.scrape_fashion_data', return_value=[{"Title": "Product", "Price": "16000", "Rating": 5, "Colors": 1, "Size": "M", "Gender": "Unisex", "Timestamp": "2024-01-01T00:00:00"}]):
        result = scrape_multiple_pages(total_pages=3)
        assert isinstance(result, list)
        assert len(result) == 3