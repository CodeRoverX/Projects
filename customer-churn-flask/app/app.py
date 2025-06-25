from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)


# Load model and preprocessors
# print("Loading models...")

# # model = joblib.load('../models/churn_model.pkl')
# # scaler = joblib.load('../models/scaler.pkl')
# # feature_name = joblib.load('../models/feature_names.pkl')
# # ...existing code...

# Get the absolute path to the models directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')

model = joblib.load(os.path.join(MODELS_DIR, 'churn_model.pkl'))
scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
feature_name = joblib.load(os.path.join(MODELS_DIR, 'feature_names.pkl'))

# ...existing code...


@app.route('/')
def home():
    return jsonify({
        "message": "Customer Churn Prediction API",
        "model": "Logistic Regression",
        "accuracy": "79.91%",
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)"   
        }
    })
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        df = pd.DataFrame([data])
        
        for feature in feature_name:
            if feature not in df.columns:
                df[feature] = 0
                
        df = df[feature_name]
        
        df_scaled = scaler.transform(df)
        
        prediction = model.predict(df_scaled)[0]
        probability = model.predict_proba(df_scaled)[0][1]
        
        if probability >= 0.7:
            risk_level = "High"
        elif probability >= 0.4:
            risk_level = "Medium"
        else:
           risk_level = "Low"       
         
        return jsonify({
            'prediction': int(prediction),
            'churn_probability': round(float(probability), 4),
            'risk_level': risk_level,
            'message': f"Customer {'will' if prediction == 1 else 'will not'} churn"
        })

        
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        
        
        

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': True
    })
    
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)