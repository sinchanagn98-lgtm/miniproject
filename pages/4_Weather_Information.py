

import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

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
# READ OPENWEATHER API KEY
# ----------------------------------

API_KEY = ""

try:
    API_KEY = st.secrets.get(
        "OPENWEATHER_API_KEY", ""
    )

    if API_KEY:
        API_KEY = str(API_KEY).strip()

except Exception:
    API_KEY = ""

# ----------------------------------
# FETCH LIVE WEATHER
# ----------------------------------

@st.cache_data(ttl=600)
def get_live_weather(city_name, api_key):

    # Get city coordinates
    geo_url = (
        "https://api.openweathermap.org/geo/1.0/direct"
    )

    geo_response = requests.get(
        geo_url,
        params={
            "q": f"{city_name},IN",
            "limit": 1,
            "appid": api_key
        },
        timeout=20
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data:
        raise ValueError("City not found.")

    latitude = geo_data[0]["lat"]
    longitude = geo_data[0]["lon"]

    # Get current weather
    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    response = requests.get(
        weather_url,
        params={
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
            "units": "metric"
        },
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# ----------------------------------
# CURRENT LIVE WEATHER SECTION
# ----------------------------------

st.divider()
st.header("🌍 Current Live Weather")

if not API_KEY:

    st.error(
        "Weather API key not found. "
        "Add OPENWEATHER_API_KEY to Streamlit Cloud Secrets."
    )

else:

    if st.button("🔄 Refresh Live Weather"):
        get_live_weather.clear()

    try:

        data = get_live_weather(city, API_KEY)

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        rainfall = data.get("rain", {}).get("1h")

        # Weather information cards
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
            f"{wind_speed} m/s"
        )

        col4.metric(
            "🌧️ Rainfall (last hour)",
            f"{rainfall} mm"
            if rainfall is not None
            else "Not reported"
        )

        st.success(
            f"Weather in {city}: {condition.title()}"
        )

        # Last updated time
        timezone_offset = data.get("timezone", 0)

        updated_time = (
            datetime.fromtimestamp(
                data["dt"],
                timezone.utc
            )
            + timedelta(seconds=timezone_offset)
        )

        st.caption(
            "Last weather observation: "
            + updated_time.strftime(
                "%d-%m-%Y %I:%M %p"
            )
        )

    except requests.exceptions.HTTPError as e:

        if e.response is not None:

            status_code = e.response.status_code

            if status_code == 401:
                st.error(
                    "Invalid or inactive OpenWeather API key. "
                    "Check your API key and account activation."
                )

            elif status_code == 429:
                st.error(
                    "API request limit reached. "
                    "Please try again later."
                )

            else:
                st.error(
                    f"OpenWeather API error: {status_code}"
                )
                st.write(e.response.text)

        else:
            st.error(f"HTTP error: {str(e)}")

    except requests.exceptions.Timeout:
        st.error(
            "Weather service is taking too long to respond. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError as e:
        st.error(
            "Unable to connect to OpenWeather. "
            "Please check the internet connection."
        )
        st.write(str(e))

    except requests.exceptions.RequestException as e:
        st.error("Weather connection failed.")
        st.write(str(e))

    except Exception as e:
        st.error(f"Unexpected weather error: {str(e)}")


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
