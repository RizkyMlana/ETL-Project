import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_fashion_data(section):
    title = section.find('h3').text
    price = section.find('span').text
    rating = section.find('p').text
    colors = section.find('p').text
    size = section.find('p').text
    gender = section.find('p').text

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
    card = soup.find('div', id="", class_="collection-card")
    if card:
        sections = [desc for desc in card.descendants if desc.name== 'section']
        for section in sections:
            fashion_data = extract_fashion_data(section)
            data.append(fashion_data)
    return data

def main():
    url = "https://fashion-studio.dicoding.dev/"
    fashion_data = scrape_fashion_data(url)
    if fashion_data:
        df = pd.DataFrame(fashion_data)
        print(df)
    else:
        print("Tidak ada data yang ditemukan")

if __name__ == "__main__":
    main()