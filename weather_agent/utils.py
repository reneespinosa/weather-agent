from typing import Dict, Any
from datetime import datetime

def format_temperature(temp_kelvin: float) -> str:
    """Convert temperature from Kelvin to Celsius and format it."""
    temp_celsius = temp_kelvin - 273.15
    return f"{temp_celsius:.1f}°C"

def format_weather_description(weather_data: Dict[str, Any]) -> str:
    """Format weather description."""
    main = weather_data['weather'][0]['main']
    description = weather_data['weather'][0]['description']
    temp = format_temperature(weather_data['main']['temp'])
    feels_like = format_temperature(weather_data['main']['feels_like'])
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind'].get('speed', 'N/A')
    
    return (
        f"🌡 *Temperature:* {temp}\n"
        f"🌡 *Feels like:* {feels_like}\n"
        f"💧 *Humidity:* {humidity}%\n"
        f"💨 *Wind:* {wind_speed} m/s\n"
        f"🌤 *Condition:* {main} ({description.capitalize()})"
    )

def format_forecast(forecast_data: Dict[str, Any], days: int = 5) -> str:
    """Format forecast for display.
    
    Args:
        forecast_data: Raw forecast data from OpenWeather API
        days: Number of days to show (1-5)
    """
    try:
        city = forecast_data.get('city', {}).get('name', 'Ubicación desconocida')
        country = forecast_data.get('city', {}).get('country', '')
        location = f"{city}, {country}" if country else city
        

        forecast_list = forecast_data.get('list', [])
        if not forecast_list:
            return f"No se encontraron datos de pronóstico para {location}"
        

        daily_forecasts = {}
        for forecast in forecast_list:
            try:

                dt = datetime.fromtimestamp(forecast['dt'])
                date_str = dt.strftime('%Y-%m-%d')
                
                if date_str not in daily_forecasts:
                    daily_forecasts[date_str] = {
                        'date': dt,
                        'forecasts': []
                    }
                daily_forecasts[date_str]['forecasts'].append(forecast)
            except (KeyError, ValueError) as e:
                logger.warning(f"Error al procesar pronóstico: {e}")
                continue
        

        sorted_days = sorted(daily_forecasts.items(), key=lambda x: x[0])[:days]
        

        result = [f"🌤 *Pronóstico para {location}* (próximos {len(sorted_days)} días):\n"]
        
        for date_str, day_data in sorted_days:
            forecasts = day_data['forecasts']
            if not forecasts:
                continue
                

            best_forecast = min(
                forecasts, 
                key=lambda x: abs(x['dt'] - (day_data['date'].replace(hour=12, minute=0).timestamp()))
            )
            

            try:

                import locale
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                date_formatted = best_forecast['dt']
                date_formatted = datetime.fromtimestamp(date_formatted).strftime('%A %d de %B')
                date_formatted = date_formatted.capitalize()
            except:
                date_formatted = datetime.fromtimestamp(best_forecast['dt']).strftime('%A, %d %B')
            

            temp = best_forecast['main']['temp']
            temp_min = best_forecast['main']['temp_min']
            temp_max = best_forecast['main']['temp_max']
            description = best_forecast['weather'][0]['description'].capitalize()
            humidity = best_forecast['main']['humidity']
            wind_speed = best_forecast.get('wind', {}).get('speed', 'N/A')

            weather_icon = {
                'clear': '☀️',
                'clouds': '☁️',
                'rain': '🌧️',
                'snow': '❄️',
                'thunderstorm': '⛈️',
                'drizzle': '🌦️',
                'mist': '🌫️'
            }.get(best_forecast['weather'][0]['main'].lower(), '🌤️')

            forecast_line = (
                f"📅 *{date_formatted}* {weather_icon}\n"
                f"   {description}\n"
                f"   🌡 {temp:.1f}°C (Máx: {temp_max:.1f}°C • Mín: {temp_min:.1f}°C)\n"
                f"   💧 Humedad: {humidity}% • 💨 Viento: {wind_speed} m/s\n"
            )
            result.append(forecast_line)
        
        return "\n".join(result)
    
    except Exception as e:
        logger.error(f"Error formateando pronóstico: {e}", exc_info=True)
        return "❌ Error al formatear el pronóstico. Por favor, inténtalo de nuevo más tarde."
