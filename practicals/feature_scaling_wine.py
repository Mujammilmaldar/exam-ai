import pandas as pd
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load Wine dataset
wine = load_wine()

# Convert to DataFrame
df = pd.DataFrame(wine.data, columns=wine.feature_names)

print("Original Data:")
print(df.head())

# -----------------------------
# Standardization
# -----------------------------
standard_scaler = StandardScaler()

standardized_data = standard_scaler.fit_transform(df)

standardized_df = pd.DataFrame(standardized_data, columns=wine.feature_names)

print("\nStandardized Data:")
print(standardized_df.head())

# -----------------------------
# Normalization
# -----------------------------
minmax_scaler = MinMaxScaler()

normalized_data = minmax_scaler.fit_transform(df)

normalized_df = pd.DataFrame(normalized_data, columns=wine.feature_names)

print("\nNormalized Data:")
print(normalized_df.head())
