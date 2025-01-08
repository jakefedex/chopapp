import streamlit as st
import pandas as pd

# Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ly5WBt0c0bRy_EV8kdkP4SjsaAmkiRbzhiEYLZw2NrU/edit?usp=sharing"  # Replace with your public Google Sheet URL

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    try:
        # Read the Google Sheet as a pandas DataFrame
        sheet_data = pd.read_csv(SHEET_URL, on_bad_lines="skip")  # Skips problematic rows
        
        # Validate the first column contains URLs
        if sheet_data.empty or len(sheet_data.columns) < 1:
            st.error("The sheet does not contain enough data or is misformatted.")
            return [], {}
        
        # Ensure all rows in the first column are valid URLs
        sheet_data = sheet_data[sheet_data.iloc[:, 0].str.startswith("http", na=False)]
        
        urls = sheet_data.iloc[:, 0].tolist()  # Assuming first column contains URLs
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

    # Selectbox with filtered URLs
    if filtered_urls:
        selected_url = st.selectbox("Select a URL", filtered_urls)
    else:
        st.write("No matching URLs")
        selected_url = None

# Right column: Page data
with col2:
    st.header("Page Data")
    if selected_url:
        data = page_data.get(selected_url, {})
        if data:
            for key, value in data.items():
                st.write(f"**{key}**: {value}")
        else:
            st.write("No data available for this URL.")
import streamlit as st
import pandas as pd

# Google Sheets URL
SHEET_URL = "your_public_google_sheet_url"  # Replace with your public Google Sheet URL

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    try:
        # Read the Google Sheet as a pandas DataFrame
        sheet_data = pd.read_csv(SHEET_URL, on_bad_lines="skip")  # Skips problematic rows
        
        # Validate the first column contains URLs
        if sheet_data.empty or len(sheet_data.columns) < 1:
            st.error("The sheet does not contain enough data or is misformatted.")
            return [], {}
        
        # Ensure all rows in the first column are valid URLs
        sheet_data = sheet_data[sheet_data.iloc[:, 0].str.startswith("http", na=False)]
        
        urls = sheet_data.iloc[:, 0].tolist()  # Assuming first column contains URLs
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

    # Selectbox with filtered URLs
    if filtered_urls:
        selected_url = st.selectbox("Select a URL", filtered_urls)
    else:
        st.write("No matching URLs")
        selected_url = None

# Right column: Page data
with col2:
    st.header("Page Data")
    if selected_url:
        data = page_data.get(selected_url, {})
        if data:
            for key, value in data.items():
                st.write(f"**{key}**: {value}")
        else:
            st.write("No data available for this URL.")
