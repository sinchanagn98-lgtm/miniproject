

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Indian Crop Information System",
    page_icon="🌾",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "crop_details.csv"
IMAGE_PATH = BASE_DIR / "crop_banner.png"

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #171614;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

h1 {
    color: #2e963e;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #aaaaaa;
    font-size: 18px;
    margin-bottom: 35px;
}

.search-heading {
    font-size: 27px;
    font-weight: bold;
    margin-top: 35px;
    margin-bottom: 20px;
}

div.stButton > button {
    background-color: #24963d;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 12px 25px;
    font-size: 17px;
}

div.stButton > button:hover {
    background-color: #18752d;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Heading
st.title("🌾 Indian Crop Information System")

st.markdown(
    '<p class="subtitle">Explore detailed information about crops grown in India</p>',
    unsafe_allow_html=True
)

# Agricultural banner
if IMAGE_PATH.exists():
    st.image(IMAGE_PATH, use_container_width=True)
else:
    st.warning("Please upload crop_banner.png to your main project folder.")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="search-heading">🔍 Search Your Crop</div>',
    unsafe_allow_html=True
)

try:
    data = pd.read_csv(DATA_PATH)

    possible_columns = [
        "Crop Name", "crop_name", "Crop", "crop"
    ]

    crop_column = next(
        (col for col in possible_columns if col in data.columns),
        None
    )

    if crop_column is None:
        st.error("Crop name column not found in CSV.")
        st.stop()

    crop_names = sorted(
        data[crop_column].dropna().astype(str).unique()
    )

    # Single searchable menu
    selected_crop = st.selectbox(
        "Search or select a crop",
        options=crop_names,
        index=None,
        placeholder="Type or select a crop name..."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🌱 View Crop Information"):

        if selected_crop:
            crop_info = data[
                data[crop_column].astype(str) == selected_crop
            ]

            st.subheader(f"🌾 {selected_crop}")

            for column in crop_info.columns:
                if column != crop_column:
                    st.markdown(
                        f"**{column}:** {crop_info.iloc[0][column]}"
                    )
        else:
            st.warning("Please select a crop.")

except FileNotFoundError:
    st.error("crop_details.csv file not found.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

st.caption(
    "🌱 Indian Crop Information System | AI-Based Crop Prediction Project"
)
