import streamlit as st

# Sample data
urls = [
    "home/about",
    "home/services/shipping",
    "home/services/international",
    "home/services/printing"
]

page_data = {
    "home/about": {
        "Performance": "95%",
        "CWV": "Good",
        "Page Speed": "1.2s",
        "Recent Changes": "Updated meta description",
        "Description": "About us page",
        "Intent": "Informational",
    },
    "home/services/shipping": {
        "Performance": "85%",
        "CWV": "Needs Improvement",
        "Page Speed": "2.3s",
        "Recent Changes": "Added new FAQ",
        "Description": "Shipping services overview",
        "Intent": "Transactional",
    },
    "home/services/international": {
        "Performance": "78%",
        "CWV": "Poor",
        "Page Speed": "3.5s",
        "Recent Changes": "Updated rates",
        "Description": "International shipping details",
        "Intent": "Transactional",
    },
    "home/services/printing": {
        "Performance": "92%",
        "CWV": "Good",
        "Page Speed": "1.8s",
        "Recent Changes": "Added new product details",
        "Description": "Printing services overview",
        "Intent": "Transactional",
    }
}

# Split layout
col1, col2 = st.columns([1, 2])

# Left column: Search and List of URLs
with col1:
    st.header("URLs")

    # Search field
    search_query = st.text_input("Search URLs", "")
    filtered_urls = [url for url in urls if search_query.lower() in url.lower()]

    # Selectbox with filtered URLs
    selected_url = st.selectbox("Select a URL", filtered_urls if filtered_urls else ["No matching URLs"])

# Right column: Page data
with col2:
    st.header("Page Data")
    if selected_url and selected_url != "No matching URLs":
        data = page_data.get(selected_url, {})
        for key, value in data.items():
            st.write(f"**{key}**: {value}")
