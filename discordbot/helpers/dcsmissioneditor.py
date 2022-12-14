import dcs
import numpy
from dcs.cloud_presets import Clouds
from dcs.weather import CloudPreset, Wind
from models import WeatherResult, WeatherResponse
from models.units import PressureUnit, Torr


class DcsMissionEditor:
    def __init__(self, mission_file):
        dcs_mission = dcs.Mission()
        dcs_mission.load_file(mission_file)

        self.mission = dcs_mission
        self.cloud_mappings = {
            'Clear': [
                Clouds.LightScattered1,
                Clouds.LightScattered2,
                Clouds.HighScattered1,
                Clouds.HighScattered2,
                Clouds.HighScattered3,
                Clouds.Scattered1,
                Clouds.Scattered2,
                Clouds.Scattered3,
                Clouds.Scattered4,
                Clouds.Scattered5,
                Clouds.Scattered6,
                Clouds.Scattered7,
            ],
            'Clouds': [
                Clouds.Broken1,
                Clouds.Broken2,
                Clouds.Broken3,
                Clouds.Broken4,
                Clouds.Broken5,
                Clouds.Broken6,
                Clouds.Broken7,
                Clouds.Broken8,
            ],
            'Rain': [
                Clouds.OvercastAndRain1,
                Clouds.OvercastAndRain2,
                Clouds.OvercastAndRain3,
            ],
            'Thunderstorm': [
                Clouds.Overcast1,
                Clouds.Overcast2,
                Clouds.Overcast3,
                Clouds.Overcast4,
                Clouds.Overcast5,
                Clouds.Overcast6,
                Clouds.Overcast7,
            ]
        }

    def set_weather(self, weather: WeatherResponse):
        speed = weather.wind.speed
        direction = weather.wind.direction

        self.mission.weather.wind_at_8000 = Wind(round((direction * numpy.random.normal(1, 0.1) + 180) % 360),
                                                 round(speed * numpy.random.normal(1.2, 0.1)))

        self.mission.weather.wind_at_2000 = Wind(round((direction * numpy.random.normal(1, 0.1) + 180) % 360),
                                                 round(speed * numpy.random.normal(1.1, 0.1)))

        self.mission.weather.wind_at_ground = Wind(round((direction * numpy.random.normal(1, 0.1) + 180) % 360),
                                                   round(speed * numpy.random.normal(1, 0.1)))

        self.mission.weather.fog_visibility = weather.visibility

        (cloud_preset, cloud_base) = self.get_cloud_preset(weather)

        pressure: Torr = weather.main.pressure.to_torr()

        self.mission.weather.clouds_preset = cloud_preset
        self.mission.weather.clouds_base = cloud_base
        self.mission.weather.qnh = round(pressure.value)
        self.mission.weather.season_temperature = round(weather.main.temperature)
        self.mission.start_time = weather.time

        return WeatherResult(self.mission.start_time,
                             cloud_preset.ui_name,
                             self.mission.weather.season_temperature,
                             cloud_base,
                             pressure.to_inch_of_mercury())

    def get_cloud_preset(self, weather: WeatherResponse) -> (CloudPreset, int):
        def get_random_preset() -> (CloudPreset, int):
            preset = numpy.random.choice(self.cloud_mappings.values())
            return preset, numpy.random.randint(preset.min_base, preset.max_base)

        cloud_mappings = self.cloud_mappings.values() if weather.info.name not in self.cloud_mappings else self.cloud_mappings[weather.info.name]
        cloud_base = weather.main.calculate_cloud_base()

        chosen_preset: CloudPreset or None = None

        for mapping in cloud_mappings:
            mapping_value = mapping.value

            if mapping_value.min_base > cloud_base or mapping_value.max_base < cloud_base:
                continue

            if chosen_preset is None:
                chosen_preset = mapping_value
                continue

            mapping_spread = mapping_value.max_base - mapping_value.min_base
            chosen_spread = chosen_preset.max_base - chosen_preset.min_base

            if abs(mapping_spread - cloud_base) < abs(chosen_spread - cloud_base):
                chosen_preset = mapping_value

        if chosen_preset is None:
            return get_random_preset()

        return chosen_preset, cloud_base

    def save(self):
        self.mission.save()
