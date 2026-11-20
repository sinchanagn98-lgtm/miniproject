
import streamlit as st
import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DETAILS_PATH = ROOT / "dataset" / "crop_details.csv"

st.title("🚜 Farming Guidance")

st.write(
    "Get crop-specific guidance for better farm management."
)

if DETAILS_PATH.exists():

    details = pd.read_csv(DETAILS_PATH)
    
    if "crop_name" in details.columns:
    crop_column = "crop_name"
elif "crop" in details.columns:
    crop_column = "crop"
else:
    st.error("Crop name column is missing.")
    st.write("Available columns:", details.columns.tolist())
    st.stop()

crops = details[crop_column].dropna().astype(str).tolist()

    

    default_crop = st.session_state.get(
        "selected_crop",
        crops[0] if crops else None
    )

    if not crops:
        st.warning("No crop information available.")
        st.stop()

    if default_crop not in crops:
        default_crop = crops[0]

    crop = st.selectbox(
        "Choose your crop",
        crops,
        index=crops.index(default_crop)
    )

    result = details[
        details["crop"].astype(str).str.lower()
        == crop.lower()
    ]

    if not result.empty:

        row = result.iloc[0]

        guidance_fields = {
            "Water Requirement": "water_requirement",
            "Irrigation Method": "irrigation_guidance",
            "Fertilizer Guidance": "fertilizer_guidance",
            "Growing Season": "growing_season",
            "Crop Duration": "duration_days",
            "Suitable Soil": "soil_suitability"
        }

        for title, column in guidance_fields.items():

            if column in details.columns:

                value = row[column]

                st.subheader(title)

                if pd.notna(value) and str(value).strip():
                    st.write(value)
                else:
                    st.info("Information not yet added.")

        st.success(
            "Use verified local agricultural advice "
            "before making farming decisions."
        )

else:
    st.warning("Crop details dataset not found.")

