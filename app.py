# Tabs setup
tab_names = ["Overview", "Analytics", "Technical", "AI Suggestions", "Preview", "Actions"]
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
    # Traffic Data
    traffic_data = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=365, freq="D"),
        "Visitors": np.random.randint(50, 500, size=365),
        "Conversions": np.random.randint(1, 50, size=365),
    })
    filtered_data = traffic_data.tail({"Last 30 Days": 30, "Last 3 Months": 90, "Last 6 Months": 180, "Last 12 Months": 365}[timeframe])
    col1, col2, col3 = st.columns(3)
    with col1:
        from streamlit_extras.metric_cards import style_metric_cards
        total_visitors = filtered_data["Visitors"].sum()
        total_conversions = filtered_data["Conversions"].sum()
        conversion_rate = f"{(total_conversions / total_visitors * 100):.2f}%" if total_visitors > 0 else "0.00%"
        st.metric("Total Visitors", f"{total_visitors}")
        st.metric("Total Conversions", f"{total_conversions}")
        st.metric("Conversion Rate", f"{conversion_rate}")
        style_metric_cards()
    with col2:
        st.write("### Traffic Trends")
        st.line_chart(filtered_data.set_index("Date"))
    with col3:
        st.write("### Search Queries")
        search_query_data = pd.DataFrame({
            "Query": [f"demo query {i}" for i in range(1, 21)],
            "CTR": np.random.uniform(1.0, 10.0, 20).round(2),
            "Impressions": np.random.randint(100, 10000, 20),
            "Clicks": np.random.randint(10, 500, 20),
        }).sort_values(by="Clicks", ascending=False)
        # Pagination
        page_size = 5
        num_pages = len(search_query_data) // page_size + (len(search_query_data) % page_size > 0)
        current_page = st.number_input("Page", min_value=1, max_value=num_pages, step=1, value=1)
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        st.dataframe(search_query_data.iloc[start_idx:end_idx], use_container_width=True)

# Technical Tab
with tabs[2]:
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
with tabs[3]:
    st.subheader("AI Suggestions")
    st.write("### Content Optimization Suggestions")
    st.write("- Improve the Meta Description to include the primary keyword.")
    st.write("- Add more internal links to related pages.")
    st.write("- Optimize images for faster load times.")
    st.write("### SEO Opportunities")
    st.write("- Target secondary keywords such as 'FedEx delivery times' and 'FedEx locations near me.'")
    st.write("- Acquire backlinks from industry-relevant domains.")

# Preview Tab
with tabs[4]:
    st.subheader("Embedded Page View")
    st.markdown(
        f'<iframe src="{selected_url}" width="100%" height="600" frameborder="0"></iframe>',
        unsafe_allow_html=True
    )

# Actions Tab
with tabs[5]:
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
