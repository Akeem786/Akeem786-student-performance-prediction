import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv("student_data.csv")  # Make sure this file exists

# Display basic info
print("Dataset Head:")
print(data.head())

# Example feature selection (you can change as needed)
X = data[['study_hours', 'attendance', 'previous_scores']]
y = data['final_score']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"R² Score: {r2:.2f}")
print(f"RMSE: {rmse:.2f}")

# Optional: Plot results
plt.scatter(y_test, y_pred)
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Actual vs Predicted Student Performance")
plt.show()
