from helpers import Units


class WeatherResult:
    time: str
    preset_name: str
    temperature: int
    cloud_base: int
    pressure: str

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
