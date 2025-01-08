import streamlit as st
import pandas as pd
import numpy as np

# Inject custom CSS
custom_css = """
<style>
/* Style the sidebar */
.sidebar .block-container {
    background-color: #f7f9fc;
    padding: 20px;
    border-right: 2px solid #ddd;
}

/* Style the headers */
h1 {
    color: #2b6777;
    font-size: 32px;
    font-weight: bold;
}

h2 {
    color: #2b6777;
    font-size: 28px;
    margin-bottom: 10px;
}

h3 {
    color: #2b6777;
    font-size: 24px;
    margin-bottom: 8px;
}

/* Style the tabs */
.css-1y4p8pa.e8zbici0 {
    background-color: #e0f4f1;
    border-radius: 5px;
    padding: 5px;
    margin-bottom: 10px;
}

/* Style for text under Analytics */
.analytics-text {
    color: #555;
    font-size: 16px;
    margin: 5px 0;
}

/* Style the charts */
.css-1f9s62r {
    background-color: #fff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
"""

# Inject the CSS
st.markdown(custom_css, unsafe_allow_html=True)


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

# Sidebar: Search and Filter functionality
with st.sidebar:
    st.header("Search and Filter")

    # Filter by reviewed status
    reviewed_filter = st.selectbox("Filter by Reviewed Status", ["All", "Yes", "No"])

    # Search field
    search_query = st.text_input("Search", "")

    # Filter URLs based on search and reviewed status
    filtered_urls = [
        url for url in urls
        if search_query.lower() in url.lower() and
        (reviewed_filter == "All" or st.session_state["reviewed_status"].get(url, "No") == reviewed_filter)
    ]

    # Dropdown for filtered URLs
    selected_url = st.selectbox("Select a URL", filtered_urls) if filtered_urls else None

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

                    # Display aggregated metrics
                    total_visitors = filtered_data["Visitors"].sum()
                    total_conversions = filtered_data["Conversions"].sum()
                    conversion_rate = f"{(total_conversions / total_visitors * 100):.2f}%" if total_visitors > 0 else "0.00%"

                    st.write(f"**Total Visitors:** {total_visitors}")
                    st.write(f"**Total Conversions:** {total_conversions}")
                    st.write(f"**Conversion Rate:** {conversion_rate}")

                    # Line chart for traffic data
                    st.line_chart(filtered_data.set_index("Date"))

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
