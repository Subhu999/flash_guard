import requests

def get_location_coordinates(location_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location_name, "count": 1, "language": "en", "format": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get("results"): return {"error": "Location not found"}
        location = data["results"][0]

        return {"name": location.get("name"), "country": location.get("country"), "latitude": location.get("latitude"),
                "longitude": location.get("longitude"), "elevation": location.get("elevation")}

    except requests.RequestException as error:
        return {"error": f"Could not retrieve location: {error}"}

def get_weather_data(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude,
              "current": ("temperature_2m," "relative_humidity_2m," "precipitation"),
              "hourly": ("precipitation," "soil_moisture_0_to_1cm," "soil_moisture_1_to_3cm"), "past_hours": 24,
              "forecast_hours": 24, "timezone": "auto"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        precipitation_values = hourly.get("precipitation", [])

        recent_rainfall = precipitation_values[:24]
        rainfall_24h = round(sum(recent_rainfall), 2)

        soil_values = hourly.get("soil_moisture_0_to_1cm", [])
        latest_soil_value = soil_values[-1] if soil_values else 0
        soil_moisture_percent = min(round(latest_soil_value * 100, 2), 100)

        return {"temperature": current.get("temperature_2m"), "humidity": current.get("relative_humidity_2m"),
                "current_precipitation": current.get("precipitation", 0), "rainfall_24h": rainfall_24h,
                "soil_moisture": soil_moisture_percent, "latitude": data.get("latitude"),
                "longitude": data.get("longitude")}

    except requests.RequestException as error:
        return {"error": f"Could not retrieve weather data: {error}"}