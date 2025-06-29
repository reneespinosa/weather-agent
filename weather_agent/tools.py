import os
import aiohttp
import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable, Tuple
from functools import reduce, partial
from datetime import datetime
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

# New tool using functional programming paradigm
async def analyze_weather_trends(city: str, days: int = 5) -> Dict[str, Any]:
    """Analyze weather trends for a city using functional programming.
    
    This function demonstrates functional programming concepts:
    - Pure functions
    - Higher-order functions
    - Function composition
    - Map, filter, reduce operations
    - Immutability
    
    Args:
        city: City name
        days: Number of days to analyze (1-5)
        
    Returns:
        Dictionary with weather trend analysis
        
    Raises:
        ValidationError: If parameters are invalid
        WeatherAPIError: If the API returns an error
    """
    # Validate parameters
    if not city or not isinstance(city, str) or len(city.strip()) == 0:
        logger.error("Invalid city parameter")
        raise ValidationError("City name must be a non-empty string")
    
    if not isinstance(days, int) or days < 1 or days > 5:
        logger.error(f"Invalid days parameter: {days}")
        raise ValidationError("Days must be an integer between 1 and 5")
    
    try:
        forecast_data = await get_forecast(city, days)

        def extract_temperatures(data: Dict[str, Any]) -> List[float]:
            """Extract temperature values from forecast data."""
            if 'list' not in data:
                return []
            return list(map(
                lambda item: item['main']['temp'],
                data['list']
            ))
        
        # Pure function to convert Kelvin to Celsius
        def k_to_c(temp: float) -> float:
            """Convert Kelvin to Celsius."""
            return temp - 273.15
        
        # Higher-order function for formatting
        def format_temp(temp: float) -> str:
            """Format temperature with unit."""
            return f"{k_to_c(temp):.1f}°C"
        
        # Pure function to calculate average using reduce
        def average(values: List[float]) -> float:
            """Calculate average of values using reduce."""
            if not values:
                return 0.0
            return reduce(lambda acc, val: acc + val, values, 0) / len(values)
        
        # Pure function to calculate temperature changes
        def calculate_changes(temps: List[float]) -> List[float]:
            """Calculate temperature changes between consecutive readings."""
            return list(map(
                lambda i: temps[i] - temps[i-1] if i > 0 else 0,
                range(len(temps))
            ))
        
        # Pure function to determine weather condition frequency
        def condition_frequency(data: Dict[str, Any]) -> Dict[str, int]:
            """Count frequency of each weather condition."""
            if 'list' not in data:
                return {}

            conditions = list(map(
                lambda item: item['weather'][0]['main'],
                data['list']
            ))
            

            return reduce(
                lambda acc, condition: {
                    **acc, 
                    condition: acc.get(condition, 0) + 1
                },
                conditions,
                {}
            )
        
        # Pure function to find dominant condition
        def dominant_condition(condition_counts: Dict[str, int]) -> Tuple[str, int]:
            """Find the most frequent weather condition."""
            if not condition_counts:
                return ("Unknown", 0)
            
            return max(
                condition_counts.items(),
                key=lambda item: item[1]
            )
        

        def categorize_trend(changes: List[float]) -> str:
            """Categorize temperature trend based on changes."""
            if not changes:
                return "stable"
            

            significant_changes = list(filter(
                lambda change: abs(change) > 1,
                changes
            ))
            

            trend_sum = sum(changes)
            
            if len(significant_changes) <= len(changes) * 0.2:
                return "stable"
            elif trend_sum > 0:
                return "warming"
            else:
                return "cooling"
        

        def analyze_data(data: Dict[str, Any]) -> Dict[str, Any]:
            """Analyze weather data using function composition."""
            temps = extract_temperatures(data)
            temp_changes = calculate_changes(temps)
            conditions = condition_frequency(data)
            main_condition, condition_count = dominant_condition(conditions)
            
            # Map temperatures to Celsius
            celsius_temps = list(map(k_to_c, temps))
            
            # Filter for temperature extremes
            if celsius_temps:
                min_temp = min(celsius_temps)
                max_temp = max(celsius_temps)
                temp_range = max_temp - min_temp
            else:
                min_temp = max_temp = temp_range = 0
            

            if 'list' in data:

                days_data = reduce(
                    lambda acc, item: {
                        **acc,
                        datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'): [
                            *acc.get(datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'), []),
                            item
                        ]
                    },
                    data['list'],
                    {}
                )
                

                daily_averages = list(map(
                    lambda day_items: {
                        'date': day_items[0],
                        'avg_temp': average([item['main']['temp'] for item in day_items[1]])
                    },
                    days_data.items()
                ))
            else:
                daily_averages = []
            
            return {
                'city': data.get('city', {}).get('name', city),
                'country': data.get('city', {}).get('country', ''),
                'average_temp': f"{k_to_c(average(temps)):.1f}°C",
                'min_temp': f"{min_temp:.1f}°C",
                'max_temp': f"{max_temp:.1f}°C",
                'temp_range': f"{temp_range:.1f}°C",
                'trend': categorize_trend(temp_changes),
                'dominant_condition': main_condition,
                'condition_frequency': conditions,
                'daily_averages': daily_averages,
                'data_points': len(temps),
                'analysis_timestamp': datetime.now().isoformat()
            }

        return analyze_data(forecast_data)
        
    except Exception as e:
        logger.error(f"Error analyzing weather trends for {city}: {str(e)}")
        raise
