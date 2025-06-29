import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/"
LANGUAGE = "en"