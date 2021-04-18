import datetime


class DcsWeatherMapper:
    def map(self, weather):
        return {
            'time': (datetime.datetime.utcnow() + datetime.timedelta(seconds=weather['timezone']))
        }
