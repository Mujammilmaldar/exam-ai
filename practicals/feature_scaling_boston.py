import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load Boston dataset manually
data_url = "http://lib.stat.cmu.edu/datasets/boston"

raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)

data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])

df = pd.DataFrame(data)

print("Original Data:")
print(df.head())

# Standardization
scaler = StandardScaler()
standardized = scaler.fit_transform(df)

print("\nStandardized Data:")
print(pd.DataFrame(standardized).head())

# Normalization
scaler2 = MinMaxScaler()
normalized = scaler2.fit_transform(df)

print("\nNormalized Data:")
print(pd.DataFrame(normalized).head())
