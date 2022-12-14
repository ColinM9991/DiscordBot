import requests


class OpenMapWeatherService:
    def __init__(self, open_weather_map_url, open_weather_map_api_key):
        self.open_weather_map_url = open_weather_map_url
        self.open_weather_map_api_key = open_weather_map_api_key

    def get_weather_by_city(self, city):
        """ Gets the weather for the specified city. """
        response = requests.get(self.open_weather_map_url, params={
            'q': city,
            'appid': self.open_weather_map_api_key,
            'units': 'metric'
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
