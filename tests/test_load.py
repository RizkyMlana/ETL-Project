import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
import pandas as pd
from utils.load import save_to_csv, save_to_gsheet, save_to_postgre

def test_save_to_csv():
    data = [{"Title": "T-shirt Keren", "Price": "7800808", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Men"}]

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        mock_to_csv.return_value = None  # Simulasikan bahwa tidak ada error saat menulis file
        save_to_csv(data, "test_fashion_data.csv")
        
        # Verifikasi apakah fungsi to_csv dipanggil dengan nama file yang benar
        mock_to_csv.assert_called_once_with("test_fashion_data.csv", index=False)

def test_save_to_postgre():
    data = [{"Title": "T-shirt Keren", "Price": "7800808", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Men"}]

    # Patch create_engine untuk menghindari koneksi ke database
    with patch("sqlalchemy.create_engine") as mock_create_engine:
        # Buat mock engine yang sesuai dengan spesifikasi Engine
        mock_engine = MagicMock(spec=Engine)
        mock_create_engine.return_value = mock_engine

        with patch("pandas.DataFrame.to_sql") as mock_to_sql:
            mock_to_sql.return_value = None  # Simulasikan bahwa tidak ada error saat menulis ke database
            save_to_postgre(data)

            # Verifikasi apakah to_sql dipanggil dengan mock engine
            mock_to_sql.assert_called_once_with('fashion_data', mock_engine, if_exists='replace', index=False)

def test_save_to_gsheet():
    # Data yang ingin diuji
    data = [{"Title": "T-shirt Keren", "Price": "7800808", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Men"}]

    # Patch build dari googleapiclient.discovery untuk menghindari panggilan API sebenarnya
    with patch("googleapiclient.discovery.build") as mock_build:
        mock_service = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_service.spreadsheets.return_value = mock_spreadsheet
        mock_build.return_value = mock_service

        mock_spreadsheet.values.return_value.update.return_value.execute.return_value = None
        # Patch pandas DataFrame untuk memastikan values yang tepat
        with patch.object(pd.DataFrame, 'values', return_value=[["T-shirt Keren", "7800808", "4.5", "3", "M", "Men"]]):
            save_to_gsheet(data)

            # Verifikasi apakah values().update dipanggil dengan argumen yang benar
            expected_body = {
                'values': [
                    ['Title', 'Price', 'Rating', 'Colors','Size', 'Gender'],
                    ['T-shirt Keren', '7800808', '4.5', '3', 'M', 'Men']
                ]
            }
            
            # Pastikan tidak ada MagicMock dalam body
            mock_spreadsheet.values().update.assert_called_once_with(
                spreadsheetId="1Qsv91kSJO4WFB9H5UFzHkyoyKxN4dnwD7oWRfE9gZmA",
                range="Sheet1!A1:G1000",
                valueInputOption="RAW",
                body=expected_body
            )