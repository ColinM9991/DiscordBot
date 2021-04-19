import datetime


class DcsWeatherMapper:
    def map(self, weather):
        return {
            'time': (datetime.datetime.utcnow() + datetime.timedelta(seconds=weather['timezone'])),
            'temperature': weather['main']['temp'],
            'pressure': weather['main']['pressure'],
            'wind': {
                'speed': weather['wind']['speed'],
                'direction': weather['wind']['deg']
            },
            'status': {
                'name': weather['weather'][0]['main'],
                'description': weather['weather'][0]['description']
            },
            'visibility': weather['visibility']
        }
