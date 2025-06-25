import requests

# Test data for a customer
customer_data = {
    'gender': 1,
    'SeniorCitizen': 0,
    'Partner': 1,
    'Dependents': 0,
    'tenure': 12,
    'PhoneService': 1,
    'MultipleLines': 0,
    'InternetService': 1,
    'OnlineSecurity': 0,
    'OnlineBackup': 1,
    'DeviceProtection': 0,
    'TechSupport': 0,
    'StreamingTV': 1,
    'StreamingMovies': 0,
    'Contract': 1,
    'PaperlessBilling': 1,
    'PaymentMethod': 2,
    'MonthlyCharges': 65.5,
    'TotalCharges': 786.0
}

# Send prediction request
response = requests.post('http://localhost:5000/predict', json=customer_data)
print("Prediction result:")
print(response.json())