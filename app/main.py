from fastapi import FastAPI, Query, HTTPException
from app.schemas.weather import WeatherResponse, WeatherSummary, TomorrowWeather, WeeklyForecast
from app.services.weather_service import fetch_weather, fetch_forecast
from app.core.config import APP_NAME, VERSION
import re
from datetime import datetime
from fastapi.responses import RedirectResponse



app = FastAPI(
    title = "Weather Forecasting API",
    description="API to show weather info based on city and location. Designation WP-1A",
    version  = "1.0",
    contact={
        "name": "Tyson R. Pine",
        "email": "kaungthawmaung91@gmail.com"
    }
) 

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/weather", response_model=WeatherResponse)
async def get_weather(
    city: str = Query(
        ..., 
        min_length=2,
        max_length=50,
        description="City name (eg: London, New York, etc.)"
    )
):
    if not re.match(r"^[a-zA-Z\s\-]+$", city):
        raise HTTPException(
            status_code=400,
            detail="City name must contain only letters and spaces"
        )

    return await fetch_weather(city)

@app.get("/weather/tomorrow", response_model=TomorrowWeather)
async def tomorrow_weather(city: str):
    data = await fetch_forecast(city)
    tomorrow = data["list"][8]

    return {
        "date": datetime.fromtimestamp(tomorrow["dt"]).strftime("%Y-%m-%d"),
        "temp_day": tomorrow["main"]["temp"],
        "temp_night": tomorrow["main"]["temp_min"],
        "condition": tomorrow["weather"][0]["description"]
    }

@app.get("/weather/forecast", response_model=WeeklyForecast)
async def weekly_weather(city: str):
    data = await fetch_forecast(city)

    forecast = []
    for i in range(0, len(data["list"]), 8):
        day = data["list"][i]
        forecast.append({
            "date": datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d"),
            "temp_day": day["main"]["temp"],
            "temp_night": day["main"]["temp_min"],
            "condition": day["weather"][0]["description"]
        })

    return {
        "city": city,
        "forecast": forecast
    }


@app.get("/weather/summary", response_model=WeatherSummary)
async def weather_summary(city: str):
    data = await fetch_weather(city)

    return {
        "city": data["city"],
        "temp_celsius": data["temperature"],
        "condition": data["description"]
    }

@app.get("/health")
def health_check():
    
    return {
        "status": "ok",
        "service": "weather-api"
    }

