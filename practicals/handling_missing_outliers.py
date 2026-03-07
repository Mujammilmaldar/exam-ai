import pandas as pd
import numpy as np

df = pd.read_csv("cars.csv")

print("Original Data")
print(df)

# Handling missing values
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Salary'] = df['Salary'].fillna(df['Salary'].mean())

print("\nData after handling missing values:")
print(df)

# Outlier detection using IQR
Q1 = df['Salary'].quantile(0.25)
Q3 = df['Salary'].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df_no_outliers = df[(df['Salary'] >= lower) & (df['Salary'] <= upper)]

print("\nData after removing outliers:")
print(df_no_outliers)
