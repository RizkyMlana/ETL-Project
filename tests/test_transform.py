import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import clean_data, convert_to_rupiah

def test_convert_to_rupiah():
    assert convert_to_rupiah("$199.99") == 3199840  # USD ke IDR
    assert convert_to_rupiah("$0") == 0  # Tes 0 USD
    assert convert_to_rupiah("$abc") is None  # Tes input yang tidak valid
    assert convert_to_rupiah(None) is None  # Tes None

# Tes untuk fungsi clean_data
def test_clean_data():
    data = [
        {"Title": "T-shirt Keren", "Price": "$199.99", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Men" },
        {"Title": "Unknown Product", "Price": "$299.99", "Rating": "Invalid Rating / 5",  "Colors": "2", "Size": "L", "Gender": "Unisex"},
        {"Title": "Jeans Kasual", "Price": "$150.00", "Rating": "Not Rated", "Colors": "5", "Size": "S", "Gender": "Women"},
        {"Title": "T-shirt Keren", "Price": "$199.99", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Men"},  # Duplikat     
        {"Title": "T-shirt Cool", "Price": "Price Unavailable", "Rating": "4.0", "Colors": "4", "Size": "L", "Gender": "Men"},        
        {"Title": "Shirt Cool", "Price": None, "Rating": "4.2", "Colors": "2", "Size": "M", "Gender": "Unisex"},
    ]

    cleaned_data = clean_data(data)

    # Memastikan hanya 1 produk valid setelah pembersihan
    assert len(cleaned_data) == 1  # Seharusnya 1 produk valid

    # Memastikan kolom Price sudah dalam format Rupiah (IDR)
    assert cleaned_data[0]["Price"] == 3199840  # USD ke IDR conversion
    
    # Memastikan data dengan rating "Invalid Rating / 5" dihapus
    assert "Invalid Rating / 5" not in [item["Rating"] for item in cleaned_data]
    
    # Memastikan data dengan "Unknown Product" dihapus
    assert "Unknown Product" not in [item["Title"] for item in cleaned_data]
    
    # Memastikan data dengan harga "Price Unavailable" dihapus
    assert "Price Unavailable" not in [item["Price"] for item in cleaned_data]
    
    # Memastikan semua nilai Rating dan Colors adalah numerik
    assert all(isinstance(item["Rating"], float) for item in cleaned_data)
    assert all(isinstance(item["Colors"], int) for item in cleaned_data)
    
    # Memastikan kolom Size sudah dalam format uppercase
    assert all(item["Size"].isupper() for item in cleaned_data)
    
    # Memastikan kolom Gender sudah bersih dari spasi tambahan
    assert all(item["Gender"] == item["Gender"].strip() for item in cleaned_data)

# Tes untuk data kosong
def test_empty_data():
    cleaned_data = clean_data([])
    assert cleaned_data == []  # Data kosong harus tetap kosong

# Tes untuk data tidak valid
def test_invalid_data():
    cleaned_data = clean_data([{"Title": "Invalid", "Price": None, "Rating": None, "Size": "M", "Gender": "Men", "Colors": None}])
    assert len(cleaned_data) == 0  # Semua data invalid harus dihapus