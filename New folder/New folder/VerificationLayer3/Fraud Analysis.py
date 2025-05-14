def analyze_transaction(self, transaction_data):
    # Makes real-time decisions based on fraud probability
    return {
        "decision": "decline" if fraud_prob > self.threshold else "approve",
        "risk_factors": self._identify_risk_factors(input_data)
    }