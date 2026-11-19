
import streamlit as st
import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parent

DATA_PATH = ROOT / "dataset" / "Crop_recommendationV2.csv"

st.set_page_config(
    page_title="AgriSmart",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AgriSmart")

st.subheader(
    "AI-Based Crop Recommendation and Farming Guidance System"
)

st.write(
    "Helping farmers select suitable crops based on "
    "soil properties and weather conditions."
)

st.image(
    "https://images.unsplash.com/photo-1500382017468-9049fed747ef",
    use_container_width=True
)

st.header("Welcome to Smart Agriculture!")

st.write("""
AgriSmart is an intelligent agricultural application
that helps farmers identify suitable crops.

Farmers can enter soil and weather information
and receive machine-learning-based crop recommendations.
""")

if DATA_PATH.exists():

    data = pd.read_csv(DATA_PATH)

    col1, col2 = st.columns(2)

    col1.metric(
        "Available Crop Records",
        len(data)
    )

    col2.metric(
        "Crop Categories",
        data["label"].nunique()
    )

st.divider()

st.header("Our Features")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌾 Crop Prediction")
    st.write(
        "Find suitable crops using soil nutrients "
        "and environmental conditions."
    )

    st.subheader("📘 Crop Information")
    st.write(
        "Learn about crop duration, growing seasons "
        "and common uses."
    )

with col2:
    st.subheader("🚜 Farming Guidance")
    st.write(
        "Explore water requirements, irrigation "
        "and fertilizer guidance."
    )

    st.subheader("🌦️ Weather Information")
    st.write(
        "View available weather observations "
        "for agricultural planning."
    )

st.divider()

st.info(
    "Use the navigation menu to explore the different "
    "features of AgriSmart."
)

st.caption(
    "AgriSmart | Smart Farming for a Better Future"
)

