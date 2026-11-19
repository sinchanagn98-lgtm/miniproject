
import streamlit as st
import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WEATHER_PATH = ROOT / "dataset" / "weather_data.csv"

st.title("🌦️ Weather Information")

st.write(
    "View weather observations for agricultural planning."
)

if WEATHER_PATH.exists():

    weather = pd.read_csv(WEATHER_PATH)

    if weather.empty:
        st.info("No weather observations have been added.")
    else:

        st.subheader("Weather Records")

        if "location" in weather.columns:

            locations = [
                "All Locations"
            ] + sorted(
                weather["location"].dropna().unique().tolist()
            )

            selected = st.selectbox(
                "Select Location",
                locations
            )

            if selected != "All Locations":
                weather = weather[
                    weather["location"] == selected
                ]

        st.dataframe(
            weather,
            use_container_width=True
        )

        if not weather.empty:

            col1, col2, col3 = st.columns(3)

            if "temperature" in weather.columns:
                col1.metric(
                    "Average Temperature",
                    f"{weather['temperature'].mean():.1f} °C"
                )

            if "humidity" in weather.columns:
                col2.metric(
                    "Average Humidity",
                    f"{weather['humidity'].mean():.1f}%"
                )

            if "rainfall" in weather.columns:
                col3.metric(
                    "Total Recorded Rainfall",
                    f"{weather['rainfall'].sum():.1f} mm"
                )

else:
    st.warning("Weather dataset not found.")

