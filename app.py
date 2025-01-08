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
        return urls, page_data, sheet_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return [], {}, None

# Fetch data
urls, page_data, sheet_data = fetch_google_sheets_data()

# State to track user decisions
if "url_decisions" not in st.session_state:
    st.session_state["url_decisions"] = {}

if "reviewed_status" not in st.session_state:
    st.session_state["reviewed_status"] = {}

# Front page: Display all URLs and their data in a table
st.header("All URLs and Data")
if sheet_data is not None:
    # Add a column with clickable links to each URL
    sheet_data["URL"] = sheet_data["URL"].apply(lambda x: f"[View Details](#{x})")
    st.write(sheet_data.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Get the URL clicked by the user
    clicked_url = st.experimental_get_query_params().get("url", [None])[0]

    # If a URL is clicked, show its details
    if clicked_url in urls:
        selected_url = clicked_url
    else:
        selected_url = None
else:
    st.write("No data available.")

# Detailed view for the selected URL
if selected_url:
    st.header("Page Data")
    st.subheader(f"Selected URL: {selected_url}")  # Display the selected URL above the tabs
    data = page_data.get(selected_url, {})
    if data:
        tab_names = list(data.keys()) + ["Analytics", "Actions"]
        tabs = st.tabs(tab_names)
        for i, key in enumerate(tab_names):
            with tabs[i]:
                if key == "Analytics":
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
        return urls, page_data, sheet_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return [], {}, None

# Fetch data
urls, page_data, sheet_data = fetch_google_sheets_data()

# State to track user decisions
if "url_decisions" not in st.session_state:
    st.session_state["url_decisions"] = {}

if "reviewed_status" not in st.session_state:
    st.session_state["reviewed_status"] = {}

# Front page: Display all URLs and their data in a table
st.header("All URLs and Data")
if sheet_data is not None:
    # Add a column with clickable links to each URL
    sheet_data["URL"] = sheet_data["URL"].apply(lambda x: f"[View Details](#{x})")
    st.write(sheet_data.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Get the URL clicked by the user
    clicked_url = st.experimental_get_query_params().get("url", [None])[0]

    # If a URL is clicked, show its details
    if clicked_url in urls:
        selected_url = clicked_url
    else:
        selected_url = None
else:
    st.write("No data available.")

# Detailed view for the selected URL
if selected_url:
    st.header("Page Data")
    st.subheader(f"Selected URL: {selected_url}")  # Display the selected URL above the tabs
    data = page_data.get(selected_url, {})
    if data:
        tab_names = list(data.keys()) + ["Analytics", "Actions"]
        tabs = st.tabs(tab_names)
        for i, key in enumerate(tab_names):
            with tabs[i]:
                if key == "Analytics":
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
