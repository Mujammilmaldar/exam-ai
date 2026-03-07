# pip install pandas
# pip install scikit-learn
# pip install matplotlib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("titanic.csv")

# Select useful features
df = df[['Pclass', 'Sex', 'Age', 'Survived']]

# Convert categorical variable
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# Remove missing values
df = df.dropna()

# Features and target
X = df[['Pclass', 'Sex', 'Age']]
y = df['Survived']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Decision Tree Model
model = DecisionTreeClassifier()

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# Plot Decision Tree
plt.figure(figsize=(15, 10))
plot_tree(model, feature_names=['Pclass', 'Sex', 'Age'],
          class_names=['Not Survived', 'Survived'], filled=True)
plt.title("Decision Tree - Titanic Survival")
plt.show()
