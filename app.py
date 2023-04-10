import os
import openai
import streamlit as st
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

# Set up API credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "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"
RANGE_NAME = "Sheet1!A:A"

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]



def get_google_sheet_data(spreadsheet_id, range_name):
    creds = None
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        creds = Credentials.from_authorized_user_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    return result.get("values", [])


def check_fortune_1000(company_name):
    prompt = f"Is {company_name} in the Fortune 1000 list?"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return answer.lower() == "yes"


def main():
    st.title("Fortune 1000 Company Lookup")
    companies = get_google_sheet_data(SPREADSHEET_ID, RANGE_NAME)

    st.write("### List of Companies:")
    for company in companies:
        company_name = company[0]
        is_fortune_1000 = check_fortune_1000(company_name)
        status = "Yes" if is_fortune_1000 else "No"
        st.write(f"{company_name}: {status}")


if __name__ == "__main__":
    main()

