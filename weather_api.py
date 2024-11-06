import os
import requests
from datetime import datetime

# Get API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Base URL for OpenWeatherMap API
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def fetch_weather_data(endpoint, params):
    """Generic function to fetch data from OpenWeatherMap API."""
    try:
        url = BASE_URL + endpoint
        params["appid"] = API_KEY

        response = requests.get(url, params=params)

        # Handle HTTP response status
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}

    except Exception as e:
        return {"error": f"An exception occurred: {str(e)}"}

def get_current_weather(city, unit="imperial"):
    """Fetch current weather data for a given city, with specified units."""
    params = {
        "q": city,
        "units": unit
    }
    data = fetch_weather_data("weather", params)

    if "error" not in data:
        return parse_weather_data(data)
    else:
        return data

def parse_weather_data(data):
    """Parse and return structured weather data."""
    try:
        city_name = data["name"]
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        timestamp = datetime.fromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')

        return {
            "city": city_name,
            "temperature": temperature,
            "feels_like": feels_like,
            "description": weather_description,
            "humidity": humidity,
            "timestamp": timestamp
        }
    except KeyError as e:
        return {"error": f"Error parsing data: {str(e)}"}

# Example usage
if __name__ == "__main__":
    city = input("Enter city name: ")
    weather = get_current_weather(city)
    if "error" in weather:
        print(weather["error"])
    else:
        print(
            f"Weather in {weather['city']}:\n"
            f"Temperature: {weather['temperature']}°F (Feels like {weather['feels_like']}°F)\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Condition: {weather['description'].capitalize()}\n"
            f"Time: {weather['timestamp']}"
        )
