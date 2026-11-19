

import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Indian Crop Information",
    page_icon="🌾",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #2E7D32;
    font-size: 38px;
    font-weight: bold;
}
.sub-title {
    text-align: center;
    color: gray;
    font-size: 17px;
}
.crop-card {
    background-color: #F1F8E9;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">🌾 Indian Crop Information System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Explore detailed information about crops grown in India</div>',
    unsafe_allow_html=True
)

st.write("")

# Load CSV file
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "crop_details.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

try:
    if not DATA_PATH.exists():
        st.error("Crop dataset not found. Please upload crop_details.csv to the main project folder.")
        st.stop()

    data = load_data()

except Exception as e:
    st.error(f"Unable to load crop information: {e}")
    st.stop()

# Search section
st.subheader("🔍 Search Your Crop")

search = st.text_input(
    "Enter crop name",
    placeholder="Example: Rice, Wheat, Ragi, Maize..."
)

crop_list = sorted(data["crop_name"].dropna().unique())

# Filter search results
if search:
    matching_crops = [
        crop for crop in crop_list
        if search.lower() in crop.lower()
    ]
else:
    matching_crops = crop_list

if matching_crops:

    selected_crop = st.selectbox(
        "Select your crop",
        matching_crops
    )

    if st.button("View Crop Information", type="primary"):

        crop_data = data[
            data["crop_name"] == selected_crop
        ].iloc[0]

        st.divider()

        st.header(f"🌱 {selected_crop}")

        st.success("Crop information found successfully!")

        # Basic information
        st.subheader("📋 Basic Information")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Crop Category",
            str(crop_data["crop_category"])
        )

        col2.metric(
            "Growing Season",
            str(crop_data["growing_season"])
        )

        col3.metric(
            "Crop Duration",
            str(crop_data["crop_duration"])
        )

        st.divider()

        # Climate requirements
        st.subheader("🌤️ Climate Requirements")

        col1, col2, col3 = st.columns(3)

        col1.info(
            f"🌡️ Temperature\n\n{crop_data['temperature_c']} °C"
        )

        col2.info(
            f"🌧️ Annual Rainfall\n\n{crop_data['annual_rainfall_mm']} mm"
        )

        col3.info(
            f"💧 Water Requirement\n\n{crop_data['water_requirement']}"
        )

        st.divider()

        # Soil details
        st.subheader("🌍 Soil Requirements")

        st.write(crop_data["suitable_soil"])

        # Cultivation states
        st.subheader("📍 Major Growing States in India")

        st.write(crop_data["major_growing_states_india"])

        st.divider()

        # Fertilizer details
        st.subheader("🧪 Fertilizer Requirements")

        st.write(crop_data["fertilizer_guidance"])

        # Irrigation details
        st.subheader("🚿 Irrigation Methods")

        st.write(crop_data["irrigation_guidance"])

        st.divider()

        # Crop uses
        st.subheader("🛒 Uses of the Crop")

        st.write(crop_data["major_uses"])

        st.balloons()

else:
    st.warning(
        f"No crop found matching '{search}'. Please try another crop name."
    )

# Footer
st.divider()

st.caption(
    "Indian Crop Information System | AI-Based Crop Prediction Project"
)
