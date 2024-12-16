from datetime import datetime, timedelta
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
    saved_cities = City.objects.all()
    saved_weather = {city.name: get_weather_data(city.name) for city in saved_cities}
    return render(request, "save.html", {"saved_weather": saved_weather})

def handle_save_city(request):
    """Handle saving a new city via AJAX."""
    if request.method == 'POST':
        city_name = request.POST.get('city')
        city, created = City.objects.get_or_create(name=city_name)
        if created:
            city.save()
            weather_data = get_weather_data(city_name)
            return JsonResponse({"status": "saved", "city": city_name, "weather": weather_data})
        else:
            return JsonResponse({"status": "exists", "city": city_name})
        
def handle_delete_city(request):
    """Handle deleting a saved city via AJAX."""
    if request.method == 'POST':
        city_name = request.POST.get('city')
        try:
            city = City.objects.get(name=city_name)
            city.delete()
            return JsonResponse({"status": "deleted", "city": city_name})
        except City.DoesNotExist:
            return JsonResponse({"status": "error", "message": "City does not exist"})

def search_view(request):
    if request.method == 'POST':
        city = request.POST['city']
        weather_data = get_weather_data(city)
        if weather_data is None:
            return render(request, "search.html", {
                "error": "City not found. Please try again."
            })
        return render(request, "search.html", {
            "city": city,
            "weather_data": weather_data,
        })
    return render(request, "search.html")

def day_format(forecast_data):
    forecast = []

    today = datetime.now().date()

    for index, day in enumerate(forecast_data['list'][::8][:5]):
        forecast_date = today + timedelta(days=index + 1)

        forecast.append({
            'day': forecast_date.strftime('%A'),
            'temp': day['main']['temp'],
            'humidity': day['main']['humidity'],
            'wind_speed': day['wind']['speed'],
            'description': day['weather'][0]['description'],
        })
    return forecast

def get_weather_data(city_name):
   
    API_KEY = open("./.env", "r").read().strip() 

    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'

    # fetch current weather data
    current_weather_response = requests.get(current_weather_url)
    if current_weather_response.status_code != 200:
        return None 

    current_weather = current_weather_response.json()
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code != 200:
        return None

    forecast_data = forecast_response.json()

    weather_data = {
        'temperature': current_weather['main']['temp'],
        'humidity': current_weather['main']['humidity'],
        'wind_speed': current_weather['wind']['speed'],
        'description': current_weather['weather'][0]['description'],
        'forecast': day_format(forecast_data)  # extract and format forecast
    }

    return weather_data



