import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Construct absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # E-Kisaan root
MODEL_DIR = os.path.join(BASE_DIR, 'analysis', 'ml_models')
DATA_PATH = os.path.join(MODEL_DIR, 'Crop_and_fertilizer_cleaned.csv')
MODEL_PATH = os.path.join(MODEL_DIR, 'crop_model.pkl')
ENCODER_PATH = os.path.join(MODEL_DIR, 'encoder.pkl')

def load_data():
    if os.path.exists(DATA_PATH):
        print(f"Loading data from {DATA_PATH}...")
        df = pd.read_csv(DATA_PATH)
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        return df
    else:
        raise FileNotFoundError(f"{DATA_PATH} not found. Please ensure the dataset exists.")

def train():
    df = load_data()
    
    # Rename columns to match expected feature names (lowercase for consistency)
    df.rename(columns={
        'Nitrogen': 'N',
        'Phosphorus': 'P',
        'Potassium': 'K',
        'pH': 'ph',
        'Rainfall': 'rainfall',
        'Temperature': 'temperature',
        'Crop': 'label'
    }, inplace=True)
    
    # Features (Dropped 'humidity' as it is not in the new dataset)
    X = df[['N', 'P', 'K', 'temperature', 'ph', 'rainfall']]
    y = df['label']
    
    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Train model
    print("Training Random Forest Classifier for Crop Recommendation...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save model and encoder
    joblib.dump(rf, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Encoder saved to {ENCODER_PATH}")

if __name__ == "__main__":
    train()
