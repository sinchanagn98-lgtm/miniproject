


import streamlit as st
import pandas as pd
import html
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Indian Crop Information System",
    page_icon="🌾",
    layout="wide"
)

# --------------------------------
# FILE PATHS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "crop_details.csv"
IMAGE_PATH = BASE_DIR / "crop_banner.png"

# --------------------------------
# CUSTOM CSS DESIGN
# --------------------------------

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

/* Main heading */

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

/* Search heading */

.search-title {
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-top: 35px;
    margin-bottom: 20px;
}

/* Search button */

div.stButton > button {
    background-color: #24963d;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 12px 25px;
    font-size: 17px;
    font-weight: bold;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #18752d;
    color: white;
    border: 1px solid #35a64b;
}

/* Information cards */

.info-card {
    background: #262923;
    border: 1px solid #3c4938;
    border-radius: 15px;
    padding: 22px;
    margin-bottom: 18px;
    min-height: 125px;
    transition: 0.3s;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.info-card:hover {
    border-color: #35a64b;
    background: #30382e;
    transform: translateY(-3px);
}

.info-title {
    color: #70c77b;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 12px;
}

.info-value {
    color: white;
    font-size: 19px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

/* Result heading */

.result-heading {
    color: #39a84b;
    font-size: 28px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 20px;
}

/* Footer */

.footer {
    color: #999999;
    text-align: center;
    font-size: 14px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# MAIN HEADING
# --------------------------------

st.markdown(
    '<div class="main-title">'
    '🌾 Indian Crop Information System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore detailed information about crops grown in India'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# AGRICULTURAL BANNER IMAGE
# --------------------------------

if IMAGE_PATH.exists():

    st.image(
        str(IMAGE_PATH),
        use_container_width=True
    )

else:
    st.warning(
        "Please upload crop_banner.png "
        "to your main project folder."
    )


# --------------------------------
# SEARCH SECTION
# --------------------------------

st.write("")
st.write("")

st.markdown(
    '<div class="search-title">'
    '🔍 Search Your Crop'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# LOAD CROP DATASET
# --------------------------------

try:

    data = pd.read_csv(DATA_PATH)

    # Identify crop name column

    possible_columns = [
        "Crop Name",
        "crop_name",
        "Crop",
        "crop"
    ]

    crop_column = next(
        (
            col for col in possible_columns
            if col in data.columns
        ),
        None
    )

    if crop_column is None:

        st.error(
            "Crop name column not found in CSV file."
        )

        st.stop()

    # Get crop names

    crop_names = sorted(
        data[crop_column]
        .dropna()
        .astype(str)
        .unique()
    )


    # --------------------------------
    # SINGLE SEARCHABLE MENU
    # --------------------------------

    selected_crop = st.selectbox(
        "Search or select a crop",

        options=crop_names,

        index=None,

        placeholder="Type or select a crop name..."
    )

    st.write("")
    st.write("")


    # --------------------------------
    # VIEW CROP INFORMATION BUTTON
    # --------------------------------

    if st.button("🌱 View Crop Information"):

        if selected_crop:

            crop_info = data[
                data[crop_column].astype(str)
                == selected_crop
            ]

            if not crop_info.empty:

                crop_row = crop_info.iloc[0]

                st.markdown(
                    f'<div class="result-heading">'
                    f'🌾 {html.escape(selected_crop)} Information'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # --------------------------------
                # DISPLAY INFORMATION IN BOXES
                # --------------------------------

                details = []

                for column in data.columns:

                    if column != crop_column:

                        value = crop_row[column]

                        if pd.notna(value):

                            details.append(
                                (column, value)
                            )

                # Two-column card layout

                columns = st.columns(2)

                for index, (column, value) in enumerate(details):

                    with columns[index % 2]:

                        title = html.escape(str(column))

                        content = html.escape(str(value))

                        st.markdown(f"""
                        <div class="info-card">

                            <div class="info-title">
                                🌿 {title}
                            </div>

                            <div class="info-value">
                                {content}
                            </div>

                        </div>
                        """, unsafe_allow_html=True)

            else:

                st.warning("Crop information not available.")

        else:

            st.warning("Please select a crop first.")


# --------------------------------
# ERROR HANDLING
# --------------------------------

except FileNotFoundError:

    st.error(
        "crop_details.csv file not found. "
        "Please check your project folder."
    )

except Exception as e:

    st.error(f"Something went wrong: {e}")


# --------------------------------
# FOOTER
# --------------------------------

st.write("")
st.write("")

st.divider()

st.markdown(
    '<div class="footer">'
    '🌱 Indian Crop Information System '
    '| AI-Based Crop Prediction Project'
    '</div>',
    unsafe_allow_html=True
)
