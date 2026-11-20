


import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Indian Crop Information System",
    page_icon="🌾",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "crop_details.csv"
IMAGE_PATH = BASE_DIR / "crop_banner.png"

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #171614;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.main-title {
    color: #32a34b;
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    color: #aaaaaa;
    text-align: center;
    font-size: 17px;
    margin-bottom: 30px;
}

.search-heading {
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 15px;
}

.card-title {
    color: #68c878;
    font-size: 17px;
    font-weight: bold;
}

.card-value {
    color: white;
    font-size: 19px;
    font-weight: 600;
}

div.stButton > button {
    background-color: #24963d;
    color: white;
    border-radius: 10px;
    border: none;
    min-height: 48px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #18752d;
    color: white;
}

.footer {
    color: #999999;
    text-align: center;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# MAIN HEADING
# --------------------------------

st.markdown(
    '<div class="main-title">🌾 Indian Crop Information System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore detailed information about crops grown in India'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# BANNER IMAGE
# --------------------------------

if IMAGE_PATH.exists():
    st.image(str(IMAGE_PATH), use_container_width=True)


# --------------------------------
# SEARCH SECTION
# --------------------------------

st.markdown(
    '<div class="search-heading">🔍 Search Your Crop</div>',
    unsafe_allow_html=True
)


# --------------------------------
# LOAD DATASET
# --------------------------------

try:

    data = pd.read_csv(DATA_PATH)

    possible_columns = [
        "Crop Name",
        "crop_name",
        "Crop",
        "crop"
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


    # --------------------------------
    # ONE SEARCHABLE MENU
    # --------------------------------

    selected_crop = st.selectbox(
        "Search or select a crop",
        options=crop_names,
        index=None,
        placeholder="Type or select a crop name..."
    )

    st.write("")

    # --------------------------------
    # VIEW INFORMATION BUTTON
    # --------------------------------

    if st.button("🌱 View Crop Information", use_container_width=True):

        if selected_crop:

            crop_info = data[
                data[crop_column].astype(str) == selected_crop
            ]

            if not crop_info.empty:

                crop_row = crop_info.iloc[0]

                st.markdown("---")

                st.markdown(
                    f"## 🌾 {selected_crop} Information"
                )

                st.write("")

                # Collect available crop details
                details = []

                for column in data.columns:

                    if column != crop_column:

                        value = crop_row[column]

                        if pd.notna(value):

                            details.append((column, value))

                # --------------------------------
                # INFORMATION BOXES
                # --------------------------------

                columns = st.columns(2, gap="large")

                for index, (label, value) in enumerate(details):

                    with columns[index % 2]:

                        with st.container(border=True):

                            st.markdown(
                                f"<div class='card-title'>🌿 "
                                f"{label}</div>",
                                unsafe_allow_html=True
                            )

                            st.markdown("")

                            st.markdown(
                                f"<div class='card-value'>"
                                f"{value}</div>",
                                unsafe_allow_html=True
                            )

                        st.write("")

        else:

            st.warning("Please select a crop first.")


except FileNotFoundError:

    st.error("crop_details.csv file not found.")

except Exception as e:

    st.error(f"Error: {e}")


# --------------------------------
# FOOTER
# --------------------------------

st.write("")
st.divider()

st.markdown(
    '<div class="footer">'
    '🌱 Indian Crop Information System | '
    'AI-Based Crop Prediction Project'
    '</div>',
    unsafe_allow_html=True
)
