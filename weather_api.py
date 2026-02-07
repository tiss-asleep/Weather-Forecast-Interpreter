import os
import requests

API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise RuntimeError("WEATHER_API_KEY is not set")

CURRENT_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"

def get_current(city_name, unit="C"):
    params = {
        "key": API_KEY,
        "q": city_name
    }

    try:
        response = requests.get(CURRENT_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather data: {e}")
        return None
    
    current = response.json()["current"]

    if unit == "C":
        temp = current["temp_c"]
    elif unit == "F":
        temp = current["temp_f"]
    else:
        print("Invalid weather unit selection")
        return None

    return {
        "temperature": temp,
        "humidity": current["humidity"],
        "wind_kph": current["wind_kph"],
        "condition": current["condition"]["text"]
    }

def get_forecast(city_name, days=3, unit="C"):
    params = {
        "key": API_KEY,
        "q": city_name,
        "days": days
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None

    forecast_days = response.json()["forecast"]["forecastday"]

    result = []

    for day in forecast_days:
        day_info = day["day"]

        if unit == "C":
            mintemp = day_info["mintemp_c"]
            maxtemp = day_info["maxtemp_c"]
        elif unit == "F":
            mintemp = day_info["mintemp_f"]
            maxtemp = day_info["maxtemp_f"]
        else:
            print("Invalid weather unit selection")
            return None

        result.append({
            "date": day["date"],
            "min_temp": mintemp,
            "max_temp": maxtemp,
            "condition": day_info["condition"]["text"],
            "chance_of_rain": day_info.get("daily_chance_of_rain", 0)
        })

    return result