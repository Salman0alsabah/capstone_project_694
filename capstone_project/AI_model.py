import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load the dataset
df = pd.read_csv('phishing_site_urls.csv')

# Separate features (X) and labels (y)
X = df['URL']
y = df['Label']

# Convert labels to numerical format (0 for 'good', 1 for 'bad')
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# For simplicity, we'll use CountVectorizer to convert URLs into numerical features
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Standardize features using StandardScaler with with_mean=False for sparse matrices
scaler = StandardScaler(with_mean=False)
X_train_scaled = scaler.fit_transform(X_train_vec)
X_test_scaled = scaler.transform(X_test_vec)

# Logistic Regression model
logistic_model = LogisticRegression(max_iter=1000, random_state=42)
logistic_model.fit(X_train_scaled, y_train)
y_pred_logistic = logistic_model.predict(X_test_scaled)

# Evaluate the Logistic Regression model
accuracy_logistic = accuracy_score(y_test, y_pred_logistic)
conf_matrix_logistic = confusion_matrix(y_test, y_pred_logistic)
classification_rep_logistic = classification_report(y_test, y_pred_logistic)



# Save the model
joblib.dump(logistic_model, 'logistic_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(scaler, 'scaler.pkl')

print('Logistic Regression Model:')
print(f'Accuracy: {accuracy_logistic}')
print('Confusion Matrix:')
print(conf_matrix_logistic)
print('Classification Report:')
print(classification_rep_logistic)


