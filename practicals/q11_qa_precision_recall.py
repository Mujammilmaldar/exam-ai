# Q11A: Question Answering System with given corpus
# Q11B: Precision, Recall, F-Measure (TP=60, FP=30, FN=20)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ========================================
# PART A: Question Answering System
# ========================================

print("========== Question Answering System ==========\n")

# Given corpus
corpus = [
    "India has the second-largest population in the world.",
    "It is surrounded by oceans from three sides which are Bay Of Bengal in the east, the Arabian Sea in the west and Indian oceans in the south.",
    "Tiger is the national animal of India.",
    "Peacock is the national bird of India.",
    "Mango is the national fruit of India."
]

print("Corpus:")
for i, doc in enumerate(corpus, 1):
    print(f"  {i}. {doc}")

# Question
question = "Which is the national bird of India?"
print(f"\nQuestion: '{question}'")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
corpus_vectors = vectorizer.fit_transform(corpus)
question_vector = vectorizer.transform([question])

# Calculate similarity scores
similarities = cosine_similarity(question_vector, corpus_vectors).flatten()

print("\nSimilarity Scores:")
for i, (doc, score) in enumerate(zip(corpus, similarities)):
    print(f"  Doc {i+1} (score: {score:.4f}): {doc[:60]}...")

# Find best matching document
best_idx = similarities.argmax()
print(f"\nAnswer: {corpus[best_idx]}")
print(f"Confidence Score: {similarities[best_idx]:.4f}")


# ========================================
# PART B: Precision, Recall, F-Measure
# ========================================

print("\n\n========== Precision, Recall, F-Measure ==========\n")

TP = 60
FP = 30
FN = 20

print(f"True Positives (TP): {TP}")
print(f"False Positives (FP): {FP}")
print(f"False Negatives (FN): {FN}")

recall = TP / (TP + FN)
print(f"\nRecall = TP / (TP + FN) = {TP} / ({TP} + {FN}) = {TP} / {TP + FN} = {recall:.4f}")

precision = TP / (TP + FP)
print(f"Precision = TP / (TP + FP) = {TP} / ({TP} + {FP}) = {TP} / {TP + FP} = {precision:.4f}")

f_score = 2 * (precision * recall) / (precision + recall)
print(f"F-Score = 2 * (P * R) / (P + R) = 2 * ({precision:.4f} * {recall:.4f}) / ({precision:.4f} + {recall:.4f}) = {f_score:.4f}")

print(f"\n--- Summary ---")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
print(f"F-Score:   {f_score:.4f} ({f_score*100:.2f}%)")
