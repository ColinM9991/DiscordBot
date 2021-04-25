import dcs
import numpy
from dcs.cloud_presets import Clouds
from dcs.weather import CloudPreset, Wind

from helpers.units import Units


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

        self.mission.weather.wind_at_8000 = Wind(round((direction * numpy.random.normal(1, 0.1) + 180) % 360),
                                                 round(speed * numpy.random.normal(1.2, 0.1)))

        self.mission.weather.wind_at_2000 = Wind(round((direction * numpy.random.normal(1, 0.1) + 180) % 360),
                                                 round(speed * numpy.random.normal(1.1, 0.1)))

        self.mission.weather.wind_at_ground = Wind(round((direction * numpy.random.normal(1, 0.1) + 180) % 360),
                                                   round(speed * numpy.random.normal(1, 0.1)))

        self.mission.weather.fog_visibility = weather['visibility']

        cloud_preset = self.get_cloud_preset(weather['status']['name'])
        cloud_base = self.calculate_cloud_base(weather['main'])
        if cloud_base < cloud_preset.min_base or cloud_base > cloud_preset.max_base:
            cloud_base = numpy.random.randint(cloud_preset.min_base, cloud_preset.max_base)

        self.mission.weather.clouds_preset = cloud_preset
        self.mission.weather.clouds_base = cloud_base
        self.mission.weather.qnh = round(weather['main']['pressure'] * Units.hPa_to_mmHg)
        self.mission.weather.season_temperature = round(weather['main']['temperature'])
        self.mission.start_time = weather['time']

        return WeatherResult(self.mission.start_time,
                             cloud_preset.ui_name,
                             self.mission.weather.season_temperature,
                             self.mission.weather.clouds_base,
                             self.mission.weather.qnh)

    def get_cloud_preset(self, weather_status) -> CloudPreset:
        if weather_status in self.cloud_mappings:
            return numpy.random.choice(self.cloud_mappings[weather_status]).value

        return numpy.random.choice(self.cloud_mappings.values())

    @staticmethod
    def calculate_cloud_base(weather_main):
        """ Calculates the cloud base using the Magnus formula """
        humidity = weather_main['humidity']
        temperature = weather_main['temperature']
        alpha = 243.12
        beta = 17.62
        gamma = ((beta * temperature) / (alpha + temperature)) + numpy.log(humidity / 100)
        ans = (alpha * gamma) / (beta - gamma)
        spread = temperature - ans
        return round((spread / 2.5) * 1000)

    def save(self):
        self.mission.save()


class WeatherResult:
    time: str
    preset_name: str
    temperature: int
    cloud_base: int
    pressure: int

    def __init__(self,
                 time,
                 preset_name: str,
                 temperature: int,
                 cloud_base: int,
                 pressure: int):
        self.time = time.strftime('%c')
        self.preset_name = preset_name
        self.temperature = temperature
        self.cloud_base = cloud_base
        self.pressure = "{:.2f}inHg".format(pressure * Units.mmHg_to_inHg)
