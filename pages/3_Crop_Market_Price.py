


import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Crop Market Price",
    page_icon="🌾",
    layout="wide"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #4CAF50;
}

.info-box {
    background-color: #1e3527;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #3d704e;
}

.info-box h4 {
    color: #b7e4c7;
}

.info-box h2 {
    color: white;
}

.section-title {
    color: #4CAF50;
    font-size: 25px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE HEADING
# ==========================================

st.markdown(
    '<p class="main-title">🌾 Crop Market Price Dashboard</p>',
    unsafe_allow_html=True
)

st.write(
    "Explore agricultural crop prices, compare markets "
    "and find suitable selling locations across India."
)

st.markdown("---")

# ==========================================
# SAMPLE DATASET
# ==========================================

sample_data = {
    "Crop": [
        "Rice", "Rice", "Rice",
        "Wheat", "Wheat", "Wheat",
        "Maize", "Maize", "Maize",
        "Cotton", "Cotton", "Cotton",
        "Sugarcane", "Sugarcane", "Sugarcane",
        "Tomato", "Tomato", "Tomato",
        "Onion", "Onion", "Onion"
    ],

    "State": [
        "Karnataka", "Punjab", "Tamil Nadu",
        "Karnataka", "Punjab", "Haryana",
        "Karnataka", "Maharashtra", "Andhra Pradesh",
        "Gujarat", "Maharashtra", "Telangana",
        "Karnataka", "Uttar Pradesh", "Maharashtra",
        "Karnataka", "Maharashtra", "Tamil Nadu",
        "Karnataka", "Maharashtra", "Madhya Pradesh"
    ],

    "Market": [
        "Bengaluru", "Amritsar", "Madurai",
        "Mysuru", "Ludhiana", "Karnal",
        "Belagavi", "Pune", "Guntur",
        "Rajkot", "Nagpur", "Warangal",
        "Mandya", "Meerut", "Kolhapur",
        "Kolar", "Pune", "Chennai",
        "Bengaluru", "Nashik", "Indore"
    ],

    "Min Price": [
        2200, 2400, 2300,
        2100, 2200, 2150,
        1800, 1900, 1850,
        6500, 6700, 6600,
        300, 320, 310,
        1800, 1600, 1700,
        2000, 1900, 1850
    ],

    "Max Price": [
        2800, 2900, 2750,
        2600, 2700, 2650,
        2400, 2500, 2350,
        7500, 7800, 7600,
        380, 400, 390,
        2800, 2600, 2700,
        3000, 2800, 2700
    ],

    "Modal Price": [
        2500, 2650, 2550,
        2400, 2500, 2450,
        2100, 2250, 2200,
        7000, 7300, 7100,
        350, 370, 360,
        2300, 2200, 2400,
        2500, 2400, 2300
    ]
}

demo_df = pd.DataFrame(sample_data)

demo_df["Date"] = pd.Timestamp.today().normalize()

# ==========================================
# UPLOAD DATASET
# ==========================================

st.markdown(
    '<p class="section-title">📁 Upload Market Price Dataset</p>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your crop market price CSV file",
    type=["csv"]
)

required_columns = [
    "Crop", "State", "Market",
    "Min Price", "Max Price",
    "Modal Price", "Date"
]

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            st.error(
                "Missing columns: " +
                ", ".join(missing_columns)
            )
            st.stop()

        # Convert numeric columns
        price_columns = [
            "Min Price", "Max Price", "Modal Price"
        ]

        for col in price_columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

        df["Date"] = pd.to_datetime(
            df["Date"], errors="coerce"
        )

        df = df.dropna(subset=required_columns)

        if df.empty:
            st.error("No valid records found in the uploaded CSV.")
            st.stop()

        st.success("Dataset uploaded successfully!")

    except Exception as e:
        st.error(f"Unable to read the CSV file: {e}")
        st.stop()

else:

    df = demo_df.copy()

    st.info(
        "Showing illustrative sample market prices. "
        "Upload verified market data for actual reported prices."
    )

# ==========================================
# SEARCH AND FILTER SECTION
# ==========================================

st.markdown("---")

st.markdown(
    '<p class="section-title">🔍 Search Crop Prices</p>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

# CROP FILTER

with col1:

    crop_options = ["All Crops"] + sorted(
        df["Crop"].astype(str).unique().tolist()
    )

    selected_crop = st.selectbox(
        "Select Crop",
        crop_options
    )

crop_df = df.copy()

if selected_crop != "All Crops":

    crop_df = crop_df[
        crop_df["Crop"] == selected_crop
    ]

# STATE FILTER

with col2:

    state_options = ["All States"] + sorted(
        crop_df["State"].astype(str).unique().tolist()
    )

    selected_state = st.selectbox(
        "Select State",
        state_options
    )

state_df = crop_df.copy()

if selected_state != "All States":

    state_df = state_df[
        state_df["State"] == selected_state
    ]

# MARKET FILTER

with col3:

    market_options = ["All Markets"] + sorted(
        state_df["Market"].astype(str).unique().tolist()
    )

    selected_market = st.selectbox(
        "Select Market",
        market_options
    )

filtered_df = state_df.copy()

if selected_market != "All Markets":

    filtered_df = filtered_df[
        filtered_df["Market"] == selected_market
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

    min_price = filtered_df["Min Price"].min()

    max_price = filtered_df["Max Price"].max()

    avg_price = filtered_df["Modal Price"].mean()

    best_market = filtered_df.loc[
        filtered_df["Modal Price"].idxmax()
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
            best_market["Market"]
        )

    st.caption(
        "All prices are displayed in ₹ per quintal."
    )

# ==========================================
# PRICE COMPARISON CHART
# ==========================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">📈 Market Price Comparison</p>',
        unsafe_allow_html=True
    )

    chart_df = filtered_df.sort_values(
        "Modal Price",
        ascending=False
    )

    st.bar_chart(
        chart_df.set_index("Market")[
            ["Min Price", "Modal Price", "Max Price"]
        ],
        height=400
    )

# ==========================================
# MARKET PRICE DETAILS
# ==========================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">📋 Market Price Details</p>',
        unsafe_allow_html=True
    )

    display_df = filtered_df[
        [
            "Crop",
            "State",
            "Market",
            "Date",
            "Min Price",
            "Max Price",
            "Modal Price"
        ]
    ].sort_values(
        "Modal Price",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# BEST MARKET INFORMATION
# ==========================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">🏆 Best Price Market</p>',
        unsafe_allow_html=True
    )

    st.success(
        f"Highest modal price is available in "
        f"{best_market['Market']}, "
        f"{best_market['State']}."
    )

    st.write(
        f"**Crop:** {best_market['Crop']}"
    )

    st.write(
        f"**Market:** {best_market['Market']}"
    )

    st.write(
        f"**Modal Price:** ₹{best_market['Modal Price']:,.0f} "
        "per quintal"
    )

# ==========================================
# DOWNLOAD REPORT
# ==========================================

    st.markdown("---")

    st.markdown(
        '<p class="section-title">⬇️ Download Market Report</p>',
        unsafe_allow_html=True
    )

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Market Price Report",
        data=csv_data,
        file_name="crop_market_price_report.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "No market price information found. "
        "Please change your search filters."
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h4>🌱 Indian Agriculture Information System</h4>
        <p>Helping farmers make better agricultural decisions.</p>
    </div>
    """,
    unsafe_allow_html=True
)
