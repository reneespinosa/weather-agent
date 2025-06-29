from google.adk.agents import Agent
from . import tools

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="Weather Agent",
    instruction="""
    You are a weather agent that can provide weather information for a given city.
    You will be given a city name and your task is to provide the current weather information for that city.
    You can use the following tools:
    - Get weather information for a given city.
    - Get forecast for a given city.
    """,
    tools=[tools.get_weather, tools.get_forecast],
)