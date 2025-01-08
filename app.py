import streamlit as st
import pandas as pd
import numpy as np

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

# State to track user decisions
if "url_decisions" not in st.session_state:
    st.session_state["url_decisions"] = {}

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
            tab_names = list(data.keys()) + ["Analytics"]
            tabs = st.tabs(tab_names)
            for i, key in enumerate(tab_names):
                with tabs[i]:
                    if key == "Analytics":
                        # Analytics Tab with Sorting Functionality
                        st.subheader("Traffic Analytics")

                        # Example traffic data
                        traffic_data = pd.DataFrame(
                            {
                                "Date": pd.date_range(start="2023-01-01", periods=365, freq="D"),
                                "Visitors": np.random.randint(50, 500, size=365),
                                "Conversions": np.random.randint(1, 50, size=365),
                            }
                        )

                        # Sorting options
                        sort_option = st.selectbox("Select Time Range", ["Last 30 Days", "Last 6 Months", "Last 12 Months"])

                        if sort_option == "Last 30 Days":
                            filtered_data = traffic_data.tail(30)
                        elif sort_option == "Last 6 Months":
                            filtered_data = traffic_data.tail(182)
                        elif sort_option == "Last 12 Months":
                            filtered_data = traffic_data.tail(365)

                        # Line chart for traffic data
                        st.line_chart(filtered_data.set_index("Date"))

                        # Display aggregated metrics
                        st.subheader("Key Metrics")
                        st.write(
                            {
                                "Total Visitors": filtered_data["Visitors"].sum(),
                                "Total Conversions": filtered_data["Conversions"].sum(),
                                "Conversion Rate": f"{(filtered_data['Conversions'].sum() / filtered_data['Visitors'].sum() * 100):.2f}%",
                            }
                        )
                    else:
                        st.write(f"**{key}**: {data[key]}")

            # Decision options for the selected URL
            st.subheader("Mark URL Decision")
            decision = st.radio(
                "What action should be taken for this URL?",
                ["No Change", "Remove from Sitemap", "Delete"],
                key=selected_url
            )
            st.session_state["url_decisions"][selected_url] = decision
            st.write(f"Current Decision: {st.session_state['url_decisions'].get(selected_url, 'No Decision')}"))
        else:
            st.write("No data available for this URL.")
