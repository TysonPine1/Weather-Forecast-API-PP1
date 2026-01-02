import time
import httpx
from fastapi import HTTPException
from app.core.config import WEATHER_API_KEY, WEATHER_BASE_URL, FORECAST_BASE_URL

cache = {}
CACHE_TTL = 600

async def fetch_forecast(city: str):
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(FORECAST_BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Forecast API error: {response.text}"
        )

    data = response.json()

    if "list" not in data:
        raise HTTPException(
            status_code=502,
            detail="Forecast data unavailable (API limit or invalid response)"
        )

    return data


async def fetch_weather(city: str):
    city = city.lower()
    now = time.time()

    if city in cache:
        cached_data, timestamp = cache[city]
        if now - timestamp < CACHE_TTL:
            return cached_data
    
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(WEATHER_BASE_URL, params=params)

    if response.status_code == 401:
        raise HTTPException(status_code=500, detail="Weather API key invalid")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="External weather service error"
    )

    data = response.json()

    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

    cache[city] = (result, time.time())

    return result
