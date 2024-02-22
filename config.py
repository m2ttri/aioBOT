import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')

PEXELS_TOKEN = os.getenv('PEXELS_TOKEN')
PEXELS_API_URL = os.getenv('PEXELS_API_URL')

WEATHER_API_URL = os.getenv('WEATHER_API_URL')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
