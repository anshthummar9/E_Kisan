from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SoilAnalysisForm
from .models import SoilReport
from .utils import get_weather_data
import joblib
import os
import pandas as pd
import numpy as np

# Load Models (Global to avoid reloading on every request)
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ml_models')

try:
    CROP_MODEL = joblib.load(os.path.join(MODEL_DIR, 'crop_model.pkl'))
    CROP_ENCODER = joblib.load(os.path.join(MODEL_DIR, 'encoder.pkl'))
    
    FERT_MODEL = joblib.load(os.path.join(MODEL_DIR, 'fert_model.pkl'))
    FERT_CROP_ENCODER = joblib.load(os.path.join(MODEL_DIR, 'fert_crop_encoder.pkl'))
    FERT_SOIL_ENCODER = joblib.load(os.path.join(MODEL_DIR, 'fert_soil_encoder.pkl'))
    print("ML Models loaded successfully.")
except Exception as e:
    print(f"Error loading ML models: {e}")
    CROP_MODEL = None

@login_required(login_url='login')
def analysis_view(request):
    if request.method == 'POST':
        form = SoilAnalysisForm(request.POST)
        if form.is_valid():
            try:
                # 1. Extract Soil Data
                data = form.cleaned_data
                soil_color = data['soil_color']
                N = data['nitrogen']
                P = data['phosphorus']
                K = data['potassium']
                ph = data['ph']
                city = form.cleaned_data.get('city')
                
                # 2. Get Weather Data
                weather = get_weather_data(city)
                if weather:
                    temp = weather['temperature']
                    rainfall = weather['rainfall']
                    if rainfall == 0:
                        # Fallback/Default if no rain info (optional: use average)
                        # For now, let's assume 100mm annual proxy or just use 0 if dry season
                        # Better approach: If < 0, use user input (if we had a field)
                        # Heuristic: If 0, maybe use 200 (moderate) to avoid skewing? 
                        # Let's keep 0 if API says 0, but user should know.
                        pass
                else:
                    # Default values (India Avg)
                    temp = 25.0
                    rainfall = 100.0
                    messages.warning(request, "Could not fetch weather. Using default values.")

                # 3. Model A: Crop Prediction
                # Feature Order: [N, P, K, temperature, ph, rainfall]
                features_a = pd.DataFrame([[N, P, K, temp, ph, rainfall]], 
                                        columns=['N', 'P', 'K', 'temperature', 'ph', 'rainfall'])
                crop_idx = CROP_MODEL.predict(features_a)[0]
                predicted_crop = CROP_ENCODER.inverse_transform([crop_idx])[0]
                
                # 4. Model B: Fertilizer Prediction
                # Feature Order: [N, P, K, Crop Type, Soil Type, ph, rainfall, temperature]
                
                # Encode Categoricals
                try:
                    crop_enc = FERT_CROP_ENCODER.transform([predicted_crop])[0]
                except ValueError:
                    print(f"Warning: Crop '{predicted_crop}' not seen by fertilizer model.")
                    crop_enc = 0 # Default/First class
                    
                try:
                    soil_enc = FERT_SOIL_ENCODER.transform([soil_color])[0]
                except ValueError:
                    print(f"Warning: Soil '{soil_color}' not seen. Using default.")
                    soil_enc = 0

                features_b = pd.DataFrame([[N, P, K, crop_enc, soil_enc, ph, rainfall, temp]], 
                                        columns=['N', 'P', 'K', 'Crop Type Encoded', 'Soil Type Encoded', 'ph', 'rainfall', 'temperature'])
                predicted_fertilizer = FERT_MODEL.predict(features_b)[0]
                
                # 5. Save to Database
                report = SoilReport.objects.create(
                    user=request.user,
                    soil_color=soil_color,
                    nitrogen=N,
                    phosphorus=P,
                    potassium=K,
                    ph=ph,
                    rainfall=rainfall,
                    temperature=temp,
                    predicted_crop=predicted_crop,
                    predicted_fertilizer=predicted_fertilizer
                )
                
                # We might want to save fertilizer too, but model doesn't have a field yet.
                # For now, we'll pass it to context.
                
                context = {
                    'report': report,
                    'fertilizer': predicted_fertilizer,
                    'city': city,
                    'weather': weather
                }
                return render(request, 'analysis/result.html', context)
                
            except Exception as e:
                print(f"Prediction Error: {e}")
                messages.error(request, f"Error during analysis: {e}")
                return redirect('analysis')
                
    else:
        form = SoilAnalysisForm()

    return render(request, 'analysis/input_form.html', {'form': form})

@login_required(login_url='login')
def report_detail_view(request, report_id):
    from django.shortcuts import get_object_or_404
    report = get_object_or_404(SoilReport, id=report_id, user=request.user)
    
    context = {
        'report': report,
        'fertilizer': report.predicted_fertilizer,
        'city': 'Not Specified',  # We did not save city in the model previously, but we have weather data
    }
    return render(request, 'analysis/report_detail.html', context)
