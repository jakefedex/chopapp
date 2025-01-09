import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ly5WBt0c0bRy_EV8kdkP4SjsaAmkiRbzhiEYLZw2NrU/export?format=csv"  # Replace with your public Google Sheet URL

# Fetch Google Sheets data
@st.cache_data
def fetch_google_sheets_data():
    try:
        sheet_data = pd.read_csv(SHEET_URL)
        sheet_data.iloc[:, 0] = sheet_data.iloc[:, 0].str.strip()
        urls = sheet_data.iloc[:, 0].tolist()
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

# Sidebar
with st.sidebar:
    st.header("Search and Filter")
    reviewed_filter = st.selectbox("Filter by Reviewed Status", ["All", "Yes", "No"])
    search_query = st.text_input("Search", "")
    author_sort = st.selectbox("Sort by Author", ["None"] + sorted(sheet_data['Author'].dropna().unique().tolist()))

    if author_sort != "None":
        filtered_urls = [url for url in urls if sheet_data[sheet_data.iloc[:, 0] == url].iloc[0, 1] == author_sort and (reviewed_filter == "All" or st.session_state["reviewed_status"].get(url, "No") == reviewed_filter)]
    else:
        filtered_urls = [url for url in urls if search_query.lower() in url.lower() and (reviewed_filter == "All" or st.session_state["reviewed_status"].get(url, "No") == reviewed_filter)]
    truncated_urls = [url.replace("https://www.fedex.com", "") for url in filtered_urls]
    selected_truncated_url = st.selectbox("Select a URL", truncated_urls) if filtered_urls else None
    selected_url = filtered_urls[truncated_urls.index(selected_truncated_url)] if selected_truncated_url else None

# Main Content
if selected_url:
    st.header("Page Data")
    st.subheader(f"Selected URL: {selected_url}")
    data = page_data.get(selected_url, {})
    if data:
        tab_names = ["Overview", "Analytics", "Actions", "Technical", "AI Suggestions", "Preview"]
        tabs = st.tabs(tab_names)

        # Overview Tab
        with tabs[0]:
            st.subheader("Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Content Details")
                row_data = sheet_data[sheet_data.iloc[:, 0] == selected_url].iloc[0, 1:6]
                st.write(f"**Page Description:** {row_data[0]}")
                st.write(f"**Author:** {row_data[1]}")
                st.write(f"**Meta Title:** {row_data[3]}")
                st.write(f"**Meta Description:** {row_data[4]}")
            with col2:
                st.write("### SEO Summary")
                st.write(f"**Is In Sitemap:** Yes")
                st.write(f"**Unique Referring Domains:** {sheet_data[sheet_data.iloc[:, 0] == selected_url].iloc[0, 6]}")
                st.write(f"**Number of Incoming Internal Links:** {sheet_data[sheet_data.iloc[:, 0] == selected_url].iloc[0, 7]}")
                st.write(f"**HTTP Status:** {st.selectbox('Select HTTP Status', ['200', '301', '404', 'Other'], key=f'http_status_{selected_url}')}")

        # Analytics Tab
        with tabs[1]:
            st.subheader("Analytics")   

            # Timeframe Selector
            timeframe = st.selectbox("Select Time Range", ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last 12 Months"])

            # Filter traffic data based on timeframe
            traffic_data = pd.DataFrame(
                {
                    "Date": pd.date_range(start="2023-01-01", periods=365, freq="D"),
                    "Visitors": np.random.randint(50, 500, size=365),
                    "Conversions": np.random.randint(1, 50, size=365),
                }
)

            if timeframe == "Last 30 Days":
                filtered_data = traffic_data.tail(30)
            elif timeframe == "Last 3 Months":
                filtered_data = traffic_data.tail(90)
            elif timeframe == "Last 6 Months":
                filtered_data = traffic_data.tail(180)
            elif timeframe == "Last 12 Months":
                filtered_data = traffic_data.tail(365)

            col1, col2, col3 = st.columns(3)
            with col1:
                from streamlit_extras.metric_cards import style_metric_cards
                st.write("### Traffic Summary")

                st.metric("Total Visitors", f"{total_visitors}")
                st.metric("Total Conversions", f"{total_conversions}")
                st.metric("Conversion Rate", f"{conversion_rate}")

                # Apply styling to metric cards
                style_metric_cards()
            with col2:
                st.write("### Traffic Trends")
                st.line_chart(filtered_data.set_index("Date"))
            with col3:
                st.write("### Search Queries")
                search_query_data = pd.DataFrame(
                    {
                        "Query": [f"demo query {i}" for i in range(1, 21)],
                        "CTR": np.random.uniform(1.0, 10.0, 20).round(2),
                        "Impressions": np.random.randint(100, 10000, 20),
                        "Clicks": np.random.randint(10, 500, 20),
                    }
).sort_values(by="Clicks", ascending=False)
                # Define pagination parameters
                page_size = 5
                num_pages = len(search_query_data) // page_size + (len(search_query_data) % page_size > 0)

                # Create a page selector
                current_page = st.number_input("Page", min_value=1, max_value=num_pages, step=1, value=1)

                # Slice the dataframe to only show the current page
                start_idx = (current_page - 1) * page_size
                end_idx = start_idx + page_size
                paginated_data = search_query_data.iloc[start_idx:end_idx]

                st.dataframe(paginated_data, use_container_width=True)

        # Actions Tab
        with tabs[2]:
            st.subheader("Actions")
            col1, col2 = st.columns(2)
            with col1:
                decision = st.selectbox(
                    "What action should be taken for this URL?",
                    ["No Change", "Remove from Sitemap", "Delete"],
                    key=f"decision_{selected_url}"
)
                st.session_state["url_decisions"][selected_url] = decision
                st.write(f"Current Decision: {st.session_state['url_decisions'].get(selected_url, 'No Decision')}")
            with col2:
                reviewed = st.selectbox(
                    "Has this URL been reviewed?",
                    ["Yes", "No"],
                    index=1,  # Default to "No"
                    key=f"reviewed_{selected_url}"
)
                st.session_state["reviewed_status"][selected_url] = reviewed
                reviewed_status = st.session_state['reviewed_status'].get(selected_url, 'No')
                if reviewed_status == 'Yes':
                    st.markdown(f"Reviewed: <span style='color: green;'>Yes</span>", unsafe_allow_html=True)
                else:
                    st.write(f"Reviewed: {reviewed_status}")

        # Technical Tab
        with tabs[3]:
            st.subheader("Technical Details")
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Core Web Vitals")
                st.markdown("**Largest Contentful Paint (LCP):** 2.3s <span style='background-color: orange; color: white; padding: 2px 5px;'>Okay</span>", unsafe_allow_html=True)
                st.markdown("**Cumulative Layout Shift (CLS):** 0.05 <span style='background-color: green; color: white; padding: 2px 5px;'>Good</span>", unsafe_allow_html=True)
                st.markdown("**First Input Delay (FID):** 18ms <span style='background-color: red; color: white; padding: 2px 5px;'>Poor</span>", unsafe_allow_html=True)
            with col2:
                st.write("### Link and Indexing Details")
                st.write("**Canonical URL:** Present")
                st.write("**Indexability:** Indexable")
                st.write("**Broken Links:** None")

        # AI Suggestions Tab
        with tabs[4]:
            st.subheader("AI Suggestions")
            st.write("### Content Optimization Suggestions")
            st.write("- Improve the Meta Description to include the primary keyword.")
            st.write("- Add more internal links to related pages.")
            st.write("- Optimize images for faster load times.")
            st.write("### SEO Opportunities")
            st.write("- Target secondary keywords such as 'FedEx delivery times' and 'FedEx locations near me.'")
            st.write("- Acquire backlinks from industry-relevant domains.")

        # Preview Tab
        with tabs[5]:
            st.subheader("Embedded Page View")
            st.markdown(
                f'<iframe src="{selected_url}" width="100%" height="600" frameborder="0"></iframe>',
                unsafe_allow_html=True
)
    else:
        st.write("No data available for this URL.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: left; font-size: small;'>Built by: Jake L.</div>", unsafe_allow_html=True)
