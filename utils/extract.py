import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_fashion_data(card):
    details = card.find('div', class_='product-details')
    if not details:
        return None
    title_el = details.find('h3', class_='product-title')
    price_el = details.find('span', class_='price')
    prg = details.find_all('p')
    
    title = title_el.get_text(strip=True) if title_el else None
    price = price_el.get_text(strip=True) if price_el else None
    rating = prg[0].get_text(strip=True).replace('Rating:', '').strip()
    colors = prg[1].get_text(strip=True)
    size = prg[2].get_text(strip=True).replace('Size:', '').strip()
    gender = prg[3].get_text(strip=True).replace('Gender:', '').strip()

    return {
        "title" : title,
        "price" : price,
        "rating" : rating,
        "colors" : colors,
        "size" : size,
        "gender" : gender
    }
def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"error saat ngambil {url}: {e}")
        return None
    
def scrape_fashion_data(url):
    content = fetch_page_content(url)
    if not content:
        return []
    soup = BeautifulSoup(content, 'html.parser')
    data = []
    cards = soup.find_all('div', class_="collection-card")
    for card in cards:
        fashion_data = extract_fashion_data(card)
        data.append(fashion_data)
    return data



