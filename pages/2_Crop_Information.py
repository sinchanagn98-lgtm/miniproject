
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

if not DATA_PATH.exists():
    st.error("crop_details.csv not found in the main project folder.")
    st.stop()

data = load_data()

# Search section
st.subheader("🔍 Search Your Crop")

search = st.text_input(
    "Enter crop name",
    placeholder="Example: Rice, Wheat, Ragi, Maize..."
)

crop_list = sorted(data["crop_name"].dropna().unique())

# Search filtering
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

        # Basic Information
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

        # Planting months
        if "planting_or_season_months" in data.columns:
            st.info(
                "📅 Planting / Season Months: "
                + str(crop_data["planting_or_season_months"])
            )

        st.divider()

        # Climate requirements
        st.subheader("🌤️ Climate Requirements")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Temperature",
            str(crop_data["temperature_c"]) + " °C"
        )

        col2.metric(
            "Annual Rainfall",
            str(crop_data["annual_rainfall_mm"]) + " mm"
        )

        col3.metric(
            "Water Requirement",
            str(crop_data["water_requirement"])
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
