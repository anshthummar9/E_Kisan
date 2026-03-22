import requests
import os

def get_weather_data(city):
    """
    Fetches temperature and estimated rainfall for a given city 
    using OpenWeatherMap API.
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    if not api_key:
        print("Warning: OPENWEATHER_API_KEY not found in environment variables.")
        return None

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric' # Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        temperature = data['main']['temp']
        
        # Rainfall is tricky. OWM Current Weather provides 'rain.1h' or 'rain.3h' if raining.
        # If not raining, it's 0. 
        # For the model, we arguably need *annual* or *seasonal* rainfall, 
        # which isn't available in current weather API.
        # FOR NOW: We will use a heuristic or just return 0 if no rain.
        # Ideally, we would ask the user for this or use a historical climate API.
        # Let's try to get current rain, else 0.
        rainfall = 0.0
        if 'rain' in data:
            if '1h' in data['rain']:
                rainfall = data['rain']['1h']
            elif '3h' in data['rain']:
                rainfall = data['rain']['3h']
        
        # NOTE: The ML model likely expects 'seasonal/annual average rainfall' (e.g. 1000mm),
        # whereas current weather gives 'instantaneous' rain (e.g. 2mm).
        # To make this realistic for the project without a paid climate API,
        # we might need to Mock this or ask user. 
        # However, per requirements, we fetch "Rainfall". 
        # We will return the current state, but user might need to override.
        
        return {
            'temperature': temperature,
            'rainfall': rainfall
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        # Return fallback/mock data so the app doesn't crash
        print("Using Mock Weather Data (Fallback)")
        return {
            'temperature': 25.0, # Average Temp
            'rainfall': 100.0    # Average Rainfall
        }
