import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API setup
SHEET_ID = "1zK6PC0vRuVvLZF0yoqhGDgUMIrt_3qT6_Qu2HcNWOwc"  # Replace with your Google Sheet ID
SERVICE_ACCOUNT_FILE = "service.json"  # Path to JSON key file

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open_by_key(SHEET_ID).sheet1

# Function to append a choice to Google Sheets
def save_to_google_sheets(choice_text):
    sheet.append_row([choice_text])

# Load data from GitHub
csv_url = "https://raw.githubusercontent.com/andrewkyne/trademash/refs/heads/main/players.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

if len(df) < 2:
    st.error("Not enough data to make a selection.")
else:
    sample = df.sample(2).reset_index(drop=True)

    def format_choice(row):
        return f"{row['Player']} - {row['Team']} - {row['Position']} - ${row['Salary']}"

    options = ["Select an option"] + list(sample.index)

    st.title("Pick Your Favorite")
    choice = st.radio(
        "Select one of the following options:",
        options=options,  
        format_func=lambda x: "Select an option" if x == "Select an option" else format_choice(sample.iloc[x]),
        index=0
    )

    if st.button("Submit Choice") and choice != "Select an option":
        user_choice = format_choice(sample.iloc[choice])
        save_to_google_sheets(user_choice)
        st.success(f"Your choice has been saved to Google Sheets: {user_choice}")