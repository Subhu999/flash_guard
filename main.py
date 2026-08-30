import streamlit as st
from risk_engine import calculate_flood_risk

st.set_page_config(
page_title="FlashGuard",
page_icon="🌊",
layout="wide"
)

st.title("🌊 FlashGuard")
st.subheader("Flash Flood Early Warning System for Hilly Regions")

st.divider()

st.sidebar.header("🌍 Environmental Conditions")

rainfall = st.sidebar.slider(
"🌧️ Rainfall (mm)",
min_value=0,
max_value=300,
value=100
)

river_level = st.sidebar.slider(
"💧 River Level (m)",
min_value=0.0,
max_value=10.0,
value=3.0,
step=0.1
)

soil_moisture = st.sidebar.slider(
"🌱 Soil Moisture (%)",
min_value=0,
max_value=100,
value=50
)

slope = st.sidebar.slider(
"⛰️ Terrain Slope (degrees)",
min_value=0,
max_value=60,
value=25
)

result = calculate_flood_risk(
rainfall=rainfall,
river_level=river_level,
soil_moisture=soil_moisture,
slope=slope
)

risk_score = result["RISK_SCORE"]
risk_level = result["RISK_LEVEL"]

st.header("🚨 Current Flood Risk Assessment")

col1, col2, col3 = st.columns(3)

col1.metric(
"Flood Risk Score",
f"{risk_score}%"
)

col2.metric(
"Risk Level",
risk_level
)

col3.metric(
"Status",
"Monitoring Active"
)

if risk_level == "LOW":
    st.success(f"🟢 {result['ALERT']}")
elif risk_level == "MODERATE":
    st.warning(f"🟡 {result['ALERT']}")
elif risk_level == "HIGH":
    st.warning(f"🟠 {result['ALERT']}")
else:
    st.error(f"🔴 {result['ALERT']}")

st.divider()
st.header("📊 Environmental Risk Factors")

factor_col1, factor_col2, factor_col3, factor_col4 = st.columns(4)

factor_col1.metric(
"🌧️ Rainfall Risk",
f"{result['FACTORS']['rainfall']}%"
)

factor_col2.metric(
"💧 River Risk",
f"{result['FACTORS']['river_level']}%"
)

factor_col3.metric(
"🌱 Soil Risk",
f"{result['FACTORS']['soil_moisture']}%"
)

factor_col4.metric(
"⛰️ Terrain Risk",
f"{result['FACTORS']['slope']}%"
)

st.divider()

st.info(
"FlashGuard combines rainfall, river level, "
"soil moisture, and terrain slope to estimate "
"flash flood risk."
)

st.caption("Prototype Version 1.0 | Multi-Source Risk Assessment System")