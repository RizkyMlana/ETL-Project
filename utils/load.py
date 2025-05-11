import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Fungsi yang mengexport hasil scraping ke dalam csv
def save_to_csv(data, filename="fashion_data.csv"):
    df = pd.DataFrame(data)
    try:
        df.to_csv(filename, index=False)
        print(f"Export to csv completed {filename}")
    except Exception as e:
        print(f"Export failed to csv : {e}")
# Fungsi yang mengexport hasil scraping ke dalam postgreSQL
def save_to_postgre(data):
    df = pd.DataFrame(data)
    db_url = "postgresql://developer:supersecretpassword@localhost:5432/scrape"
    table = 'fashion_data'
    engine = create_engine(db_url)

    try:
        df.to_sql(table, engine, if_exists='replace', index=False)
        print(f"Export to postgreSQL completed")
        
    except Exception as e:
        print(f"Export failed to postgreSQL : {e}")
        
# Fungsi yang mengexport hasil scraping ke dalam google sheet
def save_to_gsheet(data):
    df = pd.DataFrame(data)
    service_account = "./scrape-fashion-data-71271af6cfb5.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credential = Credentials.from_service_account_file(service_account, scopes=SCOPES)
    spreadsheet_id = "1Qsv91kSJO4WFB9H5UFzHkyoyKxN4dnwD7oWRfE9gZmA"
    sheet_range = 'Sheet1!A1:G1000'
    service = build('sheets', 'v4', credentials=credential)
    sheet = service.spreadsheets()
    values = [df.columns.to_list()] + df.values.tolist()
    body = {
        'values':values
    }

    try:
        sheet.values().update(
            spreadsheetId = spreadsheet_id,
            range = sheet_range,
            valueInputOption='RAW',
            body = body
        ).execute()
        print(f"Export to gsheet completed")
    except Exception as e:
        print(f"Export failed to gsheet : {e}")

        



