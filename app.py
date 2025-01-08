import streamlit as st
import pandas as pd

# Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ly5WBt0c0bRy_EV8kdkP4SjsaAmkiRbzhiEYLZw2NrU/export?format=csv"  # Replace with your public Google Sheet URL

# Fetch data from Google Sheets
def fetch_google_sheets_data():
    try:
        # Read the Google Sheet as a pandas DataFrame
        sheet_data = pd.read_csv(SHEET_URL, on_bad_lines="skip")  # Skip problematic rows

        # Debugging: Show raw data for verification
        st.write("Raw Data:", sheet_data.head())

        # Validate and clean the data
        sheet_data.iloc[:, 0] = sheet_data.iloc[:, 0].str.strip()  # Strip whitespace from URLs

        # Ensure the first column contains valid URLs
        valid_rows = sheet_data[sheet_data.iloc[:, 0].str.startswith("http", na=False)]
        if valid_rows.empty:
            st.error("No valid URLs found in the data.")
            return [], {}

        urls = valid_rows.iloc[:, 0].tolist()

        # Create a dictionary of page data
        page_data = {
            row[0]: {sheet_data.columns[i]: row[i] for i in range(1, len(sheet_data.columns))}
            for row in valid_rows.itertuples(index=False)
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

# Right column: Display page data
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
        sheet_data = pd.read_csv(SHEET_URL, on_bad_lines="skip")  # Skip problematic rows

        # Debugging: Show raw data for verification
        st.write("Raw Data:", sheet_data.head())

        # Validate and clean the data
        sheet_data.iloc[:, 0] = sheet_data.iloc[:, 0].str.strip()  # Strip whitespace from URLs

        # Ensure the first column contains valid URLs
        valid_rows = sheet_data[sheet_data.iloc[:, 0].str.startswith("http", na=False)]
        if valid_rows.empty:
            st.error("No valid URLs found in the data.")
            return [], {}

        urls = valid_rows.iloc[:, 0].tolist()

        # Create a dictionary of page data
        page_data = {
            row[0]: {sheet_data.columns[i]: row[i] for i in range(1, len(sheet_data.columns))}
            for row in valid_rows.itertuples(index=False)
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

# Right column: Display page data
with col2:
    st.header("Page Data")

    if selected_url:
        data = page_data.get(selected_url, {})
        if data:
            for key, value in data.items():
                st.write(f"**{key}**: {value}")
        else:
            st.write("No data available for this URL.")
