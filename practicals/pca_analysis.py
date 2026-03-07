# pip install scikit-learn
# pip install matplotlib
# pip install pandas

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load Iris dataset
iris = load_iris()

# Features and target
X = iris.data
y = iris.target

# Feature names
features = iris.feature_names

# Convert to DataFrame (optional but cleaner)
df = pd.DataFrame(X, columns=features)

# Standardize the dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Apply PCA (reduce to 2 components)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Print explained variance
print("Explained Variance Ratio:", pca.explained_variance_ratio_)
print("Total Variance Explained:", sum(pca.explained_variance_ratio_))

# Create scatter plot of PCA results
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA - Iris Dataset')
plt.colorbar(scatter, label='Species')
plt.show()
