import datetime
import requests
import models.units as units
import models.weatherresponse


class OpenMapWeatherService:
    def __init__(self, open_weather_map_url, open_weather_map_api_key):
        self.open_weather_map_url = open_weather_map_url
        self.open_weather_map_api_key = open_weather_map_api_key

    def get_weather_by_city(self, city) -> models.weatherresponse.WeatherResponse:
        """ Gets the weather for the specified city. """
        response = requests.get(self.open_weather_map_url, params={
            'q': city,
            'appid': self.open_weather_map_api_key,
            'units': 'metric'
        })

        if response.status_code == 404:
            raise CityNotFoundError
        elif response.status_code == 200:
            return self.create_response(response.json())
        else:
            raise OpenWeatherMapError

    @staticmethod
    def create_response(weather_api_response):
        return models.weatherresponse.WeatherResponse(
            weather_api_response['weather'][0]['main'],
            weather_api_response['weather'][0]['description'],
            weather_api_response['weather'][0]['icon'],
            (datetime.datetime.utcnow() +
             datetime.timedelta(seconds=weather_api_response['timezone'])),
            weather_api_response['visibility'],
            weather_api_response['wind']['speed'],
            weather_api_response['wind']['deg'],
            weather_api_response['main']['temp'],
            units.Pascal.from_hectopascal(
                weather_api_response['main']['pressure']),
            weather_api_response['main']['humidity']
        )


class OpenWeatherMapError(Exception):
    """ Raised when an error occurs during the Open Weather Map API request """
    pass


class CityNotFoundError(OpenWeatherMapError):
    """ Raised when a requested city was not found by the Open Weather Map API """
    pass
