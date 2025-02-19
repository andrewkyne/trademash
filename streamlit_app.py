import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Supabase credentials (replace with your own)
SUPABASE_URL = "https://ccuzilidjqzunseysfqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNjdXppbGlkanF6dW5zZXlzZnFkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk5MzM5NDgsImV4cCI6MjA1NTUwOTk0OH0.s4BSBjcIiB2n1X_vlcXDg5AmMpbkySHkWIcK9PYkrJI"

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to load CSV from GitHub
def load_csv_from_github(url: str):
    return pd.read_csv(url)

# Function to save the result to Supabase
def save_to_supabase(winner: str, loser: str):
    data = {
        "winner": winner,
        "loser": loser
    }
    supabase.table("user_data").insert(data).execute()

# Streamlit app
def main():
    # URL of the CSV file on GitHub
    csv_url = "https://raw.githubusercontent.com/andrewkyne/trademash/refs/heads/main/players.csv"
    
    st.title("Fantasy Baseball 2.0 TradeMash")

    # Load data
    df = load_csv_from_github(csv_url)

    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    # Initialize session state for random records if not already initialized
    if "selected_records" not in st.session_state or st.session_state.submitted:
        st.session_state.selected_records = df.sample(2)
        st.session_state.submitted = False  # Reset submission flag

    # Get the selected records from session state
    selected_records = st.session_state.selected_records
    record_1 = selected_records.iloc[0]
    record_2 = selected_records.iloc[1]

    # Format player display
    def format_player(record):
        return f"{record['Player']}, {record['Team']} - {record['Position']} - ${record['Salary']}"

    # Format for saving
    def format_for_saving(record):
        return f"{record['Player']} ${record['Salary']}"

    formatted_record_1 = format_player(record_1)
    formatted_record_2 = format_player(record_2)

    saved_record_1 = format_for_saving(record_1)
    saved_record_2 = format_for_saving(record_2)
    
    # Radio button for selecting the winner
    winner_choice = st.radio("Which player do you prefer?", 
                             (f"Player 1: {formatted_record_1}", 
                              f"Player 2: {formatted_record_2}"))
    
    # Handle submit action
    if st.button("Submit"):
        if not st.session_state.submitted:
            if winner_choice.startswith("Player 1"):
                save_to_supabase(saved_record_1, saved_record_2)
            else:
                save_to_supabase(saved_record_2, saved_record_1)
            
            st.session_state.submitted = True
            st.success("Vote submitted!")

    # Always show the "Next Set of Records" button
    if st.button("Next Set of Records"):
        st.session_state.selected_records = df.sample(2)
        st.session_state.submitted = False  # Reset submission flag
        st.rerun()  # Proper rerun without errors

if __name__ == "__main__":
    main()