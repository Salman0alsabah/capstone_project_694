import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
import joblib

# Load the dataset
df = pd.read_csv('phishing_site_urls.csv')

# Separate features (URLs) and labels
X = df['URL']
y = df['Label']

# Convert labels to numerical format
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Create a pipeline that includes vectorization, scaling, and logistic regression with increased regularization
pipeline = Pipeline([
    ('vectorizer', CountVectorizer(max_features=5000, min_df=5, max_df=0.7)),
    ('scaler', StandardScaler(with_mean=False)),
    ('logistic', LogisticRegression(C=0.1, max_iter=1000, random_state=42))
])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the pipeline on the training set
pipeline.fit(X_train, y_train)

# Predictions and evaluations on the test set
y_pred_test = pipeline.predict(X_test)
accuracy_test = accuracy_score(y_test, y_pred_test)
conf_matrix_test = confusion_matrix(y_test, y_pred_test)
classification_rep_test = classification_report(y_test, y_pred_test)

# Perform 5-fold cross-validation and print the mean accuracy
cross_val_accuracy = cross_val_score(pipeline, X, y, cv=5).mean()
print(f'Cross-Validation Accuracy: {cross_val_accuracy}')

# Predictions and evaluations on the training set for comparison
y_pred_train = pipeline.predict(X_train)
accuracy_train = accuracy_score(y_train, y_pred_train)

# Print training and testing accuracy
print(f'Training Accuracy: {accuracy_train}')
print(f'Testing Accuracy: {accuracy_test}')

# Print testing performance metrics
print('Logistic Regression Model Testing Performance:')
print(f'Accuracy: {accuracy_test}')
print('Confusion Matrix:')
print(conf_matrix_test)
print('Classification Report:')
print(classification_rep_test)

# Save the pipeline and label encoder
joblib.dump(pipeline, 'phishing_detection_pipeline.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
