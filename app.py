import streamlit as st
import pandas as pd

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ly5WBt0c0bRy_EV8kdkP4SjsaAmkiRbzhiEYLZw2NrU/export?format=csv"  # Replace with your public Google Sheet URL

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    try:
        # Read the Google Sheet as a pandas DataFrame
        sheet_data = pd.read_csv(SHEET_URL)

        # Validate and clean the data
        sheet_data.iloc[:, 0] = sheet_data.iloc[:, 0].str.strip()  # Strip whitespace from URLs
        urls = sheet_data.iloc[:, 0].tolist()  # Assuming first column contains URLs

        # Create a dictionary of page data
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
col1, col2 = st.columns([1, 3])

# Left column: Search and List of URLs
with col1:
    st.header("Search URLs")

    # Search field
    search_query = st.text_input("Search", "")
    filtered_urls = [url for url in urls if search_query.lower() in url.lower()]

    # Dropdown for filtered URLs
    if filtered_urls:
        selected_url = st.selectbox("Select a URL", filtered_urls)
    else:
        st.write("No matching URLs found.")
        selected_url = None

# Right column: Display page data in tabs
with col2:
    st.header("Page Data")

    if selected_url:
        data = page_data.get(selected_url, {})
        if data:
            tab_names = list(data.keys())
            tabs = st.tabs(tab_names)
            for i, key in enumerate(tab_names):
                with tabs[i]:
                    st.write(f"**{key}**: {data[key]}")
        else:
            st.write("No data available for this URL.")
