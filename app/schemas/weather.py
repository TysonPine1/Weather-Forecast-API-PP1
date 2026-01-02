from pydantic import BaseModel
from typing import List

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str

class TomorrowWeather(BaseModel):
    date: str
    temp_day: float
    temp_night: float
    condition: str

class DailyForecast(BaseModel):
    date: str
    temp_day: float
    temp_night: float
    condition: str

class WeeklyForecast(BaseModel):
    city: str
    forecast: List[DailyForecast]

class WeatherSummary(BaseModel): 
    city: str 
    temp_celsius: float 
    condition: str

    