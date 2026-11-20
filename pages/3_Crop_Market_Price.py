

import streamlit as st
import pandas as pd

# --------------------------------
# PAGE TITLE
# --------------------------------

st.title("🌾 Crop Market Price")
st.write(
    "Check and compare agricultural crop prices "
    "across different markets in India."
)

st.markdown("---")

# --------------------------------
# SAMPLE MARKET PRICE DATA
# --------------------------------
# These are illustrative demo prices,
# NOT actual live market prices.

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

# --------------------------------
# UPLOAD MARKET DATA
# --------------------------------

st.subheader("📁 Upload Market Price Dataset")

uploaded_file = st.file_uploader(
    "Upload your crop market price CSV file",
    type=["csv"]
)

required_columns = [
    "Crop", "State", "Market", "Min Price",
    "Max Price", "Modal Price", "Date"
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
                "Missing columns: "
                + ", ".join(missing_columns)
            )
            st.stop()

        df["Date"] = pd.to_datetime(
            df["Date"], errors="coerce"
        )

        for col in ["Min Price", "Max Price", "Modal Price"]:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

        df = df.dropna(subset=required_columns)

        st.success("Market price dataset uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()

else:
    df = demo_df.copy()

    st.info(
        "Showing illustrative sample data. "
        "Upload a verified market price CSV to see actual "
        "reported prices."
    )

# --------------------------------
# FILTER SECTION
# --------------------------------

st.markdown("---")
st.subheader("🔍 Search Crop Prices")

col1, col2, col3 = st.columns(3)

with col1:
    crop_options = ["All Crops"] + sorted(
        df["Crop"].astype(str).unique().tolist()
    )

    selected_crop = st.selectbox(
        "Select Crop",
        crop_options
    )

with col2:
    state_options = ["All States"] + sorted(
        df["State"].astype(str).unique().tolist()
    )

    selected_state = st.selectbox(
        "Select State",
        state_options
    )

with col3:
    market_options = ["All Markets"] + sorted(
        df["Market"].astype(str).unique().tolist()
    )

    selected_market = st.selectbox(
        "Select Market",
        market_options
    )

filtered_df = df.copy()

if selected_crop != "All Crops":
    filtered_df = filtered_df[
        filtered_df["Crop"] == selected_crop
    ]

if selected_state != "All States":
    filtered_df = filtered_df[
        filtered_df["State"] == selected_state
    ]

if selected_market != "All Markets":
    filtered_df = filtered_df[
        filtered_df["Market"] == selected_market
    ]

# --------------------------------
# PRICE SUMMARY
# --------------------------------

st.markdown("---")
st.subheader("📊 Market Price Summary")

if not filtered_df.empty:

    best_market = filtered_df.loc[
        filtered_df["Modal Price"].idxmax()
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Minimum Price",
        f"₹{filtered_df['Min Price'].min():,.0f}"
    )

    c2.metric(
        "Maximum Price",
        f"₹{filtered_df['Max Price'].max():,.0f}"
    )

    c3.metric(
        "Average Modal Price",
        f"₹{filtered_df['Modal Price'].mean():,.0f}"
    )

    c4.metric(
        "Highest Price Market",
        best_market["Market"]
    )

    st.caption(
        "Prices are in Indian Rupees per quintal (₹/quintal). "
        "The highest-price market is based on modal price."
    )

    # --------------------------------
    # PRICE COMPARISON CHART
    # --------------------------------

    st.markdown("---")
    st.subheader("📈 Market Price Comparison")

    chart_df = filtered_df.sort_values(
        "Modal Price", ascending=False
    )

    st.bar_chart(
        chart_df.set_index("Market")[
            ["Min Price", "Modal Price", "Max Price"]
        ]
    )

    # --------------------------------
    # MARKET PRICE TABLE
    # --------------------------------

    st.markdown("---")
    st.subheader("📋 Crop Market Price Details")

    display_df = filtered_df[
        [
            "Crop", "State", "Market", "Date",
            "Min Price", "Max Price", "Modal Price"
        ]
    ].sort_values("Modal Price", ascending=False)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # BEST MARKET
    # --------------------------------

    st.markdown("---")
    st.subheader("🏆 Best Price Market")

    st.success(
        f"The highest modal price is in "
        f"{best_market['Market']}, "
        f"{best_market['State']}."
    )

    st.write(
        f"**Crop:** {best_market['Crop']}"
    )

    st.write(
        f"**Modal Price:** ₹{best_market['Modal Price']:,.0f} "
        "per quintal"
    )

    # --------------------------------
    # DOWNLOAD CSV
    # --------------------------------

    st.markdown("---")
    st.subheader("⬇️ Download Market Report")

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Crop Market Price Report",
        data=csv_data,
        file_name="crop_market_price_report.csv",
        mime="text/csv"
    )

else:
    st.warning(
        "No market price information found. "
        "Please change your search filters."
    )

# --------------------------------
# FOOTER
# --------------------------------

st.markdown("---")

st.caption(
    "🌱 Indian Agriculture Information System | "
    "Crop Market Price Dashboard"
)
