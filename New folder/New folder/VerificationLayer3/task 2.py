
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

class ThirdLayerVerification:
    def __init__(self):
        # Model configuration
        self.model = GradientBoostingClassifier(n_estimators=150, random_state=42)
        self.threshold = 0.82  # Fraud probability threshold
        
        # Feature configuration
        self.numeric_features = ['typing_speed', 'product_price']
        self.categorical_features = ['payment_type']
        
        # Preprocessing pipeline
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numeric_features),
                ('cat', OneHotEncoder(), self.categorical_features)
            ])
        
        # Full pipeline
        self.pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', self.model)
        ])
        
    def collect_data(self, transaction_data):
        """Collect layer 3 verification data"""
        required_fields = ['user_id', 'typing_speed', 'product_price', 'payment_type']
        return {k: v for k, v in transaction_data.items() if k in required_fields}

    def train_model(self, historical_data_path):
        """Train the fraud detection model"""
        # Load historical data
        data = pd.read_csv(historical_data_path)
        
        # Prepare features and target
        X = data[['typing_speed', 'product_price', 'payment_type']]
        y = data['is_fraud']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate model
        train_acc = self.pipeline.score(X_train, y_train)
        test_acc = self.pipeline.score(X_test, y_test)
        print(f"Training Accuracy: {train_acc:.2f}")
        print(f"Testing Accuracy: {test_acc:.2f}")
        
        # Save model
        joblib.dump(self.pipeline, 'fraud_detection_model.pkl')

    def analyze_transaction(self, transaction_data):
        """Analyze transaction and make decision"""
        # Convert to DataFrame
        input_data = pd.DataFrame([transaction_data])
        
        # Predict fraud probability
        fraud_prob = self.pipeline.predict_proba(input_data)[0][1]
        
        # Make decision
        decision = "decline" if fraud_prob > self.threshold else "approve"
        
        return {
            "transaction_id": transaction_data.get('transaction_id'),
            "decision": decision,
            "fraud_probability": round(fraud_prob, 3),
            "risk_factors": self._identify_risk_factors(input_data),
            "timestamp": pd.Timestamp.now().isoformat()
        }

    def _identify_risk_factors(self, transaction):
        """Identify key risk factors using SHAP values"""
        # For demonstration - implement actual SHAP explanation in production
        risk_factors = []
        
        if transaction['typing_speed'].values[0] < 60:
            risk_factors.append("Abnormally fast typing speed")
        if transaction['product_price'].values[0] > 1000:
            risk_factors.append("High-value transaction")
        if transaction['payment_type'].values[0] == 'online':
            risk_factors.append("Risky payment method")
            
        return risk_factors if risk_factors else ["No significant risk factors"]

# Example Usage
if __name__ == "__main__":
    # Initialize verification system
    verifier = ThirdLayerVerification()
    
    # Train with historical data (CSV format: typing_speed,product_price,payment_type,is_fraud)
    verifier.train_model('historical_transactions.csv')
    
    # New transaction data
    new_transaction = {
        'transaction_id': 'TX123456',
        'user_id': 'ace45',
        'typing_speed': 45,  # In seconds
        'product_price': 1200.00,
        'payment_type': 'online'
    }
    new_transaction = {
        'transaction_id': 'TX190760',
        'user_id': 'ace78',
        'typing_speed': 52,  # In seconds
        'product_price': 1899.00,
        'payment_type': 'online'
    }
    
    # Analyze transaction
    result = verifier.analyze_transaction(new_transaction)
    print("\nTransaction Analysis Result:")
    print(f"Decision: {result['decision'].upper()}")
    print(f"Fraud Probability: {result['fraud_probability']:.1%}")
    print(f"Risk Factors: {', '.join(result['risk_factors'])}")




