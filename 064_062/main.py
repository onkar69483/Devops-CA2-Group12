import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# Load the dataset (download 'train.csv' from Kaggle and place it in data/)
DATA_PATH = os.path.join("data", "train.csv")

try:
    data = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully. Shape: {data.shape}")
except FileNotFoundError:
    print("❌ Error: 'train.csv' not found in the 'data/' folder.")
    exit(1)

# Example preprocessing: drop missing rows
data = data.dropna()

# Select numerical columns (excluding id) as features
features = data.select_dtypes(include='number').drop(columns=['id'], errors='ignore')

# Define target variable (update with actual column name)
target_col = 'smoking_status'
if target_col in data.columns:
    y = data[target_col]
else:
    print(f"❌ Error: Target column '{target_col}' not found.")
    exit(1)

# Encode categorical target if needed
if y.dtype == 'object':
    from sklearn.preprocessing import LabelEncoder
    y = LabelEncoder().fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.33, random_state=42)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"✅ Model trained successfully. Accuracy: {accuracy * 100:.2f}%")
