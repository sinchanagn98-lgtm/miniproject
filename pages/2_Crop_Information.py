

import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Indian Crop Information System",
    page_icon="🌾",
    layout="wide"
)

# Load crop dataset
DATA_PATH = Path(__file__).resolve().parent.parent / "crop_details.csv"

st.markdown("""
<style>
.stApp {
    background-color: #171614;
}
h1 {
    color: #278b39;
}
</style>
""", unsafe_allow_html=True)

st.title("🌾 Indian Crop Information System")
st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "Explore detailed information about crops grown in India"
    "</p>",
    unsafe_allow_html=True
)

st.divider()

st.header("🔍 Search Your Crop")

try:
    data = pd.read_csv(DATA_PATH)

    # Find crop name column
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

    # ONE searchable menu
    selected_crop = st.selectbox(
        "Search or select a crop",
        options=crop_names,
        index=None,
        placeholder="Type or select a crop name..."
    )

    if st.button("View Crop Information", type="primary"):

        if selected_crop:
            crop_info = data[
                data[crop_column].astype(str) == selected_crop
            ]

            st.subheader(f"🌱 {selected_crop}")

            for column in crop_info.columns:
                if column != crop_column:
                    value = crop_info.iloc[0][column]
                    st.markdown(f"**{column}:** {value}")
        else:
            st.warning("Please select a crop.")

except FileNotFoundError:
    st.error("crop_details.csv file not found. Please check your project folder.")

st.divider()

st.caption(
    "Indian Crop Information System | AI-Based Crop Prediction Project"
)
