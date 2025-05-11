import pandas as pd
from utils.transform import clean_data
from utils.extract import scrape_multiple_pages
from utils.load import save_to_csv, save_to_postgre, save_to_gsheet

# Fungsi yang berisikan kumpulan fungsi yang ada di extract, transform, load
def main():
    print("Mulai scraping data fashion...")
    fashion_data = scrape_multiple_pages(total_pages=50)
    if not fashion_data:
        print('Tidak ada data')
        return
    cleaned_data = clean_data(fashion_data)
    df = pd.DataFrame(cleaned_data)
    save_to_csv(df)
    save_to_postgre(df)
    save_to_gsheet(df)
if __name__ == "__main__":
    main()