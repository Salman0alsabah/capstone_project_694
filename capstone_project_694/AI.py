import joblib
import requests
import json
import time
import os
from  database import store_bad_link, check_url_in_database


# Function to load components
def load_components():
    dir_path = '/Users/salmanalsabah/Desktop/capstone_project_694'  # Adjust this to the path where your .pkl files are stored
    logistic_model_path = os.path.join(dir_path, 'logistic_model.pkl')
    label_encoder_path = os.path.join(dir_path, 'label_encoder.pkl')
    vectorizer_path = os.path.join(dir_path, 'vectorizer.pkl')
    scaler_path = os.path.join(dir_path, 'scaler.pkl')

    logistic_model = joblib.load(logistic_model_path)
    label_encoder = joblib.load(label_encoder_path)
    vectorizer = joblib.load(vectorizer_path)
    scaler = joblib.load(scaler_path)

    return logistic_model, label_encoder, vectorizer, scaler


# Function to predict URL safety
def predict_url_safety(url, logistic_model, label_encoder, vectorizer, scaler):
    url_vec = vectorizer.transform([url])
    url_scaled = scaler.transform(url_vec)
    prediction = logistic_model.predict(url_scaled)
    prediction_label = label_encoder.inverse_transform(prediction)[0]
    return prediction_label


# Function to submit URL to URLScan.io and fetch the scan result
def submit_to_urlscan_and_fetch_result(url, api_key):
    api_url = 'https://urlscan.io/api/v1/scan/'
    headers = {'Content-Type': 'application/json', 'API-Key': api_key}

    # Submit URL to URLScan.io
    payload = {'url': url, 'visibility': 'public'}
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_json = response.json()
        uuid = response_json.get('uuid')
        time.sleep(10)  # Wait for the scan to complete

        # Fetch the scan result
        result_url = f'https://urlscan.io/api/v1/result/{uuid}/'
        result_response = requests.get(result_url, headers=headers)
        if result_response.status_code == 200:
            result_json = result_response.json()
            score = result_json.get('verdicts', {}).get('urlscan', {}).get('score', 0)
            tags = result_json.get('verdicts', {}).get('urlscan', {}).get('tags', [])
            if score > 0.5 or 'malicious' in tags:
                return "bad"
    return "good"

def check_and_scan_url(url, api_key, ui_update_callback):
    logistic_model, label_encoder, vectorizer, scaler = load_components()

    # Check if the URL is already in the database
    db_status = check_url_in_database(url)
    if db_status == "bad":
        ui_update_callback(f"The URL {url} is already marked as bad in the database.", False)
        return

    # Use AI model to predict URL safety
    prediction_label = predict_url_safety(url, logistic_model, label_encoder, vectorizer, scaler)
    if prediction_label == "good":
        # If the URL is predicted as good, submit it to URLScan.io for further analysis
        scan_result = submit_to_urlscan_and_fetch_result(url, api_key)
        if scan_result == "bad":
            store_bad_link(url, scan_result)
            ui_update_callback(f"The URL {url} has been marked as bad after URLScan.io analysis.", False)
        else:
            ui_update_callback(f"The URL {url} is considered safe after URLScan.io analysis and AI model.", True)
    else:
        # If the AI model predicts the URL as unsafe, mark it as bad immediately
        store_bad_link(url, prediction_label)
        ui_update_callback(f"The URL {url} is considered potentially unsafe by the AI model and has been marked as bad.", False)