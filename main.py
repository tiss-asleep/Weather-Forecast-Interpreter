import requests

API_KEY = "7eddd10bc7244779ae104325260702"
CURRENT_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"

def get_response(city_name):
    params = {
        "key": API_KEY,
        "q": city_name
    }

    return requests.get(CURRENT_URL, params=params)

def get_current(response):
    current = response.json()["current"]

    print(f"Temperature: {current['temp_c']}C")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind: {current['wind_kph']} km/h")

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
        date = day["date"]
        max_temp = day["day"]["maxtemp_c"]
        min_temp = day["day"]["mintemp_c"]
        condition = day["day"]["condition"]["text"]
        rain_chance = day["day"]["daily_chance_of_rain"]

        print(f"\nDate: {date}")
        print(f"Min: {min_temp}C, Max: {max_temp}C")
        print(f"Condition: {condition}, Chance of rain: {rain_chance}%")

def main():
    city_name = input("Enter city name >> ")

    response = get_response(city_name)

    if response.status_code != 200:
        print("Error fetching weather data")
        exit()

    get_current(response)

if __name__ == "__main__":
    main()