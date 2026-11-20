

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

# CSS DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #171614;
}

.block-container {
    max-width: 1100px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.main-title {
    color: #2e963e;
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    color: #aaaaaa;
    text-align: center;
    font-size: 18px;
    margin-bottom: 35px;
}

.search-title {
    color: white;
    font-size: 30px;
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
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #18752d;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# MAIN HEADING
st.markdown(
    '<div class="main-title">🌾 Indian Crop Information System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Explore detailed information about crops grown in India</div>',
    unsafe_allow_html=True
)

# AGRICULTURE IMAGE
if IMAGE_PATH.exists():
    st.image(
        str(IMAGE_PATH),
        use_container_width=True
    )
else:
    st.info("Upload crop_banner.png to the main project folder.")

# SPACE
st.write("")
st.write("")

# SEARCH SECTION
st.markdown(
    '<div class="search-title">🔍 Search Your Crop</div>',
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

    # ONLY ONE SEARCH MENU
    selected_crop = st.selectbox(
        "Search or select a crop",
        crop_names,
        index=None,
        placeholder="Type or select a crop name..."
    )

    st.write("")
    st.write("")

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

# FOOTER
st.write("")
st.write("")
st.divider()

st.markdown(
    "<center style='color:gray;'>"
    "🌱 Indian Crop Information System | AI-Based Crop Prediction Project"
    "</center>",
    unsafe_allow_html=True
)
