import pandas as pd

# Fungsi yang melakukan konversi dari dollar ke rupiah dengan kurs IDR 16.000
def convert_to_rupiah(price):
    if not price:
        return None
    if "$" in price:
        price = price.replace("$", "").strip()
        try:
            return round(float(price) * 16000)
        except:
            return None
    else:
        return None
# Fungsi yang melakukan cleaning data seperti menghapus data yang memiliki dirty pattern, nan, duplicate dan mengubah tipe data yang sesuai
def clean_data(data):
    df = pd.DataFrame(data)
    dirty_patterns = {
        "Title":["Unknown Product"],
        "Rating":["Invalid Rating / 5", "Not Rated"],
        "Price":["Price Unavailable", None],
    }
    for column, patterns in dirty_patterns.items():
        df = df[~df[column].isin(patterns)]
    df = df.drop_duplicates(subset=['Title', 'Price', 'Rating', 'Gender'])
    df = df.dropna(subset=['Title','Price','Rating','Gender'])

    df['Price'] = df['Price'].apply(convert_to_rupiah)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Price'] = df['Price'].astype(float)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Gender'] = df['Gender'].str.strip()
    df['Size'] = df['Size'].str.strip().str.upper()
    df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')
    df['Colors'] = df['Colors'].astype(int)
    
    df = df.reset_index(drop=True)
    return df.to_dict(orient="records")