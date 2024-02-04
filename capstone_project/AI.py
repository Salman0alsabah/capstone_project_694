import joblib

# Load the model and preprocessing components
logistic_model_loaded = joblib.load('logistic_model.pkl')
label_encoder_loaded = joblib.load('label_encoder.pkl')
vectorizer_loaded = joblib.load('vectorizer.pkl')
scaler_loaded = joblib.load('scaler.pkl')

# To make a prediction with a new URL:
new_urls = [" https://prepa-yourmembrship.pages.mus.br/"]  # Example list of new URLs
new_urls_vec = vectorizer_loaded.transform(new_urls)
new_urls_scaled = scaler_loaded.transform(new_urls_vec)
new_predictions = logistic_model_loaded.predict(new_urls_scaled)

# Convert numerical predictions back to labels
new_predictions_labels = label_encoder_loaded.inverse_transform(new_predictions)
print(new_predictions_labels)
