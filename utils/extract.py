import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Mengatur user agent untuk menghindari pemblokiran dari server
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# fungsi yang mengambil data yg berisikan tag dan class tertentu
def extract_fashion_data(card):
    details = card.find('div', class_='product-details')
    prg = details.find_all('p')
    if not details:
        return None
    title_el = details.find('h3', class_='product-title')
    price_el = details.find('span', class_='price')
    rating_raw = prg[0].get_text(strip=True).replace('Rating:', '').strip()
    rating_match = re.search(r"(\d+(\.\d+)?)", rating_raw)
    colors_raw = prg[1].get_text(strip=True)
    color_match = re.search(r"\d+", colors_raw)

    
    title = title_el.get_text(strip=True) if title_el else None
    price = price_el.get_text(strip=True) if price_el else None
    rating = float(rating_match.group(1)) if rating_match else None
    colors = int(color_match.group()) if color_match else None
    size = prg[2].get_text(strip=True).replace('Size:', '').strip()
    gender = prg[3].get_text(strip=True).replace('Gender:', '').strip()

    return {
        "Title" : title,
        "Price" : price,
        "Rating" : rating,
        "Colors" : colors,
        "Size" : size,
        "Gender" : gender,
    }
# Fungsi yang nge fetch content dari page
def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"error saat ngambil {url}: {e}")
        return None

# Fungsi yang melakukan pengambilan data 
def scrape_fashion_data(url):
    content = fetch_page_content(url)
    if not content:
        return []
    soup = BeautifulSoup(content, 'html.parser')
    data = []
    cards = soup.find_all('div', class_="collection-card")
    extract = datetime.now().isoformat()
    for card in cards:
        fashion_data = extract_fashion_data(card)
        if fashion_data:
            fashion_data['Timestamp'] = extract
            data.append(fashion_data)
    return data

# Fungsi yang mengambil data yang melakukan perulangan sebanyak 50 page
def scrape_multiple_pages(total_pages=50):
    base_url = "https://fashion-studio.dicoding.dev"
    all_data = []

    for page in range(1, total_pages + 1):
        if page == 1:
            full_url = base_url
        else:
            full_url = f"{base_url}/page{page}"
        
        print(f"Scraping halaman {page} => {full_url}")
        page_data = scrape_fashion_data(full_url)
        
        if page_data:
            all_data.extend(page_data)
        else:
            print(f"Tidak ada data di halaman {page}")
    
    return [d for d in all_data if d is not None]


