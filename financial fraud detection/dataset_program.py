import pandas as pd
import random
from faker import Faker
import uuid
import datetime

# Seed for reproducibility
random.seed(42)

# Initialize Faker for generating fake data
fake = Faker('en_IN')

def generate_transaction(is_fraud):
    transaction_id = str(uuid.uuid4())
    merchant = fake.company()
    amount = round(random.uniform(10, 1000), 2)
    timestamp = fake.date_time_between(start_date='-30d', end_date='now')
    location = fake.city()

    return {
        'TransactionID': transaction_id,
        'Merchant': merchant,
        'Amount': amount,
        'Timestamp': timestamp,
        'Location': location,
        'IsFraud': is_fraud,
    }

# Generate synthetic transactions
num_real_transactions = int(0.7 * 1000)  # 70% real
num_fake_transactions = 1000 - num_real_transactions  # 30% fake

real_transactions = [generate_transaction(is_fraud=False) for _ in range(num_real_transactions)]
fake_transactions = [generate_transaction(is_fraud=True) for _ in range(num_fake_transactions)]

# Combine real and fake transactions
transactions = real_transactions + fake_transactions

# Shuffle the transactions
random.shuffle(transactions)

# Create a DataFrame
df = pd.DataFrame(transactions)

# Save the dataset to a CSV file
df.to_csv('indian_transaction_dataset.csv', index=False)

print("synthetic_fraud_dataset.csv'")
