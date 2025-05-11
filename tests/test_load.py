import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
from utils.load import save_to_csv, save_to_gsheet, save_to_postgre

# Melakukan test untuk menyimpan ke flat csv
def test_save_to_csv():
    data = [{"Title": "T-shirt Keren", "Price": 7800808, "Rating": 4.5, "Colors": 3, "Size": "M", "Gender": "Men"}]

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        mock_to_csv.return_value = None
        save_to_csv(data, "fashion_data.csv")
        
        # Verifikasi apakah fungsi to_csv dipanggil dengan nama file yang benar
        mock_to_csv.assert_called_once_with("fashion_data.csv", index=False)

def test_save_to_postgre():
    data = [{"Title": "T-shirt Keren", "Price": 7800808, "Rating": 4.5, "Colors": 3, "Size": "M", "Gender": "Men"}]

    # Patch create_engine untuk menghindari koneksi ke database
    with patch("utils.load.create_engine") as mock_create_engine:
        # Membuat mock engine yang sesuai dengan spesifikasi Engine
        mock_engine = MagicMock(spec=Engine)
        mock_create_engine.return_value = mock_engine

        with patch("pandas.DataFrame.to_sql") as mock_to_sql:
            mock_to_sql.return_value = None
            save_to_postgre(data)

            # Verifikasi apakah to_sql dipanggil dengan mock engine
            mock_to_sql.assert_called_once_with('fashion_data', mock_engine, if_exists='replace', index=False)

# Melakukan test untuk menyimpan ke gsheet
def test_save_to_gsheet():
    data = [{"Title": "T-shirt Keren", "Price": 7800808, "Rating": 4.5, "Colors": 3, "Size": "M", "Gender": "Men"}]
    
    # Patch build untuk menghindari koneksi
    with patch("utils.load.build") as mock_build:
        mock_service = MagicMock()
        mock_spreadsheets = MagicMock()
        mock_values = MagicMock()
        mock_update = MagicMock()

        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_spreadsheets
        mock_spreadsheets.values.return_value = mock_values
        mock_values.update.return_value = mock_update
        mock_update.execute.return_value = None
        save_to_gsheet(data)

        expected_body = {
            'values': [
                ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'],
                ['T-shirt Keren', 7800808, 4.5, 3, 'M', 'Men']
            ]
        }

        mock_values.update.assert_called_once_with(
            spreadsheetId="1Qsv91kSJO4WFB9H5UFzHkyoyKxN4dnwD7oWRfE9gZmA",
            range="Sheet1!A1:G1000",
            valueInputOption="RAW",
            body=expected_body
        )