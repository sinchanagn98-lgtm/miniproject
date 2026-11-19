
import streamlit as st
import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "dataset" / "crop_details.csv"
DETAILS_PATH = ROOT / "dataset" / "crop_details.csv"

st.title("🌾 Crop Information")

data = pd.read_csv(DATA_PATH)

crops = sorted(data["label"].unique())

default_crop = st.session_state.get(
    "selected_crop", crops[0]
)

if default_crop not in crops:
    default_crop = crops[0]

crop = st.selectbox(
    "Select a crop",
    crops,
    index=crops.index(default_crop)
)

st.subheader(crop.title())

st.write(
    "Explore the growing conditions and "
    "agricultural information for this crop."
)

if DETAILS_PATH.exists():

    details = pd.read_csv(DETAILS_PATH)

    if "crop" in details.columns:

        result = details[
            details["crop"].astype(str).str.lower()
            == crop.lower()
        ]

        if not result.empty:

            row = result.iloc[0]

            fields = [
                "growing_season",
                "duration_days",
                "water_requirement",
                "irrigation_guidance",
                "soil_suitability",
                "fertilizer_guidance",
                "common_uses",
                "marketing_options"
            ]

            for field in fields:

                if field in details.columns:

                    value = row[field]

                    if pd.notna(value) and str(value).strip():

                        st.markdown(
                            f"**{field.replace('_', ' ').title()}**"
                        )

                        st.write(value)

                    else:
                        st.write(
                            f"Information not added: "
                            f"{field.replace('_', ' ')}"
                        )

        else:
            st.warning("Crop information is not available.")

    else:
        st.error("Please check crop_details.csv.")

else:
    st.warning("Please upload crop_details.csv.")

