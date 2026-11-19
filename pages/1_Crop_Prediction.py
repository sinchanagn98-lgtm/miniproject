import os
import sys
import streamlit as st
import pandas as pd

FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
    "soil_moisture",
    "soil_type",
    "sunlight_exposure",
    "wind_speed",
    "organic_matter"
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from model.train_model import load_model

model = load_model()
import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR, "dataset", "Crop_recommendationV2.csv"
)

data = pd.read_csv(DATA_PATH)
model = load_model()

st.info(
    "Enter values from your soil test and local weather "
    "measurements. Soil type is entered using dataset codes."
)

with st.form("prediction_form"):

    st.subheader("Soil Nutrients")

    col1, col2, col3 = st.columns(3)

    with col1:
        N = st.number_input(
            "Nitrogen (N)", min_value=0.0,
            value=50.0, step=1.0
        )

    with col2:
        P = st.number_input(
            "Phosphorus (P)", min_value=0.0,
            value=50.0, step=1.0
        )

    with col3:
        K = st.number_input(
            "Potassium (K)", min_value=0.0,
            value=50.0, step=1.0
        )

    st.subheader("Soil and Weather Conditions")

    col1, col2 = st.columns(2)

    with col1:
        temperature = st.number_input(
            "Temperature (°C)", value=25.0
        )

        humidity = st.number_input(
            "Humidity (%)", min_value=0.0,
            max_value=100.0, value=70.0
        )

        rainfall = st.number_input(
            "Rainfall (mm)", min_value=0.0,
            value=100.0
        )

        ph = st.number_input(
            "Soil pH", min_value=0.0,
            max_value=14.0, value=6.5
        )

        soil_type = st.selectbox(
            "Soil Type Code",
            options=sorted(data["soil_type"].unique().tolist()),
            help="The dataset only identifies soil types as codes 1, 2 and 3. Their names are not provided."
        )

    with col2:
        soil_moisture = st.number_input(
            "Soil Moisture",
            min_value=0.0, value=20.0
        )

        sunlight_exposure = st.number_input(
            "Sunlight Exposure",
            min_value=0.0, value=8.0
        )

        wind_speed = st.number_input(
            "Wind Speed", min_value=0.0, value=5.0
        )

        organic_matter = st.number_input(
            "Organic Matter",
            min_value=0.0, value=5.0
        )

    submit = st.form_submit_button(
        "🌱 Predict Suitable Crops"
    )

if submit:

    input_data = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
        "soil_moisture": soil_moisture,
        "soil_type": str(soil_type),
        "sunlight_exposure": sunlight_exposure,
        "wind_speed": wind_speed,
        "organic_matter": organic_matter
    }], columns=FEATURES)

    probabilities = model.predict_proba(input_data)[0]

    top_indices = probabilities.argsort()[-3:][::-1]

    st.success("Prediction completed!")

    st.subheader("Your Recommended Crops")

    for rank, index in enumerate(top_indices, start=1):

        crop = model.classes_[index]
        confidence = probabilities[index] * 100

        st.write(f"### {rank}. {crop.title()}")
        st.progress(float(probabilities[index]))

        st.write(
            f"Model score: {confidence:.2f}%"
        )

        if rank == 1:
            st.session_state["selected_crop"] = crop

    st.info(
        "These are model scores, not guaranteed chances "
        "of successful farming. Check local conditions "
        "before planting."
    )

    st.write(
        "Go to the Crop Information and Farming Guidance "
        "pages to learn more about the recommended crop."
    )

