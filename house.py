import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Step 1: Data Preparation and Cleaning
# Load the dataset
try:
    df = pd.read_csv('Housing.csv')
except FileNotFoundError:
    print("Error: The file 'Housing.csv' was not found.")

# Convert binary categorical variables to 0s and 1s
print("Step 1: Data Preparation and Cleaning")
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_cols:
    df[col] = df[col].apply(lambda x: 1 if x == 'yes' else 0)

# Convert multi-class categorical 'furnishingstatus' to numerical using one-hot encoding
df = pd.get_dummies(df, columns=['furnishingstatus'], drop_first=True)
print("Data has been cleaned and encoded.")
print("First 5 rows of the cleaned data:")
print(df.head())

# Define the target variable
y = df['price']

# Step 2: Model Building and Comparison
print("\nStep 2: Building and Comparing Models")

# Simple Linear Regression Model
# Define the single feature (X) and split the data
X_simple = df[['area']]
X_simple_train, X_simple_test, y_simple_train, y_simple_test = train_test_split(X_simple, y, test_size=0.2, random_state=42)

# Build and train the simple model
simple_model = LinearRegression()
simple_model.fit(X_simple_train, y_simple_train)

# Make predictions on the test set
y_simple_pred = simple_model.predict(X_simple_test)

# Multiple Linear Regression Model
# Define the multiple features and split the data
features = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus_semi-furnished', 'furnishingstatus_unfurnished']
X_multi = df[features]
X_multi_train, X_multi_test, y_multi_train, y_multi_test = train_test_split(X_multi, y, test_size=0.2, random_state=42)

# Build and train the multiple model
multi_model = LinearRegression()
multi_model.fit(X_multi_train, y_multi_train)

# Make predictions on the test set
y_multi_pred = multi_model.predict(X_multi_test)

# Step 3: Model Evaluation
print("\nStep 3: Evaluating Model Performance")

# Evaluate the simple model
r2_simple = r2_score(y_simple_test, y_simple_pred)
rmse_simple = np.sqrt(mean_squared_error(y_simple_test, y_simple_pred))

# Evaluate the multiple model
r2_multi = r2_score(y_multi_test, y_multi_pred)
rmse_multi = np.sqrt(mean_squared_error(y_multi_test, y_multi_pred))

# Final Comparison
print("\nFinal Comparison of Models:")
print("--- Simple Linear Regression (using 'area' only) ---")
print(f"R-squared (R2) score: {r2_simple:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse_simple:.2f}")

print("\n--- Multiple Linear Regression (using multiple features) ---")
print(f"R-squared (R2) score: {r2_multi:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse_multi:.2f}")