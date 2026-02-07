"""
@file: main.py
@author: Jambaldorj Munkhsoyol

This is the main entry point of the Weather Forecast Interpreter application.
It prompts the user for input, fetches current weather and forecast data using the
weather API, and generates a user-friendly summary using the Gemini API. The
application handles errors gracefully and provides feedback to the user in
case of issues with fetching data or generating summaries.
"""

from weather_api import get_current, get_forecast
from gemini_api import get_gemini_response

"""
The main function of the application. It prompts the user for city name, unit of
temperature,and number of days to forecast. It then fetches the current weather and forecast data,
combines them into a single dictionary, and generates a user-friendly summary using 
Gemini API. The function also handles errors gracefully and provides feedback to the user.
"""
def main():
    city = input("Enter city name >> ")
    unit = input("Enter unit of temperature (C or F) >> ")
    days = int(input("Enter number of days to forecast (1-10) >> "))

    current = get_current(city, unit)
    forecast = get_forecast(city, days, unit)

    if not current or not forecast:
        print("Error fetching weather data")
        return
    
    weather_data = {
        "current": current,
        "forecast": forecast
    }

    try:
        print(f"\n{get_gemini_response(weather_data)}")
    except Exception as e:
        print(f"Error fetching AI summary: {e}")

if __name__ == "__main__":
    main()