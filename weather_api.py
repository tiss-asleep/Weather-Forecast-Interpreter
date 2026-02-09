"""
@file: weather_api.py
@author: Jambaldorj Munkhsoyol
This module provides functionality to interact with the Weather API to fetch current weather
conditions and forecasts for a given city. It retrieves the API key from environment variables,
makes HTTP requests to the Weather API, and returns structured data that can be used by other parts of the application.
The module includes error handling to manage issues such as invalid input, network errors, and API response errors.
"""

import os
import requests

CURRENT_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"

"""
Retrieves the Weather API key from environment variables.
@return: The Weather API key as a string.
@raises RuntimeError: If the WEATHER_API_KEY environment variable is not set.
"""
def _get_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("WEATHER_API_KEY is not set")
    return api_key

"""
Fetches current weather data for a given city and unit of temperature.
@param city_name: The name of the city to fetch weather for.
@param unit: The unit of temperature ("C" for Celsius, "F" for Fahrenheit).
@return: A dictionary containing current weather data.
@raises ValueError: If the input parameters are invalid.
@raises RuntimeError: If there is an error fetching the data or if no data is found
"""
def get_current(city_name, unit):
    if not city_name:
        raise ValueError("City name cannot be empty")
    if unit.upper() not in ("C", "F"):
        raise ValueError("Unit must be C or F")

    params = {
        "key": _get_api_key(),
        "q": city_name
    }
    
    try:
        response = requests.get(CURRENT_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching current weather data: {e}")
    
    current = data["current"]
    if not current:
        raise RuntimeError("No current weather data found")
    
    return {
        "temp": current[f"temp_{unit.lower()}"],
        "feels_like": current[f"feelslike_{unit.lower()}"],
        "condition": current["condition"]["text"],
        "wind_kph": current["wind_kph"],
        "humidity": current["humidity"]
    }

"""
Fetches weather forecast data for a given city, number of days, and unit of temperature.
@param city_name: The name of the city to fetch forecast for.
@param days: The number of days to forecast (1-10).
@param unit: The unit of temperature ("C" for Celsius, "F" for Fahrenheit).
@return: A list of dictionaries containing forecast data for each day.
@raises ValueError: If the input parameters are invalid.
@raises RuntimeError: If there is an error fetching the data or if no data is found
"""
def get_forecast(city_name, days, unit):
    if not city_name:
        raise ValueError("City name cannot be empty")
    if not (1 <= days <= 10):
        raise ValueError("Days must be between 1 and 10")
    if unit.upper() not in ("C", "F"):
        raise ValueError("Unit must be C or F")

    params = {
        "key": _get_api_key(),
        "q": city_name,
        "days": days
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching forecast data: {e}")

    forecast_days = data["forecast"]["forecastday"]
    if not forecast_days:
        raise RuntimeError("No forecast data found")

    result = []

    for day in forecast_days:
        day_info = day["day"]

        result.append({
            "date": day["date"],
            "avg_temp": day_info[f"avgtemp_{unit.lower()}"],
            "min_temp": day_info[f"mintemp_{unit.lower()}"],
            "max_temp": day_info[f"maxtemp_{unit.lower()}"],
            "condition": day_info["condition"]["text"],
            "chance_of_rain": day_info.get("daily_chance_of_rain", 0)
        })

    return result