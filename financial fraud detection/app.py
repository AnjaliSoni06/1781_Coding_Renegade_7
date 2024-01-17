from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from faker import Faker
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

fake = Faker()

# User registration CSV file
USER_DATA_FILE = 'user_data.csv'

# Check if the user data file exists; create it if not
if not os.path.exists(USER_DATA_FILE):
    user_columns = ['username', 'password', 'full_name', 'email', 'phone_number']
    user_df = pd.DataFrame(columns=user_columns)
    user_df.to_csv(USER_DATA_FILE, index=False)

# Load synthetic dataset
df = pd.read_csv("c:\\Users\\Asus\\Desktop\\python original\\financial fraud detection\\synthetic_fraud_dataset.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        user_data = pd.read_csv(USER_DATA_FILE)

        # Check if the username is already registered
        if username in user_data['username'].values:
            return render_template('register.html', message='Username already exists. Please choose another.')

        # Add the new user to the CSV file
        new_user = pd.DataFrame({'username': [username], 'password': [password], 'full_name': [full_name], 'email': [email], 'phone_number': [phone_number]})
        user_data = pd.concat([user_data, new_user], ignore_index=True)

        # Save the updated user data to the CSV file
        user_data.to_csv(USER_DATA_FILE, index=False)

        # Set the user session after registration
        session['username'] = username

        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = pd.read_csv(USER_DATA_FILE)

        # Check if the username and password match for any row in the DataFrame
        is_valid_user = (user_data['username'] == username).any() and (user_data['password'] == password).any()

        if is_valid_user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid username or password. Please try again.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login'))

@app.route('/transactions')
def transactions():
    transactions = df.to_dict(orient='records')
    return render_template('transactions.html', transactions=transactions)

@app.route('/fraud_detection/<string:transaction_id>', methods=['GET', 'POST'])
def fraud_detection(transaction_id):
    if request.method == 'POST':
        # Perform fraud detection logic here (dummy logic for illustration)
        is_fraudulent = random.choice([True, False])

        # Display the fraud detection result
        return render_template('fraud_detection_result.html', is_fraudulent=is_fraudulent)

    # Fetch transaction details for the given ID
    transaction = df[df['TransactionID'] == transaction_id].to_dict(orient='records')[0]
    return render_template('fraud_detection.html', transaction=transaction)

@app.route('/make_transaction', methods=['GET', 'POST'])
def make_transaction():
    if request.method == 'POST':
        # Retrieve transaction details from the form
        amount = float(request.form['amount'])
        merchant = request.form['merchant']
        location = request.form['location']

        # Perform fraud detection logic here (dummy logic for illustration)
        is_fraudulent = random.choice([True, False])

        # Display the fraud detection result
        return render_template('fraud_detection_result.html', is_fraudulent=is_fraudulent)

    return render_template('make_transaction.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
