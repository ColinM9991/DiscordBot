from os import environ

import yaml
import helpers.dcsserverrepository
import weather.openmapweatherservice

with open("config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile)

dcs_server_repository = helpers.dcsserverrepository.DcsServerRepository(
    config['dcs']['profile_path'],
    config['firedaemon']['service_names'])

open_weather_map_service = weather.openmapweatherservice.OpenMapWeatherService(
    environ.get('DISCORD_OPEN_WEATHER_MAP_URL'),
    environ.get('DISCORD_OPEN_WEATHER_MAP_API_KEY'))
