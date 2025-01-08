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
    truncated_urls = [url.replace("https://www.fedex.com", "") for url in filtered_urls]
    selected_truncated_url = st.selectbox("Select a URL", truncated_urls) if filtered_urls else None
    selected_url = filtered_urls[truncated_urls.index(selected_truncated_url)] if selected_truncated_url else None

# Detailed view for the selected URL
if selected_url:
    st.header("Page Data")
    st.subheader(f"Selected URL: {selected_url}")  # Display the selected URL above the tabs
    data = page_data.get(selected_url, {})
    if data:
        tab_names = ["Description", "Analytics", "Actions", "SEO", "Embed"]
        tabs = st.tabs(tab_names)
        for i, key in enumerate(tab_names):
            with tabs[i]:
                if key == "Description":
                    st.subheader("Page Description")
                    if sheet_data is not None:
                        row_data = sheet_data[sheet_data.iloc[:, 0] == selected_url].iloc[0, 1:6]
                        st.write(f"**Page Description:** {row_data[0]}")
                        st.write(f"**Author:** {row_data[1]}")
                        st.write(f"**Page URL:** {row_data[2]}")
                        st.write(f"**Meta Title:** {row_data[3]}")
                        st.write(f"**Meta Description:** {row_data[4]}")

                elif key == "Analytics":
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

                    # Add a spacer
                    st.markdown("---")

                    # Line chart for traffic data
                    st.line_chart(filtered_data.set_index("Date"))

                    # Example search query data
                    search_query_data = pd.DataFrame(
                        {
                            "Query": [f"demo query {i}" for i in range(1, 21)],
                            "CTR": np.random.uniform(1.0, 10.0, 20).round(2),
                            "Impressions": np.random.randint(100, 10000, 20),
                            "Clicks": np.random.randint(10, 500, 20),
                        }
                    ).sort_values(by="Clicks", ascending=False)

                    st.subheader("Search Query Data")
                    st.dataframe(search_query_data, use_container_width=True)

                    st.subheader("Search Query Data")
                    st.dataframe(search_query_data)
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

                elif key == "SEO":
                    st.subheader("SEO Information")
                    if sheet_data is not None:
                        row_data_backlinks = sheet_data[sheet_data.iloc[:, 0] == selected_url].iloc[0, 6]
                        row_data_internal_links = sheet_data[sheet_data.iloc[:, 0] == selected_url].iloc[0, 7]
                        st.write(f"**Backlinks:** {row_data_backlinks}")
                        st.write(f"**Number of Internal Links:** {row_data_internal_links}")

                elif key == "Embed":
                    st.subheader("Embedded Page View")
                    st.markdown(
                        f'<iframe src="{selected_url}" width="100%" height="600" frameborder="0"></iframe>',
                        unsafe_allow_html=True
                    )
                else:
                    st.write("No data available for this URL.")
