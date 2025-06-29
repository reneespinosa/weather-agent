# Weather Agent: Multi-Paradigm Programming Final Project

![Weather Agent](https://img.shields.io/badge/Weather%20Agent-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![ADK](https://img.shields.io/badge/Google%20ADK-Latest-orange)

A sophisticated weather agent built with Google's Agent Development Kit (ADK) that demonstrates multiple programming paradigms including functional, imperative, and asynchronous programming. This project serves as the final assignment for the Programming Languages course.

## Overview

Weather Agent is an intelligent assistant that provides comprehensive meteorological information for cities worldwide using the OpenWeatherMap API. The agent leverages multiple programming paradigms to deliver a robust, efficient, and user-friendly experience:

- **Functional Programming**: Pure functions, higher-order functions, function composition, and data transformations
- **Imperative Programming**: Sequential instructions, state modification, and control flow
- **Asynchronous Programming**: Non-blocking API calls for improved performance
- **Object-Oriented Programming**: Custom exception classes and structured data models

## Features

### Core Capabilities

- **Current Weather Data**: Detailed current conditions for any city worldwide
- **Weather Forecasts**: 5-day forecasts with 3-hour intervals
- **Weather Trend Analysis**: Temperature trends, dominant conditions, and statistical analysis
- **Unit Conversions**: Temperature and distance conversions with multiple formats

### Technical Highlights

- **Robust Error Handling**: Custom exceptions, validation, and user-friendly error messages
- **Functional Programming Utilities**: Pure functions, higher-order functions, and functional data processing
- **Asynchronous API Integration**: Non-blocking API calls using aiohttp
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Architecture

The project is structured around the following components:

- `agent.py`: Main agent configuration and prompt engineering
- `tools.py`: Core functionality including API calls and basic utilities
- `functional.py`: Functional programming utilities and data transformations
- `config.py`: Configuration settings and environment variables

### Programming Paradigms Demonstrated

#### Functional Programming
- Pure functions for data transformations
- Higher-order functions and function composition
- Map, filter, and reduce operations
- Immutable data structures
- Currying and partial application

#### Asynchronous Programming
- Asynchronous API calls with aiohttp
- Async/await syntax for non-blocking operations
- Concurrent data processing

#### Imperative Programming
- Sequential execution flow
- State management
- Conditional logic and loops

## Requirements

- Python 3.8 or higher
- Dependencies:
  - `aiohttp`: For asynchronous HTTP requests
  - `python-dotenv`: For environment variable management
  - `google-adk`: For agent development framework
- OpenWeatherMap API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/reneespinosa/weather-agent
   cd weather-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with:
   ```
   WEATHER_API_KEY=your_openweathermap_api_key
   ```
   
   > **Note**: Register on [OpenWeatherMap](https://openweathermap.org/) to get a free API key (it may take a few hours to activate).

## Usage

### Running the Agent

```bash
adk web
```

This will start the ADK web interface, typically available at http://localhost:8000.

### Available Tools

The agent provides the following tools:

- `get_weather(city)`: Gets the current weather for a city
- `get_forecast(city, days=5)`: Gets the weather forecast for a city
- `analyze_weather_trends(city, days=5)`: Analyzes weather trends using functional programming
- `kelvin_to_celsius(temperature)`: Converts temperature from Kelvin to Celsius
- `miles_to_km(miles)`: Converts distance from miles to kilometers

### Example Queries

- "What's the current weather in London?"
- "Show me the forecast for Tokyo for the next 3 days"
- "Analyze weather trends in New York"
- "Convert 300 Kelvin to Celsius"
- "How many kilometers are in 10 miles?"

## Weather Trend Analysis

The `analyze_weather_trends` tool demonstrates functional programming principles by:

1. Extracting temperature data using pure functions
2. Calculating trends with higher-order functions
3. Transforming data with map, filter, and reduce operations
4. Maintaining immutability throughout the analysis process
5. Composing functions for complex data processing

Results include temperature trends (warming, cooling, stable), dominant weather conditions, temperature ranges, and daily averages.

## Error Handling

The system implements robust error handling with:

- Custom exception classes (`WeatherAPIError`, `ValidationError`)
- Parameter validation for all functions
- Comprehensive logging with different severity levels
- User-friendly error messages and suggestions

## Security Notes

- Keep API keys private and do not share them publicly
- The agent uses environment variables for secure credential management
- All API calls are made over HTTPS for data security

## Academic Context

This project was developed as the final assignment for the Programming Languages course, demonstrating the practical application of multiple programming paradigms in a real-world application. The implementation showcases how different paradigms can be combined effectively to create robust, maintainable, and efficient software.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

 2025 René Espinosa - Programming Languages Final Project
