import datetime
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import City

# Create your views here.

# Define your API key and base URLs for fetching weather data
def get_api_key():
    with open('./API_KEY', 'r') as f:
        return f.read().strip()

# CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
# FORECAST_URL = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'




