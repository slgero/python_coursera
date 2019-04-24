import requests

class YandexWeatherForecast:
    _cities = {'Moscow': [55.45, 37.37],
               'Ramenskoe': [55.567326, 38.225840]
               }
    def get(self, city):
        if not city in self._cities:
            print('Пока нет такого города в БД')
            return None
        coord = self._cities[city]
        url = f'https://api.weather.yandex.ru/v1/forecast?lat={coord[0]}&lon={coord[1]}'
        headers = {'X-Yandex-API-Key': 'bc92bbb0-422f-43a7-8f21-e0f59e3022de', 'lang': 'ru_RU'}
        data = requests.get(url, headers=headers).json()
        return data

    @staticmethod
    def print_today(fact):
        print('Температура в Раменском {}°С, ощущается как {}°С.'.format(fact.get('temp'),
                                                                         fact.get('feels_like')))
        if fact.get('feels_like') < 10:
            print('На улице очень холодно, одевайся теплее')
        elif fact.get('feels_like') < 20:
            print('На улице прохладно, лёгкая кофточка не повредит')
        else:
            print('На улице хорошо, смело надевай шорты :)')


class CityInfo:
    def __init__(self, city):
        self.city = city
        self._weather_forecast = YandexWeatherForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    city_info = CityInfo('Ramenskoe')
    forecast = city_info.weather_forecast()
    if forecast:
        YandexWeatherForecast.print_today(forecast.get('fact'))

# Для вызова программы только напрямую
if __name__ == "__main__":
    _main()