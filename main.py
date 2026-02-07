"""
@file: main.py
@author: Jambaldorj Munkhsoyol
This is the main entry point for the Weather Forecast Interpreter application.
It prompts the user for input, fetches weather data using the Weather API, generates
a summary using the Gemini API, and displays the results. The code is structured to
handle errors gracefully and provide informative messages to the user.
"""

from weather_api import get_current, get_forecast
from gemini_api import get_gemini_response

"""
The main function prompts the user for a city name, unit of temperature, and number of days to forecast.
It validates the input, fetches current weather and forecast data, generates a summary using the Gemini API,
and prints the summary. If any errors occur during the process, it catches the exceptions and prints an error message.
"""
def main():
    city = input("Enter city name >> ").strip()
    unit = input("Enter unit of temperature (C or F) >> ").upper().strip()
    try:
        days = int(input("Enter number of days to forecast (1-10) >> "))
    except ValueError:
        print("Error: Days must be an integer")
        return
    
    if not city:
        print("Error: City is required")
        return
    if unit not in ("C", "F"):
        print("Error: Unit must be C or F")
        return
    if not (1 <= days <= 10):
        print("Error: Days must be between 1 and 10")
        return

    try:
        current = get_current(city, unit)
        forecast = get_forecast(city, days, unit)
        
        weather_data = {
            "current": current,
            "forecast": forecast
        }
        
        print(f"\n{get_gemini_response(weather_data)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()