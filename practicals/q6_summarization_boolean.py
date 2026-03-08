# Q6A: Text Summarization (Extractive)
# Q6B: Boolean Retrieval Model (BSc lectures corpus)

# ========================================
# PART A: Text Summarization (Extractive)
# ========================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("========== Text Summarization (Extractive) ==========\n")

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

sentences = [s.strip() for s in text.strip().split('\n') if s.strip()]

print(f"Total sentences: {len(sentences)}")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(sentences)

# Score sentences by similarity to document average
doc_vector = tfidf_matrix.mean(axis=0)
sentence_scores = cosine_similarity(tfidf_matrix, doc_vector).flatten()

# Display scores
print("\nSentence Scores:")
for i, (sent, score) in enumerate(zip(sentences, sentence_scores)):
    print(f"  [{score:.4f}] {sent}")

# Summary: top 3 sentences
n_summary = 3
top_indices = sorted(sentence_scores.argsort()[-n_summary:])

print(f"\nSummary ({n_summary} sentences):")
for idx in top_indices:
    print(f"  - {sentences[idx]}")

# ========================================
# PART B: Boolean Retrieval Model
# ========================================

print("\n\n========== Boolean Retrieval Model ==========\n")

# Corpus
documents = {
    "Document 1": "BSc lectures start at 7",
    "Document 2": "My lectures are over",
    "Document 3": "Today is a holiday"
}

# Build inverted index
def build_inverted_index(docs):
    index = {}
    for doc_id, text in docs.items():
        words = text.lower().split()
        for word in set(words):
            if word not in index:
                index[word] = set()
            index[word].add(doc_id)
    return index

inverted_index = build_inverted_index(documents)

print("Documents:")
for doc_id, text in documents.items():
    print(f"  {doc_id}: {text}")

print("\nInverted Index:")
for term, doc_list in sorted(inverted_index.items()):
    print(f"  '{term}': {doc_list}")

# Process Boolean query: "NOT lectures"
all_docs = set(documents.keys())

def boolean_query_not(term, index, all_docs):
    """Process NOT query - return all docs that DON'T contain the term"""
    if term in index:
        term_docs = index[term]
    else:
        term_docs = set()
    return all_docs - term_docs

query = "not lectures"
print(f"\nQuery: '{query}'")

# Documents containing "lectures"
lectures_docs = inverted_index.get("lectures", set())
print(f"Documents containing 'lectures': {lectures_docs}")

# NOT lectures = all docs - docs with lectures
result = all_docs - lectures_docs
print(f"Result of 'NOT lectures': {result}")

for doc_id in result:
    print(f"  {doc_id}: {documents[doc_id]}")
