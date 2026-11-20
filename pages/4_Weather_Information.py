

import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="Weather Information",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Information")
st.write("Live weather updates and monthly weather information for Indian cities.")

# Find project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Support both possible CSV locations
paths = [
    BASE_DIR / "dataset" / "weather_data.csv",
    BASE_DIR / "weather_data.csv"
]

DATA_PATH = next((p for p in paths if p.exists()), None)

# Load monthly CSV dataset
weather_df = None

if DATA_PATH:
    try:
        weather_df = pd.read_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Unable to read weather CSV: {e}")
else:
    st.warning("Monthly weather dataset not found. Check the dataset folder.")

# Cities
default_cities = [
    "Bengaluru", "Mysuru", "Mumbai", "Delhi",
    "Chennai", "Hyderabad", "Kolkata",
    "Pune", "Jaipur", "Thiruvananthapuram"
]

if weather_df is not None and "City" in weather_df.columns:
    cities = sorted(weather_df["City"].dropna().unique().tolist())
else:
    cities = default_cities

city = st.selectbox("Select Indian City", cities)

# Get API key securely
try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except Exception:
    API_KEY = ""

# Fetch live weather
@st.cache_data(ttl=600)
def get_live_weather(city_name, api_key):

    # First find city coordinates
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"

    geo_response = requests.get(
        geo_url,
        params={
            "q": f"{city_name},IN",
            "limit": 1,
            "appid": api_key
        },
        timeout=15
    )

    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if not geo_data:
        raise ValueError("City not found.")

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # Fetch current weather
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    response = requests.get(
        weather_url,
        params={
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# LIVE WEATHER SECTION
st.divider()
st.header("🌍 Current Live Weather")

if not API_KEY:
    st.error(
        "Weather API key not found. "
        "Add OPENWEATHER_API_KEY to Streamlit secrets."
    )

else:
    if st.button("🔄 Refresh Live Weather"):
        get_live_weather.clear()

    try:
        data = get_live_weather(city, API_KEY)

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        rainfall = data.get("rain", {}).get("1h")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Temperature",
            f"{temperature} °C"
        )

        col2.metric(
            "Humidity",
            f"{humidity}%"
        )

        col3.metric(
            "Wind Speed",
            f"{wind} m/s"
        )

        col4.metric(
            "Rainfall (last hour)",
            f"{rainfall} mm" if rainfall is not None
            else "Not reported"
        )

        st.success(
            f"Weather in {city}: {condition.title()}"
        )

        # Display last updated time
        timezone_offset = data.get("timezone", 0)

        updated_time = (
            datetime.fromtimestamp(data["dt"], timezone.utc)
            + timedelta(seconds=timezone_offset)
        )

        st.caption(
            f"Last weather observation: "
            f"{updated_time.strftime('%d-%m-%Y %I:%M %p')}"
        )

    except requests.exceptions.HTTPError as e:
        st.error(
            "Weather API request failed. Check your API key "
            "and account activation."
        )
    except requests.exceptions.RequestException:
        st.error("Unable to connect to the weather service.")
    except Exception as e:
        st.error(f"Weather error: {e}")


# MONTHLY CSV DATASET SECTION
st.divider()
st.header("📅 Monthly Weather Information")

if weather_df is not None:

    required_columns = [
        "City", "Month", "Temperature_C",
        "Humidity_Percent", "Rainfall_mm",
        "Weather", "Season"
    ]

    missing = [
        col for col in required_columns
        if col not in weather_df.columns
    ]

    if missing:
        st.error(f"Missing CSV columns: {', '.join(missing)}")

    else:
        city_data = weather_df[
            weather_df["City"].astype(str).str.lower()
            == city.lower()
        ].copy()

        if not city_data.empty:

            st.subheader(f"Monthly Weather in {city}")

            st.dataframe(
                city_data[required_columns],
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Monthly Temperature")

            chart_data = city_data.set_index("Month")[
                ["Temperature_C"]
            ]

            st.line_chart(chart_data)

            st.subheader("Monthly Rainfall")

            rainfall_chart = city_data.set_index("Month")[
                ["Rainfall_mm"]
            ]

            st.bar_chart(rainfall_chart)

        else:
            st.warning("No monthly information available for this city.")

    st.info(
        "Note: Monthly CSV values are illustrative sample data, "
        "not official historical weather records."
    )
