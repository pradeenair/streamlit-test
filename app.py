import openai
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import streamlit as st

# Google Sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Enter your Google Sheet ID and range
SPREADSHEET_ID = "1y1M1nzulCTWOSPiZAGh_zVeAHwZ6Z8bgwfY0AvIO4Dk"
RANGE_NAME = "Sheet1!A1:A"  # Adjust according to the column containing the company names

# ChatGPT API setup
openai.api_key = "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"


def get_google_sheet_data(spreadsheet_id, range_name):
    creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

    service = build("sheets", "v4", credentials=creds)
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get("values", [])


def is_company_in_fortune_1000(company):
    prompt = f"Is {company} in the Fortune 1000 list?"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip().lower()
    return answer == "yes"


def main():
    st.title("Fortune 1000 Company Lookup")

    companies = get_google_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    result_list = []

    for company in companies:
        company_name = company[0]
        in_fortune_1000 = is_company_in_fortune_1000(company_name)
        result_list.append((company_name, in_fortune_1000))

    st.write("Results:")

    for result in result_list:
        st.write(f"{result[0]}: {'Yes' if result[1] else 'No'}")


if __name__ == "__main__":
    main()
