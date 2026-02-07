import requests

API_KEY = "7eddd10bc7244779ae104325260702"
CURRENT_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"

def get_current(city_name):
    params = {
        "key": API_KEY,
        "q": city_name
    }

    response = requests.get(CURRENT_URL, params=params)
    if response.status_code != 200:
        print("Error fetching current weather data")
        return
    
    current = response.json()["current"]

    print(f"\nCurrent temperature: {current['temp_c']}C")
    print(f"Current humidity: {current['humidity']}%")
    print(f"Current wind speeds: {current['wind_kph']} km/h")

def get_forecast(city_name, days=3):
    params = {
        "key": API_KEY,
        "q": city_name,
        "days": days
    }

    response = requests.get(FORECAST_URL, params=params)
    if response.status_code != 200:
        print("Error fetching forecast data")
        return

    forecast_days = response.json()["forecast"]["forecastday"]

    for day in forecast_days:
        print(f"\nForecasted date: {day['date']}")
        print(f"Minimum temperature: {day['day']['mintemp_c']}C")
        print(f"Maximum temperature: {day['day']['maxtemp_c']}C")
        print(f"Condition: {day['day']['condition']['text']}, Chance of rain: {day['day']['daily_chance_of_rain']}%")

def main():
    city_name = input("Enter city name >> ")

    get_current(city_name)

    get_forecast(city_name)

if __name__ == "__main__":
    main()