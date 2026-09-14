import math
import requests

ELEVATION_API = "https://api.open-meteo.com/v1/elevation"

def get_elevations(latitude, longitude):
    offset = 0.01
    latitudes = [latitude, latitude + offset, latitude - offset, latitude, latitude]
    longitudes = [longitude, longitude, longitude, longitude + offset, longitude - offset]
    params = {"latitude": ",".join(map(str, latitudes)), "longitude": ",".join(map(str, longitudes))}

    try:
        response = requests.get(ELEVATION_API, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        elevations = data.get("elevation")
        if not elevations or len(elevations) < 5:
            return {"error": "Incomplete elevation data received."}

        return {"center": elevations[0], "north": elevations[1], "south": elevations[2], "east": elevations[3],
                "west": elevations[4]}

    except requests.RequestException as error:
        return {"error": f"Elevation API error: {error}"}
    except (KeyError, TypeError, ValueError) as error:
        return {"error": f"Invalid elevation data: {error}"}

def calculate_terrain_slope(latitude, longitude):
    elevations = get_elevations(latitude, longitude)
    if "error" in elevations:
        return elevations

    center = elevations["center"]
    north_difference = abs(elevations["north"] - center)
    south_difference = abs(elevations["south"] - center)
    east_difference = abs(elevations["east"] - center)
    west_difference = abs(elevations["west"] - center)
    maximum_difference = max(north_difference, south_difference, east_difference, west_difference)
    horizontal_distance = 1110

    slope_radians = math.atan(maximum_difference / horizontal_distance)
    slope_degrees = math.degrees(slope_radians)

    return {"center_elevation": round(center, 2), "north_elevation": round(elevations["north"], 2),
            "south_elevation": round(elevations["south"], 2), "east_elevation": round(elevations["east"], 2),
            "west_elevation": round(elevations["west"], 2), "max_elevation_difference": round(maximum_difference, 2),
            "estimated_slope": round(slope_degrees, 2)}

def get_terrain_risk(slope):
    if slope < 5:
        risk = 10
        level = "LOW"

    elif slope < 15:
        risk = 30
        level = "MODERATE"

    elif slope < 30:
        risk = 60
        level = "HIGH"

    else:
        risk = 90
        level = "VERY HIGH"

    return {"terrain_risk": risk, "terrain_level": level}

