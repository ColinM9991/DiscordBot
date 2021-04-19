import dcs
import numpy
from dcs.cloud_presets import Clouds
from dcs.weather import CloudPreset


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

    def set_weather(self, weather):
        speed = weather['wind']['speed']
        direction = weather['wind']['direction']

        self.mission.weather.wind_at_8000.speed = speed * numpy.random.normal(1.2, 0.1)
        self.mission.weather.wind_at_8000.direction = (direction * numpy.random.normal(1, 0.1) + 180) % 360

        self.mission.weather.wind_at_2000.speed = speed * numpy.random.normal(1.1, 0.1)
        self.mission.weather.wind_at_2000.direction = (direction * numpy.random.normal(1, 0.1) + 180) % 360

        self.mission.weather.wind_at_ground.speed = speed * numpy.random.normal(1, 0.1)
        self.mission.weather.wind_at_ground.direction = (direction * numpy.random.normal(1, 0.1) + 180) % 360
        self.mission.weather.qnh = (weather['pressure'] * 0.02953)

        self.mission.weather.fog_visibility = weather['visibility']

        cloud_preset = self.get_cloud_preset(weather['status']['name'])
        self.mission.weather.clouds_preset = cloud_preset
        self.mission.weather.clouds_base = numpy.random.randint(cloud_preset.min_base, cloud_preset.max_base)

        self.mission.start_time = weather['time']

        return WeatherResult(cloud_preset.ui_name, self.mission.weather.qnh)

    def get_cloud_preset(self, weatherstatus) -> CloudPreset:
        if weatherstatus in self.cloud_mappings:
            return numpy.random.choice(self.cloud_mappings[weatherstatus]).value

        return numpy.random.choice(self.cloud_mappings.values())

    def save(self):
        self.mission.save()


class WeatherResult:
    preset_name: str
    pressure: float

    def __init__(self, preset_name: str, pressure: float):
        self.preset_name = preset_name
        self.pressure = pressure
