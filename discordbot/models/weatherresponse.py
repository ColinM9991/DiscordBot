from dataclasses import dataclass
from datetime import datetime
from models.units import PressureUnit
import numpy


@dataclass
class WeatherResponse:
    @dataclass
    class Wind:
        speed: float
        direction: float

        def __init__(self, speed: float, direction: float):
            self.speed = speed
            self.direction = direction

    @dataclass
    class Info:
        name: str
        description: str
        icon: str

        def __init__(self, name: str, description: str, icon: str):
            self.name = name
            self.description = description
            self.icon = icon

    @dataclass
    class Main:
        temperature: float
        pressure: PressureUnit
        humidity: int

        def __init__(self, temperature: float, pressure: PressureUnit, humidity: int):
            self.temperature = temperature
            self.pressure = pressure
            self.humidity = humidity

        def calculate_cloud_base(self):
            """Calculates the cloud base using the Magnus formula"""
            humidity = self.humidity
            temperature = self.temperature
            alpha = 243.12
            beta = 17.62
            gamma = ((beta * temperature) / (alpha + temperature)) + numpy.log(
                humidity / 100
            )
            ans = (alpha * gamma) / (beta - gamma)
            spread = temperature - ans
            return round((spread / 2.5) * 1000)

    time: datetime
    visibility: int
    wind: Wind
    info: Info
    main: Main

    def __init__(
        self,
        name: str,
        description: str,
        icon: str,
        time: datetime,
        visibility: int,
        wind_speed: float,
        wind_direction: float,
        temperature: float,
        pressure: PressureUnit,
        humidity: int,
    ):
        self.time = time
        self.visibility = visibility
        self.wind = WeatherResponse.Wind(wind_speed, wind_direction)
        self.info = WeatherResponse.Info(name, description, icon)
        self.main = WeatherResponse.Main(temperature, pressure, humidity)
