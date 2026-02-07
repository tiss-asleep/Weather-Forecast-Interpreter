from weather_api import get_current, get_forecast
from gemini_api import get_gemini_response

def main():
    city = input("Enter city name >> ")
    unit = input("Enter unit of temperature (C or F) >> ")
    days = int(input("Enter number of days to forecast (1-10) >> "))

    current = get_current(city, unit)
    forecast = get_forecast(city, days, unit)

    if not current or not forecast:
        print("Failed to fetch weather data")
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