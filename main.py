import requests

API_KEY = "7eddd10bc7244779ae104325260702"

def get_city_name():
    return input("Enter name of city to forecast >> ")

def main():
    city_name = get_city_name()

    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city_name
    }

    response = requests.get(url, params=params)

    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()