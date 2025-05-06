import pandas as pd
from utils.extract import scrape_fashion_data
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