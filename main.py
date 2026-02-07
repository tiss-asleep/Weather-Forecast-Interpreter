import weather_api

def main():
    city_name = input("Enter city name >> ")

    weather_api.get_current(city_name)

    weather_api.get_forecast(city_name)

if __name__ == "__main__":
    main()