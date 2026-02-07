import requests

API_KEY = "7eddd10bc7244779ae104325260702"
CURRENT = "https://api.weatherapi.com/v1/current.json"
FORECAST = "https://api.weatherapi.com/v1/forecast.json"

def get_response(city_name):
    params = {
        "key": API_KEY,
        "q": city_name
    }

    return requests.get(CURRENT, params=params)

def get_current(response):
    current = response.json()["current"]

    print(f"Temperature: {current['temp_c']}C")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind: {current['wind_kph']} km/h")

def main():
    city_name = input("Enter city name >> ")

    response = get_response(city_name)

    if response.status_code != 200:
        print("Error fetching weather data")
        exit()

    get_current(response)

if __name__ == "__main__":
    main()