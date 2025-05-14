import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Assume 'transaction_data.csv' has transaction features and a 'is_fraud' label
transaction_data = pd.read_csv('transaction_data.csv')
X = transaction_data.drop('is_fraud', axis=1)
y = transaction_data['is_fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier for fraud detection
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# When a new transaction occurs, predict if it's fraudulent
new_transaction_data = [...] # Extract features of the current transaction
fraud_probability = model.predict_proba(new_transaction_data)[:, 1]

if fraud_probability > 0.8: # Set a threshold
    # Trigger additional verification or hold the transaction
    print("High risk transaction detected!")
else:
    print("Transaction risk is low.")
