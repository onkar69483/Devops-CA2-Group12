import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the data
df = pd.read_csv('C:/Users/kvroh/OneDrive/Desktop/CA1_devops/data/test.csv')

# Drop 'Id' column if it exists
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# ------------------------------
# 📊 BASIC EDA
# ------------------------------
print("Target (Slope) stats:")
print(df['Slope'].describe())
print("\nCorrelation with Slope:\n", df.corr()['Slope'].sort_values(ascending=False).head(10))

# Histogram of Slope
sns.histplot(df['Slope'], kde=True, bins=30)
plt.title("Slope Distribution")
plt.show()

# Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=False, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

# ------------------------------
# 📦 TRAIN-TEST SPLIT
# ------------------------------
X = df.drop('Slope', axis=1)
y = df['Slope']

# Optional: scale continuous features
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled.iloc[:, :10] = scaler.fit_transform(X_scaled.iloc[:, :10])

# Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ------------------------------
# 🤖 RANDOM FOREST REGRESSOR
# ------------------------------
rf = RandomForestRegressor(random_state=42)

# Hyperparameter tuning
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
}

grid = GridSearchCV(rf, param_grid, cv=3, n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)

# Best model
best_rf = grid.best_estimator_

# Predict
y_pred = best_rf.predict(X_test)

# ------------------------------
# 📊 EVALUATION
# ------------------------------
print("Best Parameters:\n", grid.best_params_)
print("\nMean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

# Feature Importance Plot
importances = pd.Series(best_rf.feature_importances_, index=X.columns)
importances.nlargest(15).plot(kind='barh')
plt.title("Top 15 Feature Importances")
plt.show()
