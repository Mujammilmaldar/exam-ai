# Q1A: Edit Distance between "write" and "right"
# Q1B: K-Means Clustering on Documents

# ========================================
# PART A: Edit Distance (Spelling Correction)
# ========================================

def edit_distance(str1, str2):
    m = len(str1)
    n = len(str2)

    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],       # Delete
                    dp[i][j - 1],       # Insert
                    dp[i - 1][j - 1]    # Replace
                )

    # Print DP table
    print("DP Table:")
    print("   ", "  ".join([" "] + list(str2)))
    for i in range(m + 1):
        row_label = " " if i == 0 else str1[i - 1]
        print(f" {row_label}", dp[i])

    return dp[m][n]

str1 = "write"
str2 = "right"

distance = edit_distance(str1, str2)
print(f"\nEdit Distance between '{str1}' and '{str2}': {distance}")

# ========================================
# PART B: K-Means Clustering on Documents
# ========================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Sample documents
documents = [
    "Machine learning is a subset of artificial intelligence",
    "Deep learning uses neural networks for modeling",
    "Natural language processing deals with text data",
    "Football is a popular sport worldwide",
    "Cricket is played in many countries",
    "Basketball requires speed and agility",
    "Python is a programming language for data science",
    "Java is used for enterprise applications",
    "Web development uses HTML CSS and JavaScript"
]

# Convert text to TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Apply K-Means clustering
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X)

# Results
print("\n\n========== K-Means Clustering ==========")
print(f"Number of clusters: {k}")
for i, doc in enumerate(documents):
    print(f"Cluster {kmeans.labels_[i]}: {doc}")

# Evaluate clustering
score = silhouette_score(X, kmeans.labels_)
print(f"\nSilhouette Score: {score:.4f}")
