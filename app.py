import os
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def get_google_sheet_data(sheet_id, range_name):
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        # Use the credentials stored in the environment variable
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
    else:
        # Use the credentials stored in a JSON file
        credentials = Credentials.from_service_account_file(
            "google-credentials.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        )

    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id).worksheet(range_name)
    data = sheet.get_all_values()

    return data

def main():
    st.title("Google Sheets Integration Example")
    
    # Define your Google Sheets ID and range here
    SPREADSHEET_ID = "your_google_sheets_id"
    RANGE_NAME = "your_range_name"
    
    companies = get_google_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    st.write(companies)

if __name__ == "__main__":
    main()
