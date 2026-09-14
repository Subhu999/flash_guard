import streamlit as st
from risk_engine import calculate_flood_risk
from weather_data import get_location_coordinates, get_weather_data
from terrain_data import calculate_terrain_slope, get_terrain_risk

st.set_page_config(
page_title="FlashGuard",
page_icon="🌊",
layout="wide"
)

st.title("🌊 FlashGuard")
st.subheader("Flash Flood Early Warning System for Hilly Regions")

st.divider()

st.header("📡 Live Environmental Monitoring")

location_name = st.text_input(
"📍 Enter Location",
placeholder="Example: Manali, India"
)

if st.button("📡 Fetch Live Environmental Data"):

    with st.spinner("Fetching real environmental data..."):

        location = get_location_coordinates(location_name)

        if "error" in location:
            st.error(location["error"])

        else:
            weather = get_weather_data(
                location["latitude"],
                location["longitude"]
            )

            terrain = calculate_terrain_slope(
                location["latitude"],
                location["longitude"]
            )

            if "error" in terrain:

                terrain_risk = None

            else:

                terrain_risk = get_terrain_risk(
                    terrain["estimated_slope"]
                )

            st.session_state["live_data"] = {
                "location": location,
                "weather": weather,
                "terrain": terrain,
                "terrain_risk": terrain_risk
            }

            if "error" in weather:
                st.error(weather["error"])

            else:
                st.success(
                    f"Live data loaded for "
                    f"{location['name']}, "
                    f"{location['country']}"
                )

if "live_data" in st.session_state:

    live_data = st.session_state["live_data"]

    location = live_data["location"]
    weather = live_data["weather"]

    st.subheader(
        f"📍 Monitoring: {location['name']}"
    )

    live_col1, live_col2, live_col3, live_col4 = st.columns(4)

    live_col1.metric(
        "🌡️ Temperature",
        f"{weather['temperature']} °C"
    )

    live_col2.metric(
        "💧 Humidity",
        f"{weather['humidity']}%"
    )

    live_col3.metric(
        "🌧️ Rainfall (24h)",
        f"{weather['rainfall_24h']} mm"
    )

    live_col4.metric(
        "🌱 Soil Moisture",
        f"{weather['soil_moisture']}%"
    )

    st.divider()

    st.subheader("⛰️ Real Terrain Analysis")

    terrain = live_data.get("terrain")
    terrain_risk = live_data.get("terrain_risk")

    if terrain and "error" not in terrain:

        terrain_col1, terrain_col2, terrain_col3 = st.columns(3)

        terrain_col1.metric(
            "⛰️ Elevation",
            f"{terrain['center_elevation']} m"
        )

        terrain_col2.metric(
            "📐 Estimated Slope",
            f"{terrain['estimated_slope']}°"
        )

        terrain_col3.metric(
            "⚠️ Terrain Risk",
            terrain_risk["terrain_level"]
        )

        st.caption(
            "Slope estimated from real elevation differences "
            "around the selected location."
        )

    else:

        st.error(
            "⛰️ Terrain data could not be retrieved."
        )

        if terrain and "error" in terrain:
            st.code(terrain["error"])

if "live_data" in st.session_state:

    weather = st.session_state["live_data"]["weather"]
    location = st.session_state["live_data"]["location"]

    st.divider()

    if st.button("🤖 Analyze Live Flood Risk"):
        terrain = st.session_state["live_data"].get("terrain")

        if terrain:

            terrain_slope = terrain["estimated_slope"]

        else:

            st.warning(
                "Real terrain slope unavailable. "
                "Flood risk analysis requires terrain data."
            )

            terrain_slope = 0

        live_result = calculate_flood_risk(
            rainfall=weather["rainfall_24h"],
            river_level=3.0,
            soil_moisture=weather["soil_moisture"],
            slope=terrain_slope
        )

        st.header("🚨 Live Flash Flood Risk Assessment")

        risk_col1, risk_col2, risk_col3 = st.columns(3)

        risk_col1.metric(
            "Risk Score",
            f"{live_result["RISK_SCORE"]}%"
        )

        risk_col2.metric(
            "Risk Level",
            live_result["RISK_LEVEL"]
        )

        risk_col3.metric(
            "Monitoring Location",
            location["name"]
        )

        if live_result["RISK_LEVEL"] == "LOW":
            st.success(live_result["ALERT"])

        elif live_result["RISK_LEVEL"] == "MODERATE":
            st.warning(live_result["ALERT"])

        elif live_result["RISK_LEVEL"] == "HIGH":
            st.warning(live_result["ALERT"])

        else:
            st.error(live_result["ALERT"])


st.divider()

st.info(
"FlashGuard combines rainfall, river level, "
"soil moisture, and terrain slope to estimate "
"flash flood risk."
)
