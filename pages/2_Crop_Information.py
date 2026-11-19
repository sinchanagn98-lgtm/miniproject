

import streamlit as st
import pandas as pd
from pathlib import Path

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# CSV file location
DATA_PATH = BASE_DIR / "crop_details.csv"

# Check whether the file exists
if not DATA_PATH.exists():
    st.error("crop_details.csv not found!")
    st.write("Expected location:", str(DATA_PATH))
    st.stop()

# Load dataset
data = pd.read_csv(DATA_PATH)

st.success("Crop dataset loaded successfully!")

st.title("Indian Crop Information 🌾")

st.dataframe(data, use_container_width=True)
