# Q4A: PageRank Algorithm
# Q4B: Text Summarization (Extractive)

import numpy as np

# ========================================
# PART A: PageRank Algorithm
# ========================================

print("========== PageRank Algorithm ==========\n")

# Web graph structure:
# Page A -> B, C, D
# Page B -> C, E
# Page C -> A, D

pages = ['A', 'B', 'C', 'D', 'E']
n = len(pages)
page_index = {page: i for i, page in enumerate(pages)}

# Adjacency matrix (links)
links = {
    'A': ['B', 'C', 'D'],
    'B': ['C', 'E'],
    'C': ['A', 'D'],
    'D': [],
    'E': []
}

print("Link Structure:")
for page, targets in links.items():
    print(f"  Page {page} -> {targets if targets else 'No outgoing links'}")

# Build transition matrix
M = np.zeros((n, n))

for page, targets in links.items():
    if len(targets) > 0:
        for target in targets:
            M[page_index[target]][page_index[page]] = 1.0 / len(targets)

# Handle dangling nodes (pages with no outgoing links)
for j in range(n):
    if M[:, j].sum() == 0:
        M[:, j] = 1.0 / n

# Damping factor
d = 0.85

# PageRank iteration
pagerank = np.ones(n) / n  # Initial equal probability
print(f"\nInitial PageRank: {dict(zip(pages, np.round(pagerank, 4)))}")

# Iterate until convergence
for iteration in range(100):
    new_pagerank = (1 - d) / n + d * M @ pagerank

    # Check convergence
    if np.allclose(pagerank, new_pagerank, atol=1e-6):
        print(f"\nConverged after {iteration + 1} iterations")
        break
    pagerank = new_pagerank

# Results
print("\nFinal PageRank Scores:")
for page, score in zip(pages, pagerank):
    print(f"  Page {page}: {score:.6f}")

# Ranking
ranked = sorted(zip(pages, pagerank), key=lambda x: x[1], reverse=True)
print("\nPages ranked by importance:")
for rank, (page, score) in enumerate(ranked, 1):
    print(f"  {rank}. Page {page} (score: {score:.6f})")


# ========================================
# PART B: Extractive Text Summarization
# ========================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("\n\n========== Text Summarization (Extractive) ==========\n")

text = """Machine learning is a branch of artificial intelligence.
It allows computers to learn from data without being explicitly programmed.
Deep learning is a subset of machine learning that uses neural networks.
Neural networks are inspired by the human brain structure.
Machine learning has many applications in healthcare, finance, and technology.
Data preprocessing is an important step in any machine learning pipeline.
Supervised learning uses labeled data to train models.
Unsupervised learning finds patterns in unlabeled data.
Machine learning models can be evaluated using accuracy, precision, and recall.
The field of machine learning is rapidly growing and evolving."""

# Split into sentences
sentences = [s.strip() for s in text.strip().split('\n') if s.strip()]

print(f"Total sentences: {len(sentences)}")

# Calculate TF-IDF for each sentence
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(sentences)

# Calculate sentence scores using similarity to overall document
doc_vector = tfidf_matrix.mean(axis=0)
sentence_scores = cosine_similarity(tfidf_matrix, doc_vector).flatten()

# Select top N sentences for summary
n_summary = 3
top_indices = sentence_scores.argsort()[-n_summary:][::-1]
top_indices = sorted(top_indices)  # Keep original order

print(f"\nSummary ({n_summary} sentences):")
for idx in top_indices:
    print(f"  - {sentences[idx]}")
