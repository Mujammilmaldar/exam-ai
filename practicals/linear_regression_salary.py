# pip install pandas
# pip install scikit-learn

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load dataset
df = pd.read_csv("salary_dataset.csv")

# Select independent and dependent variables
X = df[['YearsExperience']]   # input feature
y = df['Salary']              # output

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("R2 Score:", r2_score(y_test, y_pred))
print("Slope (Weight):", model.coef_)
print("Intercept:", model.intercept_)
