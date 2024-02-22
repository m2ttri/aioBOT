import math
import random

import aiohttp
import pexelsPy

from config import WEATHER_API_URL, WEATHER_API_KEY, PEXELS_TOKEN, PEXELS_API_URL as API_URL

API = pexelsPy.API(PEXELS_TOKEN)


class Utils:

    @staticmethod
    async def get_total_results(message):
        """Получить количество изображений или видео по запрошенной категории"""

        user_request = message.split(' ')
        if user_request[0] == '/v':
            API.search_videos(user_request[1], page=1, results_per_page=1)
        else:
            API.search_photos(user_request[1], page=1, results_per_page=1)
        total_results = API.total_results
        print(f'Total results: {total_results}')
        return total_results

    @staticmethod
    async def get_random_page(message):
        """Получить случайную страницу с контентом по запросу"""

        total_results = await utils.get_total_results(message)
        if total_results != 0:
            user_request = message.split(' ')[1:]
            total_pages = math.ceil(int(total_results) / int(user_request[1]))
            random_page = random.randint(1, total_pages)
            print(f'Random page: {random_page}')
            return random_page

    @staticmethod
    async def get_user_name(message):
        """Получить имя пользователя"""

        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if last_name:
            return f"{first_name} {last_name}"
        return f"{first_name}"

    @staticmethod
    async def get_weather(message):
        """Получить погоду в указанном городе"""
        try:
            city = ' '.join(message.text.split(' ')[1:]).title()
            url = f'{WEATHER_API_URL}?q={city}&units=metric&lang=en&appid={WEATHER_API_KEY}'

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:

                    if resp.status != 200:
                        f'Error when receiving weather data 🌧️'

                    weather_data = await resp.json()
                    if weather_data.get('cod') == '404':
                        return f'{city} not found 🦆'
                    else:
                        temperature = round(weather_data['main']['temp'])
                        sky = weather_data['weather'][0]['main']
                        wind = round(weather_data['wind']['speed'])
                        return (f'{city}\n'
                                f'{temperature} °C\n'
                                f'{sky}\n'
                                f'{wind} m/s')
        except Exception as e:
            return f'Error when receiving weather {str(e)}'

    @staticmethod
    async def get_random_content(message):
        """Получить случайное изображение или видео по запросу PEXELS_API"""

        user_request = message.split(' ')
        results = user_request[2]

        random_page = await utils.get_random_page(message)

        if user_request[0] == '/v':
            API.search_videos(
                user_request[1],
                page=random_page,
                results_per_page=results
            )
            content = API.get_videos()
            category = 'video'
        else:
            API.search_photos(
                user_request[1],
                page=random_page,
                results_per_page=results
            )
            content = API.get_photos()
            category = 'photo'

        for item in content:
            url = f'{API_URL}/{category}/{item.id}/download'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.read()
                    yield data, category


utils = Utils()
