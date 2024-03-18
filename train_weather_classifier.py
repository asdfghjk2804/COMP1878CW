from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.svm import SVC  # Chosen additional algorithm, Support Vector Classifier (SVC)

# Load forecast_data obtained from task 2
# Prepare data
X = forecast_data.drop(columns=['Weather Type'])  # Features
y = forecast_data['Weather Type']  # Target variable

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Training the classifiers
# RandomForestClassifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Chosen classifier (SVC)
svc_classifier = SVC(kernel='linear')  # You can customize the SVC as needed
svc_classifier.fit(X_train, y_train)

# Evaluating the performance
# RandomForestClassifier
rf_predictions = rf_classifier.predict(X_test)
rf_report = classification_report(y_test, rf_predictions)

# Chosen classifier (SVC)
svc_predictions = svc_classifier.predict(X_test)
svc_report = classification_report(y_test, svc_predictions)

# Print the classification reports
print("RandomForestClassifier Report:")
print(rf_report)

print("\nSupport Vector Classifier Report:")
print(svc_report)
