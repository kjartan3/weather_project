from django.test import TestCase, Client
from unittest.mock import patch
from .models import City
from weather_app.views import get_weather_data
from datetime import datetime

# Create your tests here.

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_compare_view(self):
        response = self.client.get('/compare/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compare.html')
        
    def test_save_view(self):
        response = self.client.get('/save/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'save.html')

    def test_handle_save_city(self):
        response = self.client.post('/save/city/', {'city': 'Berlin'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "saved")
        self.assertEqual(response.json()["city"], "Berlin")

        response_repeat = self.client.post('/save/city/', {'city': 'Berlin'})
        self.assertEqual(response_repeat.status_code, 200)
        self.assertEqual(response_repeat.json()["status"], "exists")

    def test_handle_delete_city(self):
        City.objects.create(name="Paris")

        response = self.client.post('/delete/city/', {'city': 'Paris'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "deleted")

        response_not_found = self.client.post('/delete/city/', {'city': 'NoCity'})
        self.assertEqual(response_not_found.status_code, 200)
        self.assertEqual(response_not_found.json()["status"], "error")

class WeatherFunctionalityTests(TestCase):
    @patch('weather_app.views.requests.get')  # Mocking the requests.get call
    def test_get_weather_data(self, mock_requests_get):
        mock_current_weather = {
            'main': {'temp': 22, 'humidity': 50},
            'wind': {'speed': 4},
            'weather': [{'description': 'clear sky'}]
        }

        mock_forecast = {
            'list': [
                {'main': {'temp': 23, 'humidity': 55}, 'wind': {'speed': 3}, 'weather': [{'description': 'partly cloudy'}]},
                {'main': {'temp': 24, 'humidity': 60}, 'wind': {'speed': 2}, 'weather': [{'description': 'cloudy'}]},
                {'main': {'temp': 22, 'humidity': 65}, 'wind': {'speed': 4}, 'weather': [{'description': 'rain'}]},
                {'main': {'temp': 20, 'humidity': 50}, 'wind': {'speed': 5}, 'weather': [{'description': 'clear sky'}]},
                {'main': {'temp': 19, 'humidity': 70}, 'wind': {'speed': 3}, 'weather': [{'description': 'sunny'}]}
            ]
        }

        mock_requests_get.side_effect = [
            MockResponse(mock_current_weather, 200),  
            MockResponse(mock_forecast, 200)      
        ]

        weather_data = get_weather_data("Berlin")

        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data['temperature'], 22)
        self.assertEqual(weather_data['humidity'], 50)
        self.assertEqual(weather_data['wind_speed'], 4)
        self.assertEqual(weather_data['description'], 'clear sky')

# Helper class to mock the requests.Response object
class MockResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data