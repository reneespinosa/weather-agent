import os
import aiohttp
from typing import Dict, Any, Optional
from .config import WEATHER_API_KEY, LANGUAGE, BASE_WEATHER_URL

async def _make_api_call(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make an API call to OpenWeather."""
    url = f"{BASE_WEATHER_URL}{endpoint}"
    params.update({
        'appid': WEATHER_API_KEY,
        'lang': LANGUAGE
    })
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            if response.status != 200:
                error_msg = data.get('message', 'Unknown error')
                raise Exception(f"Error {response.status}: {error_msg}")
            return data

async def get_weather(city: str) -> Dict[str, Any]:
    """Get current weather for a city."""
    params = {'q': city}
    return await _make_api_call('weather', params)

async def get_forecast(city: str, days: int = 5) -> Dict[str, Any]:
    """Get weather forecast for a city.
    
    Args:
        city: City name
        days: Number of days to forecast (1-5)
    """
    params = {
        'q': city,
        'cnt': days * 8
    }
    
    return await _make_api_call('forecast', params)

def kelvin_to_celsius(temperature: float) -> Dict[str, Any]:
    """Convert temperature from Kelvin to Celsius.
    
    Args:
        temperature: Temperature in Kelvin
        
    Returns:
        Dictionary with the converted temperature in Celsius
    """
    celsius = temperature - 273.15
    return {
        "kelvin": temperature,
        "celsius": celsius,
        "formatted": f"{celsius:.1f}°C"
    }

def miles_to_km(miles: float) -> Dict[str, Any]:
    """Convert distance from miles to kilometers.
    
    Args:
        miles: Distance in miles
        
    Returns:
        Dictionary with the converted distance in kilometers
    """
    kilometers = miles * 1.60934
    return {
        "miles": miles,
        "kilometers": kilometers,
        "formatted": f"{kilometers:.2f} km"
    }
