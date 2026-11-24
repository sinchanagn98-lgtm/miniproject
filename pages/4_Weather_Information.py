


import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Weather Information",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Information")

st.write(
    "Live weather updates and monthly weather "
    "information for Indian cities."
)

# ----------------------------------
# FIND PROJECT FOLDER
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

paths = [
    BASE_DIR / "dataset" / "weather_data.csv",
    BASE_DIR / "weather_data.csv"
]

DATA_PATH = next(
    (path for path in paths if path.exists()),
    None
)

# ----------------------------------
# LOAD MONTHLY WEATHER CSV
# ----------------------------------

weather_df = None

if DATA_PATH is not None:
    try:
        weather_df = pd.read_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Unable to read weather CSV: {e}")
else:
    st.warning(
        "Monthly weather dataset not found. "
        "Please check your dataset folder."
    )

# ----------------------------------
# CITY SELECTION
# ----------------------------------

default_cities = [
    "Bengaluru",
    "Mysuru",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Jaipur",
    "Thiruvananthapuram"
]

if weather_df is not None and "City" in weather_df.columns:
    cities = sorted(
        weather_df["City"].dropna().astype(str).unique().tolist()
    )
else:
    cities = default_cities

city = st.selectbox(
    "Select Indian City",
    cities
)

# ----------------------------------
# WEATHER CONDITION DESCRIPTION
# ----------------------------------

def get_weather_description(code):

    descriptions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Freezing Drizzle",
        57: "Heavy Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Heavy Thunderstorm with Hail"
    }

    return descriptions.get(code, "Unknown Weather")


# ----------------------------------
# FETCH LIVE WEATHER USING OPEN-METEO
# ----------------------------------

@st.cache_data(ttl=600)
def get_live_weather(city_name):

    # Find city coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={
            "name": city_name,
            "count": 10,
            "language": "en",
            "format": "json"
        },
        timeout=20
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    results = geo_data.get("results", [])

    # Prefer the matching city in India
    indian_results = [
        item for item in results
        if item.get("country_code") == "IN"
    ]

    if not indian_results:
        raise ValueError(
            f"Could not find {city_name} in India."
        )

    location = indian_results[0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Fetch current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "rain,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto"
        },
        timeout=20
    )

    weather_response.raise_for_status()

    return weather_response.json()


# ----------------------------------
# CURRENT LIVE WEATHER SECTION
# ----------------------------------

st.divider()
st.header("🌍 Current Live Weather")

if st.button("🔄 Refresh Live Weather"):
    get_live_weather.clear()

try:

    data = get_live_weather(city)

    current = data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    rainfall = current["precipitation"]
    wind_speed = current["wind_speed_10m"]
    weather_code = current["weather_code"]

    condition = get_weather_description(weather_code)

    # Weather cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡️ Temperature",
        f"{temperature} °C"
    )

    col2.metric(
        "💧 Humidity",
        f"{humidity}%"
    )

    col3.metric(
        "💨 Wind Speed",
        f"{wind_speed} km/h"
    )

    col4.metric(
        "🌧️ Precipitation",
        f"{rainfall} mm"
    )

    st.success(
        f"Weather in {city}: {condition}"
    )

    st.caption(
        f"Last updated: {current['time']}"
    )

except requests.exceptions.Timeout:

    st.error(
        "Weather service is taking too long. "
        "Please try again."
    )

except requests.exceptions.RequestException as e:

    st.error(
        "Unable to connect to the weather service."
    )
    st.write(str(e))

except Exception as e:

    st.error(f"Weather error: {e}")


# ----------------------------------
# MONTHLY WEATHER INFORMATION
# ----------------------------------

st.divider()
st.header("📅 Monthly Weather Information")

if weather_df is not None:

    required_columns = [
        "City",
        "Month",
        "Temperature_C",
        "Humidity_Percent",
        "Rainfall_mm",
        "Weather",
        "Season"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in weather_df.columns
    ]

    if missing_columns:

        st.error(
            "Missing CSV columns: "
            + ", ".join(missing_columns)
        )

    else:

        city_data = weather_df[
            weather_df["City"].astype(str).str.lower()
            == city.lower()
        ].copy()

        if not city_data.empty:

            st.subheader(
                f"Monthly Weather in {city}"
            )

            st.dataframe(
                city_data[required_columns],
                use_container_width=True,
                hide_index=True
            )

            # Temperature chart
            st.subheader("📈 Monthly Temperature")

            temperature_chart = city_data.set_index(
                "Month"
            )[["Temperature_C"]]

            st.line_chart(temperature_chart)

            # Rainfall chart
            st.subheader("🌧️ Monthly Rainfall")

            rainfall_chart = city_data.set_index(
                "Month"
            )[["Rainfall_mm"]]

            st.bar_chart(rainfall_chart)

        else:

            st.warning(
                f"No monthly weather information available for {city}."
            )
