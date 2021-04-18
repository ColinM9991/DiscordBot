import requests

from helpers.weatherservice import WeatherService


class OpenMapWeatherService(WeatherService):
    def __init__(self, openweathermapurl, openweathermapapikey):
        self.openweathermapurl = openweathermapurl
        self.openweathermapapikey = openweathermapapikey

    def get_weather_by_city(self, city):
        """ Gets the weather for the specified city. """
        response = requests.get(self.openweathermapurl, params={
            'q': city,
            'appid': self.openweathermapapikey
        })

        if response.status_code == 404:
            raise CityNotFoundError
        elif response.status_code == 200:
            return response.json()
        else:
            raise OpenWeatherMapError


class OpenWeatherMapError(Exception):
    """ Raised when an error occurs during the Open Weather Map API request """
    pass


class CityNotFoundError(OpenWeatherMapError):
    """ Raised when a requested city was not found by the Open Weather Map API """
    pass
