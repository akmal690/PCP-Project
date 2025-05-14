self.preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['typing_speed', 'product_price']),
        ('cat', OneHotEncoder(), ['payment_type'])
    ])
