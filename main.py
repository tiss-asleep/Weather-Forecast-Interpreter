import requests

API_KEY = "7eddd10bc7244779ae104325260702"

def get_response(city_name):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city_name
    }

    return requests.get(url, params=params)

def get_current(response):
    current = response.json()["current"]

    print(f"Temperature: {current["temp_c"]}C")
    print(f"Humidity: {current["humidity"]}%")
    print(f"Wind: {current["wind_kph"]}km/h")

def main():
    # city_name = input("Enter name of city to forecast >> ")

    response = get_response("Rochester")

    if (response.status_code != 200):
        print("Error fetching weather data")
        exit()

    print("\n", response.text, "\n")

    get_current(response)

if __name__ == "__main__":
    main()