import unittest

from models import WeatherResponse
from models.units import Pascal


class CloudBaseTests(unittest.TestCase):

    def __init__(self, method_name):
        super().__init__(method_name)
        self.cloud_base_test_data = [
            {
                'temperature': 11.83,
                'humidity': 58,
                'cloud_base': 3202
            },
            {
                'temperature': 7.63,
                'humidity': 61,
                'cloud_base': 2820
            }
        ]

    def test_cloud_base_calculation(self):
        for test_data in self.cloud_base_test_data:
            expected_cloud_base = test_data['cloud_base']

            temperature = test_data['temperature']
            humidity = test_data['humidity']
            pressure = Pascal.from_hectopascal(996)

            weather_response_main = WeatherResponse.Main(temperature, pressure, humidity)

            calculated_cloud_base = weather_response_main.calculate_cloud_base()

            self.assertEqual(expected_cloud_base, calculated_cloud_base)