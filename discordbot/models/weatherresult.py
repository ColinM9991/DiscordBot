from models.units import InchOfMercury


class WeatherResult:
    time: str
    preset_name: str
    temperature: int
    cloud_base: int
    pressure: InchOfMercury

    def __init__(self,
                 time,
                 preset_name: str,
                 temperature: int,
                 cloud_base: int,
                 pressure: InchOfMercury):
        self.time = time.strftime('%c')
        self.preset_name = preset_name
        self.temperature = temperature
        self.cloud_base = cloud_base
        self.pressure = pressure
