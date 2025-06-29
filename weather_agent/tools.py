import os
import aiohttp
import logging
import asyncio
from typing import Dict, Any, Optional
from .config import WEATHER_API_KEY, LANGUAGE, BASE_WEATHER_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherAPIError(Exception):
    """Custom exception for OpenWeather API errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

class ValidationError(Exception):
    """Custom exception for parameter validation errors."""
    pass

async def _make_api_call(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make an API call to OpenWeather.
    
    Args:
        endpoint: API endpoint to call
        params: Query parameters for the API call
        
    Returns:
        Dictionary with the API response
        
    Raises:
        WeatherAPIError: If the API returns an error
        ConnectionError: If there's a network issue
        TimeoutError: If the API request times out
    """
    url = f"{BASE_WEATHER_URL}{endpoint}"
    
    # Verify that the API key is configured
    if not WEATHER_API_KEY:
        logger.error("API key not configured. Please set WEATHER_API_KEY in .env file")
        raise WeatherAPIError(401, "API key not configured")
    
    params.update({
        'appid': WEATHER_API_KEY,
        'lang': LANGUAGE
    })
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                data = await response.json()
                if response.status != 200:
                    error_msg = data.get('message', 'Unknown error')
                    logger.error(f"API Error {response.status}: {error_msg} for endpoint {endpoint} with params {params}")
                    raise WeatherAPIError(response.status, error_msg)
                return data
    except aiohttp.ClientConnectorError as e:
        logger.error(f"Connection error: {str(e)}")
        raise ConnectionError(f"Failed to connect to OpenWeather API: {str(e)}")
    except aiohttp.ClientResponseError as e:
        logger.error(f"Response error: {str(e)}")
        raise WeatherAPIError(e.status, str(e))
    except aiohttp.ClientError as e:
        logger.error(f"Client error: {str(e)}")
        raise ConnectionError(f"API request failed: {str(e)}")
    except asyncio.TimeoutError:
        logger.error("Request timed out")
        raise TimeoutError("OpenWeather API request timed out")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

async def get_weather(city: str) -> Dict[str, Any]:
    """Get current weather for a city.
    
    Args:
        city: City name
        
    Returns:
        Dictionary with current weather data
        
    Raises:
        ValidationError: If city parameter is invalid
        WeatherAPIError: If the API returns an error
        ConnectionError: If there's a network issue
    """
    if not city or not isinstance(city, str) or len(city.strip()) == 0:
        logger.error("Invalid city parameter")
        raise ValidationError("City name must be a non-empty string")
    
    try:
        params = {'q': city}
        return await _make_api_call('weather', params)
    except Exception as e:
        logger.error(f"Error getting weather for {city}: {str(e)}")
        raise

async def get_forecast(city: str, days: int = 5) -> Dict[str, Any]:
    """Get weather forecast for a city.
    
    Args:
        city: City name
        days: Number of days to forecast (1-5)
        
    Returns:
        Dictionary with forecast data
        
    Raises:
        ValidationError: If parameters are invalid
        WeatherAPIError: If the API returns an error
        ConnectionError: If there's a network issue
    """
    if not city or not isinstance(city, str) or len(city.strip()) == 0:
        logger.error("Invalid city parameter")
        raise ValidationError("City name must be a non-empty string")
    
    if not isinstance(days, int) or days < 1 or days > 5:
        logger.error(f"Invalid days parameter: {days}")
        raise ValidationError("Days must be an integer between 1 and 5")
    
    try:
        params = {
            'q': city,
            'cnt': days * 8
        }
        
        return await _make_api_call('forecast', params)
    except Exception as e:
        logger.error(f"Error getting forecast for {city}: {str(e)}")
        raise

def kelvin_to_celsius(temperature: float) -> Dict[str, Any]:
    """Convert temperature from Kelvin to Celsius.
    
    Args:
        temperature: Temperature in Kelvin
        
    Returns:
        Dictionary with the converted temperature in Celsius
        
    Raises:
        ValidationError: If temperature parameter is invalid
    """
    try:
        # Validate the temperature parameter
        if not isinstance(temperature, (float, int)):
            raise ValidationError("Temperature must be a number")
        
        # Validate that the temperature is not absurdly low (absolute zero is -273.15°C)
        if temperature < 0:
            logger.warning(f"Temperature below absolute zero: {temperature}K")
            raise ValidationError("Temperature cannot be below absolute zero (0K)")
        
        celsius = temperature - 273.15
        return {
            "kelvin": temperature,
            "celsius": celsius,
            "formatted": f"{celsius:.1f}°C"
        }
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error converting temperature: {str(e)}")
        raise ValueError(f"Failed to convert temperature: {str(e)}")

def miles_to_km(miles: float) -> Dict[str, Any]:
    """Convert distance from miles to kilometers.
    
    Args:
        miles: Distance in miles
        
    Returns:
        Dictionary with the converted distance in kilometers
        
    Raises:
        ValidationError: If miles parameter is invalid
    """
    try:
        # Validate the miles parameter
        if not isinstance(miles, (float, int)):
            raise ValidationError("Distance must be a number")
        
        # Validate that the distance is not negative
        if miles < 0:
            logger.warning(f"Negative distance provided: {miles} miles")
            raise ValidationError("Distance cannot be negative")
        
        kilometers = miles * 1.60934
        return {
            "miles": miles,
            "kilometers": kilometers,
            "formatted": f"{kilometers:.2f} km"
        }
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error converting distance: {str(e)}")
        raise ValueError(f"Failed to convert distance: {str(e)}")
