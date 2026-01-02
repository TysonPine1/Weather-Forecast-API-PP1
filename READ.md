# Weather API (FastAPI)

A RESTful API that provides:
Current weather
Tomorrow's forecast
5-day weather forecast

## Tech Stack
FastAPI
Python
OpenWeatherMap API

## Endpoints
GET /weather/current?city=Tokyo  
GET /weather/tomorrow?city=Tokyo  
GET /weather/forecast?city=Tokyo  

## Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload


#Developer : Tyson R. Pine