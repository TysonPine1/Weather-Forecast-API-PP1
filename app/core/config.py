import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Weather API"
VERSION = "1.0.0"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

if not WEATHER_API_KEY:
    raise RuntimeError("WEATHER_API_KEY is not set in .env")

