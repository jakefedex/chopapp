import streamlit as st
import pandas as pd

# Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ly5WBt0c0bRy_EV8kdkP4SjsaAmkiRbzhiEYLZw2NrU/edit?usp=sharing"  # Replace with your public Google Sheet URL

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    try:
        # Read the Google Sheet as a pandas DataFrame
        sheet_data = pd.read_csv(SHEET_URL, on_bad_lines="skip")  # Skips problematic rows
        st.write("Raw Data:", sheet_data)  # Debugging: Show raw data

        # Validate and clean URLs
        sheet_data.iloc[:, 0] = sheet_data.iloc[:, 0].str.strip()  # Strip whitespace
        st.write("URLs Column After Stripping:", sheet_data.iloc[:, 0])  # Debugging

        # Extract URLs and Page Data
        urls = sheet_data.iloc[:, 0].tolist()
        page_data = {
            row[0]: {sheet_data.columns[i]: row[i] for i in range(1, len(sheet_data.columns))}
            for row in sheet_data.itertuples(index=False)
        }
        return urls, page_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return [], {}

# Fetch data
urls, page_data = fetch_google_sheets_data()

# Split layout
col1, col2 = st.columns([1, 2])

# Left column: Search and List of URLs
with col1:
    st.header("URLs")

    # Search field
    search_query = st.text_input("Search URLs", "")
    filtered_urls = [url for url in urls if search_query.lower() in url.lower()]
    st.write("Filtered URLs:", filtered_urls)
