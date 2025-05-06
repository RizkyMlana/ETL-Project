import pandas as pd
from utils.transform import clean_data
from utils.extract import scrape_multiple_pages

def main():
    print("Mulai scraping data fashion...")
    fashion_data = scrape_multiple_pages(total_pages=50)
    if fashion_data:
        df = pd.DataFrame(fashion_data)
        print("📊 Data berhasil diambil!")
        print(df)
    else:
        print("Tidak ada data yang ditemukan")

if __name__ == "__main__":
    main()