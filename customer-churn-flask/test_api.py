import requests
import json

base_url = 'http://localhost:5000'

print("Testing Customer Churn Prediction API")
print("="*50)

print("1. Testing health endpoint...")
response = requests.get(f'{base_url}') 
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()


# Test 2: Home endpoint
print("2. Testing home endpoint...")
response = requests.get(base_url)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()


# Test 3: Prediction - High churn risk customer
print("3. Testing prediction - High risk customer...")
high_risk_customer = {
    'gender': 1,           # Male
    'SeniorCitizen': 1,    # Senior citizen
    'Partner': 0,          # No partner
    'Dependents': 0,       # No dependents
    'tenure': 2,           # Short tenure (2 months)
    'PhoneService': 1,     # Has phone service
    'MultipleLines': 0,    # No multiple lines
    'InternetService': 2,  # Fiber optic
    'OnlineSecurity': 0,   # No online security
    'OnlineBackup': 0,     # No online backup
    'DeviceProtection': 0, # No device protection
    'TechSupport': 0,      # No tech support
    'StreamingTV': 0,      # No streaming TV
    'StreamingMovies': 0,  # No streaming movies
    'Contract': 0,         # Month-to-month contract
    'PaperlessBilling': 1, # Paperless billing
    'PaymentMethod': 1,    # Electronic check
    'MonthlyCharges': 85.0,# High monthly charges
    'TotalCharges': 170.0  # Low total charges (short tenure)
}

response = requests.post(f'{base_url}/predict', json=high_risk_customer)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()


# Test 4: Prediction - Low churn risk customer
print("4. Testing prediction - Low risk customer...")
low_risk_customer = {
    'gender': 0,           # Female
    'SeniorCitizen': 0,    # Not senior citizen
    'Partner': 1,          # Has partner
    'Dependents': 1,       # Has dependents
    'tenure': 60,          # Long tenure (5 years)
    'PhoneService': 1,     # Has phone service
    'MultipleLines': 1,    # Multiple lines
    'InternetService': 1,  # DSL
    'OnlineSecurity': 1,   # Has online security
    'OnlineBackup': 1,     # Has online backup
    'DeviceProtection': 1, # Has device protection
    'TechSupport': 1,      # Has tech support
    'StreamingTV': 1,      # Has streaming TV
    'StreamingMovies': 1,  # Has streaming movies
    'Contract': 2,         # Two year contract
    'PaperlessBilling': 0, # Not paperless billing
    'PaymentMethod': 0,    # Bank transfer
    'MonthlyCharges': 55.0,# Moderate monthly charges
    'TotalCharges': 3300.0 # High total charges (long tenure)
}



response = requests.post(f'{base_url}/predict', json=low_risk_customer)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

print("✅ API testing completed!")