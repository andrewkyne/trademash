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
    csv_url = "https://raw.githubusercontent.com/andrewkyne/trademash/refs/heads/main/players.csv?token=GHSAT0AAAAAAC7F6QRFJO4QXIFMVCRMTVCMZ5VKTRQ"
     
    # Load data
    df = load_csv_from_github(csv_url)

    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    # Initialize session state for random records if not already initialized
    if "selected_records" not in st.session_state:
        # Select two random records and store them in session state
        st.session_state.selected_records = df.sample(2)
        st.session_state.submitted = False  # Flag to track if submission has been made

    # Get the selected records from session state
    selected_records = st.session_state.selected_records
    record_1 = selected_records.iloc[0]
    record_2 = selected_records.iloc[1]
    
    # Display the two records to the user
    st.write(f"Record 1: {record_1.to_dict()}")
    st.write(f"Record 2: {record_2.to_dict()}")
    
    # Radio button for selecting the winner
    winner_choice = st.radio("Which record do you prefer?", 
                             (f"Record 1: {record_1.to_dict()}", 
                              f"Record 2: {record_2.to_dict()}"))
    
    # Handle submit action
    if st.button("Submit"):
        # Ensure the submission happens only once
        if not st.session_state.submitted:
            if winner_choice.startswith("Record 1"):
                save_to_supabase(record_1['Player'], record_2['Player'])
            else:  # If user selects record 2
                save_to_supabase(record_2['Player'], record_1['Player'])
            
            # Set the submission flag to True
            st.session_state.submitted = True
            st.success("Selection saved successfully!")
        
        # Optionally, create a button to load the next set of random records
        if st.session_state.submitted:
            next_set_button = st.button("Next Set of Records")
            if next_set_button:
                # Reset selected records to get a new random set
                st.session_state.selected_records = df.sample(2)
                st.session_state.submitted = False  # Reset submitted flag for the new round

if __name__ == "__main__":
    main()
