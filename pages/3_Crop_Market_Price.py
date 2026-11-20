


import streamlit as st
import pandas as pd
import requests

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Live Crop Market Prices",
    page_icon="🌾",
    layout="wide"
)

API_URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.main-title {
    font-size: 34px;
    font-weight: bold;
    color: #4CAF50;
}
.info-card {
    background: #193b29;
    border: 1px solid #38734c;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}
.info-card p {
    color: #b7e4c7;
    margin-bottom: 5px;
}
.info-card h2 {
    color: white;
}
.section-title {
    color: #4CAF50;
    font-size: 25px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">🌾 Live Crop Market Price Dashboard</p>',
    unsafe_allow_html=True
)

st.write(
    "Explore the latest reported agricultural wholesale "
    "prices from markets across India."
)

st.caption(
    "Data source: Government of India – AGMARKNET / data.gov.in"
)

st.markdown("---")

# ==========================================
# API KEY
# ==========================================

try:
    API_KEY = st.secrets["DATA_GOV_API_KEY"]
except Exception:
    st.error(
        "Government API key not found. Please add "
        "DATA_GOV_API_KEY to .streamlit/secrets.toml."
    )
    st.stop()

# ==========================================
# FETCH GOVERNMENT MARKET DATA
# ==========================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_market_data(api_key):

    all_records = []
    limit = 1000

    for offset in range(0, 5000, limit):

        params = {
            "api-key": api_key,
            "format": "json",
            "limit": limit,
            "offset": offset
        }

        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        records = result.get("records", [])

        if not records:
            break

        all_records.extend(records)

        total = int(result.get("total", 0))

        if len(all_records) >= total:
            break

        if len(records) < limit:
            break

    if not all_records:
        raise ValueError(
            "The government API returned no market records."
        )

    data = pd.DataFrame(all_records)

    # Standardize column names
    data.columns = [
        str(col).strip().lower().replace(" ", "_")
        for col in data.columns
    ]

    # Required API fields
    required = [
        "state",
        "district",
        "market",
        "commodity",
        "arrival_date",
        "min_price",
        "max_price",
        "modal_price"
    ]

    missing = [
        col for col in required
        if col not in data.columns
    ]

    if missing:
        raise ValueError(
            "API response is missing fields: "
            + ", ".join(missing)
        )

    # Convert prices to numeric
    for col in ["min_price", "max_price", "modal_price"]:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    # Convert arrival date
    data["arrival_date"] = pd.to_datetime(
        data["arrival_date"],
        errors="coerce",
        dayfirst=True
    )

    # Clean records
    data = data.dropna(
        subset=[
            "state", "district", "market",
            "commodity", "min_price",
            "max_price", "modal_price"
        ]
    )

    return data


# ==========================================
# REFRESH DATA
# ==========================================

if st.button("🔄 Refresh Latest Market Prices"):

    get_market_data.clear()

    st.rerun()

# ==========================================
# LOAD DATA
# ==========================================

try:

    with st.spinner(
        "Fetching latest reported market prices from Government of India..."
    ):

        df = get_market_data(API_KEY)

    st.success(
        f"Successfully fetched {len(df):,} market price records."
    )

except Exception as error:

    st.error(
        f"Unable to fetch government market data: {error}"
    )

    st.info(
        "Check your API key, internet connection and "
        "data.gov.in API availability."
    )

    st.stop()

# ==========================================
# DATA SOURCE INFORMATION
# ==========================================

latest_date = df["arrival_date"].max()

if pd.notna(latest_date):

    st.info(
        f"Latest reported market arrival date: "
        f"{latest_date.strftime('%d-%m-%Y')}"
    )

st.caption(
    "Prices are daily reported wholesale prices, not "
    "instantaneous live trading prices. The API data "
    "may have reporting delays."
)

# ==========================================
# SEARCH FILTERS
# ==========================================

st.markdown("---")

st.markdown(
    '<p class="section-title">🔍 Search Market Prices</p>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

# CROP FILTER

with col1:

    crops = ["All Crops"] + sorted(
        df["commodity"].dropna().astype(str).unique()
    )

    selected_crop = st.selectbox(
        "Select Crop",
        crops
    )

crop_df = df.copy()

if selected_crop != "All Crops":

    crop_df = crop_df[
        crop_df["commodity"] == selected_crop
    ]

# STATE FILTER

with col2:

    states = ["All States"] + sorted(
        crop_df["state"].dropna().astype(str).unique()
    )

    selected_state = st.selectbox(
        "Select State",
        states
    )

state_df = crop_df.copy()

if selected_state != "All States":

    state_df = state_df[
        state_df["state"] == selected_state
    ]

# DISTRICT FILTER

with col3:

    districts = ["All Districts"] + sorted(
        state_df["district"].dropna().astype(str).unique()
    )

    selected_district = st.selectbox(
        "Select District",
        districts
    )

district_df = state_df.copy()

if selected_district != "All Districts":

    district_df = district_df[
        district_df["district"] == selected_district
    ]

# MARKET FILTER

markets = ["All Markets"] + sorted(
    district_df["market"].dropna().astype(str).unique()
)

selected_market = st.selectbox(
    "Select Market / Mandi",
    markets
)

filtered_df = district_df.copy()

if selected_market != "All Markets":

    filtered_df = filtered_df[
        filtered_df["market"] == selected_market
    ]

# ==========================================
# MARKET PRICE SUMMARY
# ==========================================

st.markdown("---")

st.markdown(
    '<p class="section-title">📊 Market Price Summary</p>',
    unsafe_allow_html=True
)

if not filtered_df.empty:

    min_price = filtered_df["min_price"].min()

    max_price = filtered_df["max_price"].max()

    avg_price = filtered_df["modal_price"].mean()

    best_market = filtered_df.loc[
        filtered_df["modal_price"].idxmax()
    ]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Minimum Price",
            f"₹{min_price:,.0f}"
        )

    with c2:
        st.metric(
            "Maximum Price",
            f"₹{max_price:,.0f}"
        )

    with c3:
        st.metric(
            "Average Modal Price",
            f"₹{avg_price:,.0f}"
        )

    with c4:
        st.metric(
            "Highest Price Market",
            str(best_market["market"])
        )

    st.caption(
        "Price unit: ₹ per quintal. Summary values are based "
        "on the records currently selected."
    )

    # ======================================
    # PRICE COMPARISON CHART
    # ======================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">📈 Market Price Comparison</p>',
        unsafe_allow_html=True
    )

    chart_df = filtered_df.sort_values(
        "modal_price",
        ascending=False
    ).copy()

    chart_df["Market Label"] = (
        chart_df["market"].astype(str)
        + " - "
        + chart_df["district"].astype(str)
    )

    chart_df = chart_df.drop_duplicates(
        subset=["Market Label", "commodity", "arrival_date"]
    )

    chart_df = chart_df.head(20)

    st.bar_chart(
        chart_df.set_index("Market Label")[
            ["min_price", "modal_price", "max_price"]
        ],
        height=400
    )

    # ======================================
    # MARKET PRICE TABLE
    # ======================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">📋 Market Price Details</p>',
        unsafe_allow_html=True
    )

    display_columns = [
        "arrival_date",
        "state",
        "district",
        "market",
        "commodity"
    ]

    if "variety" in filtered_df.columns:
        display_columns.append("variety")

    display_columns += [
        "min_price",
        "max_price",
        "modal_price"
    ]

    display_df = filtered_df[
        display_columns
    ].copy()

    display_df = display_df.rename(
        columns={
            "arrival_date": "Arrival Date",
            "state": "State",
            "district": "District",
            "market": "Market",
            "commodity": "Crop",
            "variety": "Variety",
            "min_price": "Minimum Price",
            "max_price": "Maximum Price",
            "modal_price": "Modal Price"
        }
    )

    display_df = display_df.sort_values(
        "Arrival Date",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # BEST MARKET INFORMATION
    # ======================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">🏆 Highest Modal Price</p>',
        unsafe_allow_html=True
    )

    st.success(
        f"Highest modal price in the selected results: "
        f"{best_market['market']}, "
        f"{best_market['district']}, "
        f"{best_market['state']}."
    )

    st.write(
        f"**Crop:** {best_market['commodity']}"
    )

    st.write(
        f"**Modal Price:** ₹{best_market['modal_price']:,.0f} "
        "per quintal"
    )

    st.write(
        f"**Arrival Date:** "
        f"{best_market['arrival_date'].strftime('%d-%m-%Y')}"
        if pd.notna(best_market["arrival_date"])
        else "**Arrival Date:** Not available"
    )

    # ======================================
    # DOWNLOAD REPORT
    # ======================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">⬇️ Download Market Report</p>',
        unsafe_allow_html=True
    )

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Market Price CSV",
        data=csv_data,
        file_name="live_crop_market_prices.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "No matching market records found. "
        "Try selecting All Crops, All States or All Districts."
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h4>🌱 Indian Agriculture Information System</h4>
        <p>Supporting farmers with agricultural market information.</p>
        <p>Source: AGMARKNET / data.gov.in</p>
    </div>
    """,
    unsafe_allow_html=True
)
