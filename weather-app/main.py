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
    unit = input("Enter unit of temperature (C or F) >> ").strip()
    try:
        days = int(input("Enter number of days to forecast (1-10) >> ").strip())
    except ValueError:
        print("Days must be an integer between 1 and 10")
        return

    try:
        current = get_current(city, unit)
        forecast = get_forecast(city, days, unit)
        
        weather_data = {
            "current": current,
            "forecast": forecast
        }
        
        print(f"\n{get_gemini_response(weather_data)}")
    except ValueError as e:
        print(f"Input error: {e}")
    except RuntimeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()