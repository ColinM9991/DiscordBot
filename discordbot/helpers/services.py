from os import environ
import helpers.dcsserverrepository
import weather.openmapweatherservice

dcs_server_repository = helpers.dcsserverrepository.DcsServerRepository(
    environ.get('DCS_PROFILE_PATH'),
    environ.get('FIREDAEMON_CONFIG_PATH'))

open_weather_map_service = weather.openmapweatherservice.OpenMapWeatherService(
    environ.get('DISCORD_OPEN_WEATHER_MAP_URL'),
    environ.get('DISCORD_OPEN_WEATHER_MAP_API_KEY'))
