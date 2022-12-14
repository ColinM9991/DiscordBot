from dcs.weather import Wind
from models.units import InchOfMercury


class WeatherResult:
    time: str
    preset_name: str
    temperature: int
    cloud_base: int
    pressure: InchOfMercury
    wind_at_ground: Wind
    wind_at_2000: Wind
    wind_at_8000: Wind

    def __init__(self,
                 time,
                 preset_name: str,
                 temperature: int,
                 cloud_base: int,
                 pressure: InchOfMercury,
                 wind_at_ground: Wind,
                 wind_at_2000: Wind,
                 wind_at_8000: Wind):
        self.time = time.strftime('%c')
        self.preset_name = preset_name
        self.temperature = temperature
        self.cloud_base = cloud_base
        self.pressure = pressure
        self.wind_at_ground = wind_at_ground
        self.wind_at_2000 = wind_at_2000
        self.wind_at_8000 = wind_at_8000
