import joblib
import requests
import json
from database import store_bad_link
from database import check_url_in_database
import time

# Load the model and preprocessing components
logistic_model_loaded = joblib.load('logistic_model.pkl')
label_encoder_loaded = joblib.load('label_encoder.pkl')
vectorizer_loaded = joblib.load('vectorizer.pkl')
scaler_loaded = joblib.load('scaler.pkl')

# Example list of new URLs to check
new_urls = ["https://usps.myepackage.com"]

# Transform URLs using the loaded vectorizer and scaler
new_urls_vec = vectorizer_loaded.transform(new_urls)
new_urls_scaled = scaler_loaded.transform(new_urls_vec)

# Predict using the loaded logistic model
new_predictions = logistic_model_loaded.predict(new_urls_scaled)

# Convert numerical predictions back to labels
new_predictions_labels = label_encoder_loaded.inverse_transform(new_predictions)

# URLScan.io API key and endpoint
api_key = 'ca44cc05-a78a-4a0a-ab83-71d46e971518'  # Replace with your actual API key
api_url = 'https://urlscan.io/api/v1/scan/'

# Headers for URLScan.io request
headers = {
    'Content-Type': 'application/json',
    'API-Key': api_key,
}

submissions = []  # To store URL and UUID for later result fetching

# Iterate over each URL and its corresponding prediction label
for url, label in zip(new_urls, new_predictions_labels):
    # Check if the URL is already in the database
    db_status = check_url_in_database(url)

    if db_status == "bad":
        print(f"The URL {url} is already marked as bad in the database, skipping URLScan.io submission.")
        continue  # Skip to the next URL without submitting to URLScan.io

    if label == "good":
        # Parameters for the POST request body to URLScan.io
        payload = {
            'url': url,
            'visibility': 'public'  # Can be 'public', 'private', or 'unlisted'
        }

        # Sending the POST request to URLScan.io API
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))

        # Parsing the JSON response
        response_json = response.json()

        # Output the submission response and store UUID for later fetching
        if response_json:
            uuid = response_json.get('uuid', 'N/A')
            submissions.append((url, uuid))
            print(f"URLScan.io scan submitted for {url}. Scan UUID: {uuid}")
        else:
            print(f"Failed to submit URL {url} to URLScan.io.")
    else:
        print(f"The URL {url} is considered potentially unsafe by AI model")
        store_bad_link(url, label)

# Function to fetch and analyze the scan result
def fetch_scan_result(uuid, api_key):
    result_url = f'https://urlscan.io/api/v1/result/{uuid}/'
    headers = {'API-Key': api_key}
    time.sleep(10)  

    # Fetching the scan result
    result_response = requests.get(result_url, headers=headers)
    if result_response.status_code == 200:
        result_json = result_response.json()

        # Analyze the scan result
        score = result_json.get('verdicts', {}).get('urlscan', {}).get('score', 0)
        tags = result_json.get('verdicts', {}).get('urlscan', {}).get('tags', [])

        if score > 0.5 or 'malicious' in tags:  # Adjust conditions based on your criteria
            return "bad"  
        else:
            return "good"  
    else:
        return "error"  

# Fetch and analyze scan results for each submitted URL
for url, uuid in submissions:
    result = fetch_scan_result(uuid, api_key)
    print(f"The URLScan.io scan result for {url} (UUID: {uuid}) is labeled as {result}.")
    if result == 'bad':
        store_bad_link(url, result)
