def train_model(self, historical_data_path):
    # Uses Gradient Boosting classifier for fraud detection
    self.pipeline.fit(X_train, y_train)
