def calculate_flood_risk(rainfall,river_level,soil_moisture,slope):
    rainfall_score=min((rainfall / 300) * 100, 100)
    river_score=min((river_level / 10) * 100, 100)
    soil_score=max(0, min(soil_moisture, 100))
    slope_score=min((slope / 60) * 100, 100)

    risk_score=(rainfall_score*0.35 + river_score*0.30 + soil_score*0.20 + slope_score*0.10)
    risk_score=round(risk_score,2)

    if risk_score<=30:
        risk_level="LOW"
        alert="Conditions are currently safe"
    elif risk_score<=55:
        risk_level="MODERATE"
        alert="Carefully monitor weather and water conditions around your area"
    elif risk_score<=75:
        risk_level="HIGH"
        alert="High flood risk detected. Prepare for possible evacuation"
    else:
        risk_level="CRITICAL"
        alert="CRITICAL FLOOD RISK DETECTED. IMMEDIATE EVACUATION REQUIRED"

    return {
        "RISK_SCORE": risk_score,
        "RISK_LEVEL": risk_level,
        "ALERT": alert,
        "FACTORS": {"rainfall": round(rainfall_score, 2), "river_level": round(river_score, 2),
                    "soil_moisture": round(soil_score, 2), "slope": round(slope_score, 2),
                    },
    }