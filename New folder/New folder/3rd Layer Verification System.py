
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class VerificationLayer3:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()
        self.features = ['typing_speed', 'product_price', 'payment_type']
        self.threshold = 0.85  # Confidence threshold
        
    def preprocess_data(self, data):
        """Process raw verification data"""
        # Convert payment type to numerical
        data['payment_type'] = data['payment_type'].map({'online': 0, 'direct': 1})
        
        # Feature engineering
        data['typing_speed_norm'] = self.scaler.fit_transform(data[['typing_speed']])
        data['price_category'] = pd.cut(data['product_price'],
                                      bins=[0, 100, 500, np.inf],
                                      labels=[0, 1, 2])
        return data[self.features + ['typing_speed_norm', 'price_category']]

    def train_model(self, historical_data):
        """Train fraud detection model"""
        # Historical data format: [typing_speed, product_price, payment_type, is_fraud]
        df = pd.DataFrame(historical_data, 
                        columns=self.features + ['is_fraud'])
        
        # Preprocess data
        processed_data = self.preprocess_data(df)
        
        # Split data
        X = processed_data
        y = df['is_fraud']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        preds = self.model.predict(X_test)
        print(f"Model Accuracy: {accuracy_score(y_test, preds):.2f}")
        print(classification_report(y_test, preds))
        
    def analyze_transaction(self, transaction_data):
        """Analyze transaction for fraud detection"""
        # Input format: {typing_speed, product_price, payment_type}
        df = pd.DataFrame([transaction_data], columns=self.features)
        processed = self.preprocess_data(df)
        
        # Get prediction probabilities
        proba = self.model.predict_proba(processed)[0]
        fraud_prob = proba[1]  # Probability of being fraud
        
        # Decision logic
        if fraud_prob > self.threshold:
            return {
                'status': 'decline',
                'confidence': fraud_prob,
                'reasons': self.get_fraud_reasons(processed)
            }
        return {'status': 'approve', 'confidence': 1 - fraud_prob}
    
    def get_fraud_reasons(self, data):
        """Explainable AI: Get reasons for fraud detection"""
        reasons = []
        if data['typing_speed_norm'].values[0] < -1.5:
            reasons.append("Abnormal typing speed")
        if data['price_category'].values[0] == 2:  # High value item
            reasons.append("High value transaction")
        if data['payment_type'].values[0] == 0:  # Online payment
            reasons.append("Risky payment method")
        return reasons

# Example usage
if __name__ == "__main__":
    # Initialize verification system
    verifier = VerificationLayer3()
    
    # Sample training data (replace with real historical data)
    historical_data = [
        [120, 150.0, 'online', 0],
        [80, 800.0, 'direct', 1],
        [95, 300.0, 'online', 0],
        [60, 1200.0, 'online', 1],
        [110, 200.0, 'direct', 0]
    ]
    
    # Train model
    verifier.train_model(historical_data)
    
    # Test transaction
    transaction = {
        'typing_speed': 70,  # In seconds
        'product_price': 950.0,
        'payment_type': 'online'
    }
    
    # Get verification decision
    result = verifier.analyze_transaction(transaction)
    print("\nTransaction Decision:")
    print(result)


