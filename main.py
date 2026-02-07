import requests

API_KEY = "7eddd10bc7244779ae104325260702"

def get_response(city_name):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city_name
    }

    return requests.get(url, params=params)

def parse_json(response):
    data = response.json()

    current = data["current"]

    temp = current["temp_c"]
    humidity = current["humidity"]
    wind = current["wind_kph"]

    print(f"Temperature: {temp}C")
    print(f"Humidity: {humidity}%")
    print(f"Wind: {wind}km/h")

def main():
    city_name = input("Enter name of city to forecast >> ")

    response = get_response(city_name)

    if (response.status_code != 200):
        print("Error fetching weather data")
        exit()

    print(response.text)

    parse_json(response)

if __name__ == "__main__":
    main()