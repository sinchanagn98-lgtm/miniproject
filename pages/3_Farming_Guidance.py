

import streamlit as st
import pandas as pd
from pathlib import Path

# Find the project folder
ROOT = Path(__file__).resolve().parents[1]

# CSV file location
DETAILS_PATH = ROOT / "dataset" / "crop_details.csv"

st.title("🚜 Farming Guidance")
st.write("Get crop-specific guidance for better farm management.")

# Check whether the CSV exists
if not DETAILS_PATH.exists():
    st.error("Crop details dataset not found.")
    st.write("Expected file location:", str(DETAILS_PATH))
    st.stop()

# Read CSV file
details = pd.read_csv(DETAILS_PATH)

# Support both crop and crop_name column names
if "crop_name" in details.columns:
    crop_column = "crop_name"
elif "crop" in details.columns:
    crop_column = "crop"
else:
    st.error("Crop name column is missing.")
    st.write("Available columns:", details.columns.tolist())
    st.stop()

# Get crop names
crops = details[crop_column].dropna().astype(str).tolist()

if not crops:
    st.warning("No crop information available.")
    st.stop()

# Select crop
default_crop = st.session_state.get("selected_crop", crops[0])

if default_crop not in crops:
    default_crop = crops[0]

crop = st.selectbox(
    "Choose your crop",
    crops,
    index=crops.index(default_crop)
)

# Find selected crop
result = details[
    details[crop_column].astype(str).str.lower() == crop.lower()
]

if not result.empty:
    row = result.iloc[0]

    # Match alternative CSV column names
    guidance_fields = {
        "Water Requirement": ["water_requirement"],
        "Irrigation Method": ["irrigation_guidance"],
        "Fertilizer Guidance": ["fertilizer_guidance"],
        "Growing Season": ["growing_season"],
        "Crop Duration": ["crop_duration", "duration_days"],
        "Suitable Soil": ["suitable_soil", "soil_suitability"],
        "Major Uses": ["major_uses", "uses"]
    }

    for title, possible_columns in guidance_fields.items():
        st.subheader(title)

        column = next(
            (col for col in possible_columns if col in details.columns),
            None
        )

        if column is not None:
            value = row[column]

            if pd.notna(value) and str(value).strip():
                st.write(value)
            else:
                st.info("Information not yet added.")
        else:
            st.info("This information is not available in the CSV.")

    st.success(
        "Use verified local agricultural advice "
        "before making farming decisions."
    )
