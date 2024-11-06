import os
import requests

api_key = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    try:
        # Define the API endpoint and parameters
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "imperial"
        }

        # Make the request
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract desired data from the response
            city_name = data["name"]
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]

            return {
                "city": city_name,
                "temperature": temperature,
                "description": weather_description
            }
        else:
            # Handle errors, such as city not found
            print(response.text)
            return {"error": f"Error: {response.status_code}, City not found."}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


# Test the function
if __name__ == "__main__":
    city = input("Enter city name: ")
    weather = get_weather(city)
    if "error" in weather:
        print(weather["error"])
    else:
        print(f"Weather in {weather['city']}: {weather['temperature']}°F, {weather['description'].capitalize()}")


