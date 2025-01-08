
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

if "reviewed_status" not in st.session_state:
    st.session_state["reviewed_status"] = {}

# Split layout
col1, col2 = st.columns([1, 3])

# Left column: Search and List of URLs
with col1:
    st.header("Search URLs")

    # Filter by reviewed status
    reviewed_filter = st.selectbox("Filter by Reviewed Status", ["All", "Yes", "No"])

    # Search field
    search_query = st.text_input("Search", "")
    filtered_urls = [
        url for url in urls 
        if search_query.lower() in url.lower() and 
        (reviewed_filter == "All" or st.session_state["reviewed_status"].get(url, "No") == reviewed_filter)
    ]

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
            tab_names = list(data.keys()) + ["Analytics", "Actions"]
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
                    elif key == "Actions":
                        # Actions Tab for URL Decisions and Reviewed Status
                        st.subheader("Mark URL Decision")
                        decision = st.radio(
                            "What action should be taken for this URL?",
                            ["No Change", "Remove from Sitemap", "Delete"],
                            key=f"decision_{selected_url}"
                        )
                        st.session_state["url_decisions"][selected_url] = decision
                        st.write(f"Current Decision: {st.session_state['url_decisions'].get(selected_url, 'No Decision')}")

                        st.subheader("Reviewed Status")
                        reviewed = st.radio(
                            "Has this URL been reviewed?",
                            ["Yes", "No"],
                            index=1,  # Default to "No"
                            key=f"reviewed_{selected_url}"
                        )
                        st.session_state["reviewed_status"][selected_url] = reviewed
                        st.write(f"Reviewed: {st.session_state['reviewed_status'].get(selected_url, 'No')}")
                    else:
                        st.write(f"**{key}**: {data[key]}")
        else:
            st.write("No data available for this URL.")

# Export user selections
def export_user_selections():
    decisions_data = [
        {"URL": url, "Decision": decision, "Reviewed": st.session_state["reviewed_status"].get(url, "No")}
        for url, decision in st.session_state["url_decisions"].items()
    ]
    return pd.DataFrame(decisions_data)

if st.button("Export Selections"):
    # Prepare the data for export
    export_df = export_user_selections()
    
    if not export_df.empty:
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="user_selections.csv",
            mime="text/csv",
        )
    else:
        st.warning("No selections have been made yet!")
