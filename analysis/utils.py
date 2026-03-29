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

def get_fertilizer_details(fertilizer_name):
    """
    Returns the reason for farmer trust and benefits for a given fertilizer.
    """
    fertilizer_name = str(fertilizer_name).strip().upper()
    
    details = {
        'UREA': {
            'reason': 'Urea is highly trusted by farmers due to its high nitrogen content (46%) and rapid dissolution in water, making it immediately available to crops.',
            'benefits': 'Accelerates plant growth, enhances the green leafy growth (chlorophyll synthesis), and significantly increases overall yield, especially in early growth stages.'
        },
        'DAP': {
            'reason': 'Diammonium Phosphate (DAP) provides a quick boost of both Phosphorus and Nitrogen. Farmers trust it for root establishment and early crop resilience.',
            'benefits': 'Promotes strong root development, faster establishment of the crop, and provides essential energy for seed formation and blooming.'
        },
        '14-35-14': {
            'reason': 'This specific NPK blend is trusted for its perfect balance in soils that lack phosphorus but require basal doses of Nitrogen and Potassium.',
            'benefits': 'Ensures robust flowering, improved seed health, and resistance against environmental stress and diseases right from the planting stage.'
        },
        '28-28': {
            'reason': 'Farmers trust this balanced N-P complex fertilizer for crops that are in rapid vegetative growth stages requiring high nitrogen and phosphorus simultaneously.',
            'benefits': 'Offers immediate nutrient availability, improves stalk strength, and enhances tillering in cereal crops.'
        },
        '10-26-26': {
            'reason': 'Rich in Phosphorus and Potassium, farmers rely on it for root, fruit, and grain development where less Nitrogen is required.',
            'benefits': 'Improves the quality and size of grains/fruits, enhances crop resistance to pests and diseases, and strengthens plants against lodging.'
        },
        '20-20': {
            'reason': 'A well-rounded Nitrogen-Phosphorus fertilizer trusted for balanced growth across various soil types.',
            'benefits': 'Promotes healthy vegetative growth alongside robust root systems, establishing a strong foundation for the mature plant.'
        },
        'MAGNESIUM SULPHATE': {
            'reason': 'Often known as Epsom Salt, farmers trust it to quickly correct Soil Magnesium deficiencies which cause yellowing of leaves.',
            'benefits': 'Restores healthy green color (essential for photosynthesis in chlorophyll), improves nutrient uptake, and boosts overall crop vitality.'
        },
        'SSP': {
            'reason': 'Single Super Phosphate is trusted not just for Phosphorus but also for supplying essential secondary nutrients like Sulphur and Calcium.',
            'benefits': 'Strengthens root development, improves crop quality (especially oil content in oilseeds), and enriches the soil structure.'
        },
        'MOP': {
            'reason': 'Muriate of Potash (MOP) is highly trusted as a direct source of Potassium, critical for enzyme activation and water regulation in plants.',
            'benefits': 'Protects crops from drought by regulating water loss, improves grain fullness, and significantly enhances shelf-life and aesthetic quality of produce.'
        }
    }
    
    # Try exact match first
    if fertilizer_name in details:
        return details[fertilizer_name]
        
    # Try partial match (e.g., if model returns 'Magnesium' or '17-17-17')
    for key in details.keys():
        if key in fertilizer_name or fertilizer_name in key:
            return details[key]
            
    # Default or generic response if not found
    return {
        'reason': f"This fertilizer is suggested based on your specific soil and climate parameters to balance the required NPK nutrients.",
        'benefits': f"Balances soil nutrient deficiency, promotes optimal health for the recommended crop, and maximizes yield potential."
    }

import datetime

def get_crop_schedule(crop_name, predicted_fertilizer, start_date=None):
    """
    Generates a generic timeline schedule for watering, fertilizing, and harvesting
    based on the predicted crop and start date.
    """
    if not start_date:
        start_date = datetime.date.today()
    elif isinstance(start_date, datetime.datetime):
        start_date = start_date.date()

    crop_name = str(crop_name).strip().upper()
    
    # Generic schedule template: list of tuples (days_gap, type 'water'/'fertilizer'/'harvest', instruction)
    schedules = {
        'COTTON': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (50%).'),
            (0, 'water', 'Light irrigation immediately after sowing.'),
            (20, 'water', 'First irrigation (2-3 inches). Gap: 20 days.'),
            (40, 'fertilizer', f'First top dressing. Apply {predicted_fertilizer} (25%). Gap: 40 days.'),
            (45, 'water', 'Second irrigation. Gap: 25 days.'),
            (70, 'fertilizer', f'Second top dressing. Apply {predicted_fertilizer} (25%) during flowering.'),
            (75, 'water', 'Third irrigation during boll formation. Gap: 30 days.'),
            (110, 'water', 'Final irrigation. Stop watering 20 days before first picking.'),
            (130, 'harvest', 'Start of first picking.')
        ],
        'SUGARCANE': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (30%).'),
            (0, 'water', 'Irrigation immediately after planting setts.'),
            (10, 'water', 'Light irrigation. Gap: 10 days.'),
            (30, 'water', 'Irrigation. Gap: 20 days.'),
            (45, 'fertilizer', f'First top dressing of {predicted_fertilizer} (30%). Gap: 45 days.'),
            (60, 'water', 'Irrigation before earthing up. Gap: 30 days.'),
            (90, 'fertilizer', f'Final top dressing of {predicted_fertilizer} (40%). Gap: 45 days.'),
            (120, 'water', 'Regular irrigation every 15-20 days during grand growth phase.'),
            (300, 'harvest', 'Stop watering 15-20 days prior to harvest. Harvest begins.')
        ],
        'RICE': [
            (0, 'water', 'Puddling and transplanting (keep 2-3 cm standing water).'),
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (50%).'),
            (15, 'water', 'Maintain 5 cm standing water till tillering. Gap: 15 days.'),
            (30, 'fertilizer', f'Top dressing of {predicted_fertilizer} (25%). Gap: 30 days.'),
            (50, 'water', 'Drain water for 2-3 days, then reflood to 5cm. Gap: 35 days.'),
            (60, 'fertilizer', f'Final top dressing of {predicted_fertilizer} (25%) at panicle initiation.'),
            (100, 'water', 'Drain completely 10-15 days before harvesting.'),
            (115, 'harvest', 'Harvesting.')
        ],
        'WHEAT': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (50%).'),
            (0, 'water', 'Pre-sowing irrigation (Palewa) for germination.'),
            (21, 'water', 'Crown Root Initiation (CRI) stage irrigation. Most critical. Gap: 21 days.'),
            (25, 'fertilizer', f'Top dress {predicted_fertilizer} (50%) after first irrigation.'),
            (45, 'water', 'Tillering stage irrigation. Gap: 24 days.'),
            (65, 'water', 'Late jointing stage irrigation. Gap: 20 days.'),
            (85, 'water', 'Flowering stage irrigation. Gap: 20 days.'),
            (105, 'water', 'Dough stage irrigation. Gap: 20 days.'),
            (130, 'harvest', 'Harvesting.')
        ],
        'JOWAR': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (50%).'),
            (30, 'water', 'Irrigation if dry spell occurs (Knee-high stage). Gap: 30 days.'),
            (35, 'fertilizer', f'Top dressing of {predicted_fertilizer} (50%). Gap: 35 days.'),
            (55, 'water', 'Irrigation at booting/flowering stage. Gap: 25 days.'),
            (80, 'water', 'Irrigation at grain filling stage. Gap: 25 days.'),
            (110, 'harvest', 'Harvesting.')
        ],
        'MAIZE': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (30%).'),
            (0, 'water', 'Light irrigation after sowing.'),
            (25, 'fertilizer', f'Top dress {predicted_fertilizer} (30%) at knee-high stage. Gap: 25 days.'),
            (30, 'water', 'Irrigation. Gap: 30 days.'),
            (50, 'fertilizer', f'Final top dress {predicted_fertilizer} (40%) at tasseling. Gap: 25 days.'),
            (55, 'water', 'Irrigation at silking/tasseling. Gap: 25 days.'),
            (75, 'water', 'Irrigation at dough stage. Gap: 20 days.'),
            (100, 'harvest', 'Harvesting.')
        ],
        'GROUNDNUT': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (100%).'),
            (0, 'water', 'Pre-sowing irrigation.'),
            (25, 'water', 'Irrigation at flowering stage. Gap: 25 days.'),
            (45, 'water', 'Irrigation at pegging stage. Gap: 20 days.'),
            (70, 'water', 'Irrigation at pod development. Gap: 25 days.'),
            (100, 'harvest', 'Harvesting.')
        ],
        'SOYBEAN': [
            (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (100%).'),
            (0, 'water', 'Irrigate immediately if soil lacks moisture.'),
            (30, 'water', 'Irrigate during flowering if dry. Gap: 30 days.'),
            (50, 'water', 'Irrigate during pod filling if dry. Gap: 20 days.'),
            (90, 'harvest', 'Harvesting.')
        ],
    }

    # Default generic schedule for Tur, Urad, Moong, Gram, Masoor, Ginger, Turmeric, Grapes etc.
    default_schedule = [
        (0, 'fertilizer', f'Apply basal dose of {predicted_fertilizer} (50%).'),
        (0, 'water', 'Irrigate immediately after sowing.'),
        (15, 'water', 'Second irrigation. Gap: 15 days.'),
        (30, 'fertilizer', f'Top dressing of {predicted_fertilizer} (50%). Gap: 30 days.'),
        (35, 'water', 'Third irrigation. Gap: 20 days.'),
        (60, 'water', 'Irrigation during flowering/fruiting phase. Gap: 25 days.'),
        (100, 'harvest', 'Harvesting depending on crop maturity.')
    ]

    selected_schedule = schedules.get(crop_name, default_schedule)

    # Build the final schedule array
    timeline = []
    
    # Explicit Sowing Step at Day 0
    sowing_date = start_date + datetime.timedelta(days=0)
    timeline.append({
        'days': 0,
        'date': sowing_date.strftime('%B %d, %Y'),
        'type': 'Sowing',
        'instruction': f"Sow {crop_name.title()} seeds or seedlings in the prepared field.",
        'color': 'info'
    })

    for days_gap, task_type, instruction in selected_schedule:
        task_date = start_date + datetime.timedelta(days=days_gap)
        
        # Friendly color based on task type
        color = 'primary' if task_type == 'water' else 'warning' if task_type == 'fertilizer' else 'success'
        
        timeline.append({
            'days': days_gap,
            'date': task_date.strftime('%B %d, %Y'),
            'type': task_type.capitalize(),
            'instruction': instruction,
            'color': color
        })

    return timeline

