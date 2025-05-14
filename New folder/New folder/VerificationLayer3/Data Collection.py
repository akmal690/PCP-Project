def collect_data(self, transaction_data):
    # Collects typing speed, product price, and payment type
    return {k: v for k, v in transaction_data.items() if k in required_fields}
