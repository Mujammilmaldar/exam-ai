# Q7A: K-Means Clustering on Text Documents
# Q7B: K-Means on 20 Newsgroups Dataset

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ========================================
# PART A: K-Means on Custom Text Documents
# ========================================

print("========== K-Means Clustering (Custom Documents) ==========\n")

documents = [
    "Machine learning is a branch of artificial intelligence",
    "Deep learning uses neural networks for modeling",
    "Natural language processing deals with text data",
    "Football is a popular sport worldwide",
    "Cricket is played in many countries",
    "Basketball requires speed and agility",
    "Python is a programming language for data science",
    "Java is used for enterprise applications",
    "Web development uses HTML CSS and JavaScript"
]

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# K-Means clustering
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X)

print(f"Number of clusters: {k}\n")
print("Clustering Results:")
for i, doc in enumerate(documents):
    print(f"  Cluster {kmeans.labels_[i]}: {doc}")

score = silhouette_score(X, kmeans.labels_)
print(f"\nSilhouette Score: {score:.4f}")

# ========================================
# PART B: K-Means on 20 Newsgroups Dataset
# ========================================

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
import numpy as np

print("\n\n========== K-Means on 20 Newsgroups ==========\n")

# Load subset of 20 Newsgroups
categories = ['comp.graphics', 'sci.med', 'soc.religion.christian', 'rec.sport.baseball']

print(f"Loading categories: {categories}")
newsgroups = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

print(f"Total documents: {len(newsgroups.data)}")

# TF-IDF vectorization
vectorizer2 = TfidfVectorizer(stop_words='english', max_features=5000)
X2 = vectorizer2.fit_transform(newsgroups.data)

# Apply K-Means
k2 = len(categories)
kmeans2 = KMeans(n_clusters=k2, random_state=42, n_init=10)
kmeans2.fit(X2)

# Evaluate
print(f"\nClusters: {k2}")
print(f"Silhouette Score: {silhouette_score(X2, kmeans2.labels_):.4f}")

# Show cluster distribution
print("\nCluster Distribution:")
for cluster_id in range(k2):
    count = np.sum(kmeans2.labels_ == cluster_id)
    print(f"  Cluster {cluster_id}: {count} documents")

# Show top terms per cluster
print("\nTop Terms per Cluster:")
order_centroids = kmeans2.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer2.get_feature_names_out()

for i in range(k2):
    top_terms = [terms[ind] for ind in order_centroids[i, :8]]
    print(f"  Cluster {i}: {', '.join(top_terms)}")
