import datetime
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import City

# Create your views here.

# Define your API key and base URLs for fetching weather data

# def get_api_key():
#     with open('./.env', 'r') as f:
#         return f.read().strip()

# CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
# FORECAST_URL = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

def home_view(request):
    return render(request, "home.html")

def compare_view(request):
    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST['city2']

        weather_city1 = get_weather_data(city1)
        weather_city2 = get_weather_data(city2)

        return render(request, "compare.html", {
            "city1": city1,
            "weather_city1": weather_city1,
            "city2": city2,
            "weather_city2": weather_city2,
        })
    return render(request, "compare.html")

def save_view(request):
    from .models import City  # This assumes a City model is defined

    if request.method == 'POST':
        city_name = request.POST['city']
        city, created = City.objects.get_or_create(name=city_name)
        if created:
            city.save()
    saved_cities = City.objects.all()
    saved_weather = {city.name: get_weather_data(city.name) for city in saved_cities}

    return render(request, "save.html", {"saved_weather": saved_weather})

def search_view(request):
    if request.method == 'POST':
        city = request.POST['city']
        weather_data = get_weather_data(city)
        return render(request, "search.html", {
            "city": city,
            "weather_data": weather_data,
        })
    return render(request, "search.html")

def get_weather_data(city_name):
    API_KEY = open("./.env", "r").read().strip()  # Gets the API key from the file

    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'

    current_weather_response = requests.get(current_weather_url)
    current_weather = current_weather_response.json()

    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    weather_data = {
        'temperature': current_weather['main']['temp'],
        'humidity': current_weather['main']['humidity'],
        'wind_speed': current_weather['wind']['speed'],
        'description': current_weather['weather'][0]['description'],
        'forecast': []  # 5-days of data
    }

    # Process the forecast data (next 5 days)
    for day in forecast_data['list'][::8]:  # Get one forecast per day
        weather_data['forecast'].append({
            'date': day['dt_txt'],
            'temp': day['main']['temp'],
            'humidity': day['main']['humidity'],
            'wind_speed': day['wind']['speed'],
            'description': day['weather'][0]['description'],
        })

    return weather_data


