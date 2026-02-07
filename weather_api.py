"""
@file: weather_api.py
@author: Jambaldorj Munkhsoyol

This module provides functions to interact with the Weather API to fetch current weather
and forecast data. It retrieves the API key from environment variables, defines functions
to fetch current weather and forecast data for a given city, and handles errors gracefully
by raising exceptions with informative messages.
"""

import os
import requests

CURRENT_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"

"""
Retrieves the weather API key from environment variables.
@return: The weather API key as a string.
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
@raises RuntimeError: If there is an error fetching the data or if no data is found.
"""
def get_current(city_name, unit="C"):
    if unit not in ("C", "F"):
        raise ValueError("Unit must be 'C' or 'F'")

    params = {
        "key": _get_api_key(),
        "q": city_name
    }

    try:
        response = requests.get(CURRENT_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching current weather data: {e}")
    
    current = response.json()["current"]
    if not current:
        raise RuntimeError("No current weather data found")

    return {
        "temperature": current["temp_c" if unit == "C" else "temp_f"],
        "humidity": current["humidity"],
        "wind_kph": current["wind_kph"],
        "condition": current["condition"]["text"]
    }

"""
Fetches weather forecast data for a given city, number of days, and unit of temperature.
@param city_name: The name of the city to fetch forecast for.
@param days: The number of days to forecast (1-10).
@param unit: The unit of temperature ("C" for Celsius, "F" for Fahrenheit).
@return: A list of dictionaries containing forecast data for each day.
@raises RuntimeError: If there is an error fetching the data, if no data is found, or if parameters are invalid.
"""
def get_forecast(city_name, days=3, unit="C"):
    if not 1 <= days <= 10:
        raise ValueError("Days must be between 1 and 10")
    if unit not in ("C", "F"):
        raise ValueError("Unit must be 'C' or 'F'")

    params = {
        "key": _get_api_key(),
        "q": city_name,
        "days": days
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching forecast data: {e}")

    forecast_days = response.json()["forecast"]["forecastday"]
    if not forecast_days:
        raise RuntimeError("No forecast data found")

    result = []

    for day in forecast_days:
        day_info = day["day"]

        result.append({
            "date": day["date"],
            "min_temp": day_info["mintemp_c" if unit == "C" else "mintemp_f"],
            "max_temp": day_info["maxtemp_c" if unit == "C" else "maxtemp_f"],
            "condition": day_info["condition"]["text"],
            "chance_of_rain": day_info.get("daily_chance_of_rain", 0)
        })

    return result