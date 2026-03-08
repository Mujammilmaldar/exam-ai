# Q5A: Cosine Similarity
# Q5B: Question Answering System

import math
from collections import Counter

# ========================================
# PART A: Cosine Similarity
# ========================================

print("========== Cosine Similarity ==========\n")

query = "gold silver truck"
document = "shipment of gold damaged in a gold fire"

print(f"Query: '{query}'")
print(f"Document: '{document}'")

# Tokenize
query_words = query.lower().split()
doc_words = document.lower().split()

# Get all unique terms
all_terms = list(set(query_words + doc_words))
all_terms.sort()

print(f"\nAll terms: {all_terms}")

# Create term frequency vectors
query_vector = [query_words.count(term) for term in all_terms]
doc_vector = [doc_words.count(term) for term in all_terms]

print(f"\nTerm Frequency Table:")
print(f"{'Term':<12} {'Query':<8} {'Document':<8}")
print("-" * 28)
for term, q, d in zip(all_terms, query_vector, doc_vector):
    print(f"{term:<12} {q:<8} {d:<8}")

# Calculate cosine similarity
dot_product = sum(q * d for q, d in zip(query_vector, doc_vector))
magnitude_q = math.sqrt(sum(q ** 2 for q in query_vector))
magnitude_d = math.sqrt(sum(d ** 2 for d in doc_vector))

if magnitude_q == 0 or magnitude_d == 0:
    cosine_sim = 0
else:
    cosine_sim = dot_product / (magnitude_q * magnitude_d)

print(f"\nDot Product: {dot_product}")
print(f"Magnitude of Query: {magnitude_q:.4f}")
print(f"Magnitude of Document: {magnitude_d:.4f}")
print(f"\nCosine Similarity: {cosine_sim:.4f}")

# ========================================
# PART B: Question Answering System
# ========================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs

print("\n\n========== Question Answering System ==========\n")

# Knowledge base
corpus = [
    "Python is a popular programming language for data science.",
    "Machine learning is a subset of artificial intelligence.",
    "The capital of India is New Delhi.",
    "Deep learning uses neural networks with multiple layers.",
    "Natural language processing helps computers understand human language.",
    "The Earth revolves around the Sun.",
    "Data science involves statistics, programming, and domain knowledge."
]

# Question
question = "What is machine learning?"
print(f"Question: '{question}'")

# Build TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words='english')
corpus_vectors = vectorizer.fit_transform(corpus)
question_vector = vectorizer.transform([question])

# Find most similar document
similarities = cs(question_vector, corpus_vectors).flatten()

print(f"\nSimilarity Scores:")
for i, (doc, score) in enumerate(zip(corpus, similarities)):
    print(f"  Doc {i+1} (score: {score:.4f}): {doc}")

# Best match
best_idx = similarities.argmax()
print(f"\nAnswer: {corpus[best_idx]}")
print(f"Confidence: {similarities[best_idx]:.4f}")
