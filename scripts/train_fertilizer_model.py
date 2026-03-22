import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Construct absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # E-Kisaan root
MODEL_DIR = os.path.join(BASE_DIR, 'analysis', 'ml_models')
DATA_PATH = os.path.join(MODEL_DIR, 'Crop_and_fertilizer_cleaned.csv')
MODEL_PATH = os.path.join(MODEL_DIR, 'fert_model.pkl')
ENCODER_PATH = os.path.join(MODEL_DIR, 'fert_crop_encoder.pkl')
SOIL_ENCODER_PATH = os.path.join(MODEL_DIR, 'fert_soil_encoder.pkl')

def train():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found.")

    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    # Strip whitespace from column names if any
    df.columns = df.columns.str.strip()
    
    # Map columns to standard names
    df.rename(columns={
        'Nitrogen': 'N',
        'Phosphorus': 'P',
        'Potassium': 'K',
        'Crop': 'Crop Type',
        'Fertilizer': 'Fertilizer Name',
        'Soil_color': 'Soil Type', # Using 'Soil Type' as feature name
        'pH': 'ph',
        'Rainfall': 'rainfall',
        'Temperature': 'temperature'
    }, inplace=True)
    
    # Features: N, P, K, Crop Type, Soil Type, ph, rainfall, temperature
    # We need to encode Crop Type and Soil Type
    
    # Encoders
    le_crop = LabelEncoder()
    df['Crop Type Encoded'] = le_crop.fit_transform(df['Crop Type'])
    
    le_soil = LabelEncoder()
    df['Soil Type Encoded'] = le_soil.fit_transform(df['Soil Type'])
    
    X = df[['N', 'P', 'K', 'Crop Type Encoded', 'Soil Type Encoded', 'ph', 'rainfall', 'temperature']]
    y = df['Fertilizer Name']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier (Model B - Enhanced)...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save model and encoders
    joblib.dump(rf, MODEL_PATH)
    joblib.dump(le_crop, os.path.join(MODEL_DIR, 'fert_crop_encoder.pkl'))
    joblib.dump(le_soil, os.path.join(MODEL_DIR, 'fert_soil_encoder.pkl'))
    
    print(f"Model saved to {MODEL_PATH}")
    print(f"Encoders saved to {MODEL_DIR} (fert_crop_encoder.pkl, fert_soil_encoder.pkl)")

if __name__ == "__main__":
    train()
