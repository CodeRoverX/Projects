import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Churn Prediction Dashboard", layout="wide",page_icon='bar_chart')

# Title and description
st.title("Customer Churn Prediction Dashboard")
st.markdown("### Predict if a customer will leave your service .")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "🔮 Predict", "📈 Analytics", "ℹ️ About",])

if page == "🏠 Home":
    st.header("Welcome to Customer Churn Predictor!")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 What is Customer Churn?")
        st.write("""
        Customer churn is when customers stop using your service. 
        Our AI model predicts which customers are likely to leave 
        so you can take action to retain them.
        """)
        
        st.subheader("🤖 Our Model")
        st.info("""
        - **Algorithm**: Logistic Regression
        - **Accuracy**: 79.91%
        - **Dataset**: 7,043 customers
        - **Features**: 19 customer attributes
        """)
    
    with col2:
        st.subheader("📊 Key Features")
        features = [
            "Demographics (Age, Gender)",
            "Services (Internet, Phone)",
            "Contract Details",
            "Payment Information",
            "Usage Patterns"
        ]
        for feature in features:
            st.write(f"✅ {feature}")
        
        st.subheader("🚀 How to Use")
        st.write("""
        1. Go to **Predict** page
        2. Enter customer details
        3. Click **Predict Churn**
        4. Get instant results!
        """)
elif page == "🔮 Predict":
    st.header("🔮 Customer Churn Prediction")
    st.markdown("Enter customer details below to predict churn probability")
     # Check if Flask API is running
    try:
        health_response = requests.get('http://localhost:5000/health', timeout=2)
        if health_response.status_code == 200:
            st.success("✅ API is running and ready!")
        else:
            st.error("❌ API is not responding properly")
    except:
        st.error("❌ Flask API is not running. Please start it first!")
        st.code("cd app && python app.py")
        st.stop()
     # Create input form
    with st.form("customer_form"):
        st.subheader("👤 Customer Demographics")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Female", "Male"])
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
            partner = st.selectbox("Has Partner", ["No", "Yes"])
            dependents = st.selectbox("Has Dependents", ["No", "Yes"])
            
        with col2:
            tenure = st.slider("Tenure (months)", 0, 72, 12)
            monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 150.0, 65.0, step=0.1)
            total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0, step=1.0)
        
        st.subheader("📞 Services")
        col3, col4 = st.columns(2)
        
        
        with col3:
            phone_service = st.selectbox("Phone Service", ["No", "Yes"])
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
            online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        
        with col4:
            device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
            tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
            streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
            streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        
        st.subheader("💳 Contract & Payment")
        col5, col6 = st.columns(2)
        
        with col5:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
        
        with col6:
            payment_method = st.selectbox("Payment Method", 
                                        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
            
        submitted = st.form_submit_button("🔮 Predict Churn",use_container_width=True)
        
        if submitted:
            # Convert categorical inputs to numerical
            def encode_input(value, options):
                return options.index(value)
            
            # Prepare data for API
            customer_data = {
                'gender': encode_input(gender, ["Female", "Male"]),
                'SeniorCitizen': encode_input(senior_citizen, ["No", "Yes"]),
                'Partner': encode_input(partner, ["No", "Yes"]),
                'Dependents': encode_input(dependents, ["No", "Yes"]),
                'tenure': tenure,
                'PhoneService': encode_input(phone_service, ["No", "Yes"]),
                'MultipleLines': encode_input(multiple_lines, ["No", "Yes", "No phone service"]),
                'InternetService': encode_input(internet_service, ["DSL", "Fiber optic", "No"]),
                'OnlineSecurity': encode_input(online_security, ["No", "Yes", "No internet service"]),
                'OnlineBackup': encode_input(online_backup, ["No", "Yes", "No internet service"]),
                'DeviceProtection': encode_input(device_protection, ["No", "Yes", "No internet service"]),
                'TechSupport': encode_input(tech_support, ["No", "Yes", "No internet service"]),
                'StreamingTV': encode_input(streaming_tv, ["No", "Yes", "No internet service"]),
                'StreamingMovies': encode_input(streaming_movies, ["No", "Yes", "No internet service"]),
                'Contract': encode_input(contract, ["Month-to-month", "One year", "Two year"]),
                'PaperlessBilling': encode_input(paperless_billing, ["No", "Yes"]),
                'PaymentMethod': encode_input(payment_method, ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]),
                'MonthlyCharges': monthly_charges,
                'TotalCharges': total_charges
            }
            
             # Make prediction
            try:
                with st.spinner("Making prediction..."):
                    response = requests.post('http://localhost:5000/predict', json=customer_data)
                    
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("Prediction completed!")
                    
                    col_result1, col_result2, col_result3 = st.columns(3)
                    
                    with col_result1:
                        if result['prediction'] == 1:
                            st.error(f"🚨 **WILL CHURN**")
                        else:
                            st.success(f"✅ **WILL STAY**")
                    
                    with col_result2:
                        churn_prob = result['churn_probability']
                        st.metric("Churn Probability", f"{churn_prob:.1%}")
                    
                    with col_result3:
                        risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                        st.metric("Risk Level", f"{risk_color.get(result['risk_level'], '⚪')} {result['risk_level']}")
                     # Probability gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = churn_prob * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Churn Probability (%)"},
                        delta = {'reference': 50},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 40], 'color': "lightgreen"},
                                {'range': [40, 70], 'color': "yellow"},
                                {'range': [70, 100], 'color': "red"}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 70}}))
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Recommendations
                    st.subheader("💡 Recommendations")
                    if result['prediction'] == 1:
                        st.warning("""
                        **High churn risk detected!** Consider these actions:
                        - 📞 Contact customer immediately
                        - 💰 Offer retention discount
                        - 🎁 Provide loyalty rewards
                        - 📞 Improve customer service
                        - 📋 Conduct satisfaction survey
                        """)
                    else:
                        st.info("""
                        **Customer looks stable!** Keep them happy:
                        - 🎯 Continue current service level
                        - 📧 Send satisfaction surveys
                        - 🆕 Introduce new features
                        - 💌 Loyalty program enrollment
                        """)
                else:
                    st.error("Failed to get prediction from API")
            except Exception as e:
                st.error(f"Error: {str(e)}")
            

elif page == "📈 Analytics":
    st.header("📈 Churn Analytics Dashboard")
    st.markdown("Understanding patterns in customer churn")
    
    # Sample analytics (you can expand this)
    st.subheader("📊 Key Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Model Accuracy", "79.91%", "2.1%")
    with col2:
        st.metric("Total Customers", "7,043", "")
    with col3:
        st.metric("Churn Rate", "26.5%", "")
    with col4:
        st.metric("Avg Monthly Charge", "$64.76", "")
    
    # Sample charts
    st.subheader("📈 Churn Factors")
    
    # Create sample data for visualization
    contract_data = pd.DataFrame({
        'Contract Type': ['Month-to-month', 'One year', 'Two year'],
        'Churn Rate': [42.7, 11.3, 2.8]
    })
    fig = px.bar(contract_data, x='Contract Type', y='Churn Rate', 
                 title='Churn Rate by Contract Type',
                 color='Churn Rate', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)
    
     # Feature importance
    st.subheader("🎯 Most Important Factors")
    importance_data = pd.DataFrame({
        'Feature': ['Contract Type', 'Tenure', 'Monthly Charges', 'Internet Service', 'Payment Method'],
        'Importance': [0.23, 0.19, 0.15, 0.12, 0.09]
    })
    
    fig2 = px.bar(importance_data, x='Importance', y='Feature',
                            title='Feature Importance in Churn Prediction')
    st.plotly_chart(fig2, use_container_width=True)
    
elif page == "ℹ️ About":
    st.header("ℹ️ About This Project")
    
    st.subheader("🎯 Project Overview")
    st.write("""
    This Customer Churn Prediction system uses machine learning to identify 
    customers who are likely to cancel their service. It's built with modern 
    tools and deployed as both an API and web interface.
    """)
    
    st.subheader("🛠️ Technology Stack")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Machine Learning:**
        - 🐍 Python
        - 📊 Pandas, NumPy
        - 🤖 Scikit-learn
        - 📈 Matplotlib, Seaborn
        """)
        
        st.markdown("""
        **Web Development:**
        - 🌐 Flask (API)
        - 🎨 Streamlit (UI)
        - 🐳 Docker
        """)
        
    with col2:
        st.markdown("""
        **Model Details:**
        - **Algorithm**: Logistic Regression
        - **Features**: 19 customer attributes
        - **Training Data**: 5,634 customers
        - **Test Data**: 1,409 customers
        - **Accuracy**: 79.91%
        """)
        
        st.markdown("""
        **Key Features:**
        - Real-time predictions
        - REST API
        - Interactive web interface
        - Docker deployment ready
        """)
    
    st.subheader("📚 How It Works")
    st.write("""
    1. **Data Collection**: Customer information is collected including demographics, services, and billing
    2. **Preprocessing**: Data is cleaned and encoded for machine learning
    3. **Model Training**: Logistic Regression algorithm learns patterns from historical data
    4. **Prediction**: New customer data is analyzed to predict churn probability
    5. **Action**: Business can take proactive steps to retain at-risk customers
    """)
    
    st.subheader("🚀 Future Improvements")
    improvements = [
        "Add more advanced algorithms (XGBoost, Neural Networks)",
        "Implement real-time model retraining",
        "Add customer segmentation analysis",
        "Include time-series forecasting",
        "Deploy to cloud platforms (AWS, GCP)",
        "Add A/B testing framework"
    ]
    
    for improvement in improvements:
        st.write(f"📌 {improvement}")
    
    st.subheader("👨‍💻 Developer")
    st.info("Built as part of AI/ML engineering portfolio project")


# Footer
st.markdown("---")
st.markdown("**Customer Churn Prediction System** | Built with ❤️ using Streamlit and Flask")