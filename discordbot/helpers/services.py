from os import environ
from helpers import DcsServerRepository
from weather import OpenMapWeatherService

dcs_server_repository = DcsServerRepository(
    environ.get('DCS_PROFILE_PATH'),
    environ.get('FIREDAEMON_CONFIG_PATH'))

open_weather_map_service = OpenMapWeatherService(
    environ.get('DISCORD_OPEN_WEATHER_MAP_URL'),
    environ.get('DISCORD_OPEN_WEATHER_MAP_API_KEY'))
