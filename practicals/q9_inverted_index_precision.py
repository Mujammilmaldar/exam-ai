# Q9A: Inverted Index Construction & Document Retrieval
# Q9B: Precision, Recall, F-Measure (TP=20, FP=10, FN=30)

# ========================================
# PART A: Inverted Index & Document Retrieval
# ========================================

print("========== Inverted Index Construction ==========\n")

document1 = "best of luck tycs students for your practical examination"
document2 = "tycs students please carry your journal at the time of practical examination"

documents = {
    "document1": document1,
    "document2": document2
}

print("Documents:")
print(f"  Document 1: {document1}")
print(f"  Document 2: {document2}")

# Build inverted index
def build_inverted_index(docs):
    index = {}
    for doc_id, text in docs.items():
        words = text.lower().split()
        for position, word in enumerate(words):
            if word not in index:
                index[word] = {}
            if doc_id not in index[word]:
                index[word][doc_id] = []
            index[word][doc_id].append(position)
    return index

inverted_index = build_inverted_index(documents)

print("\nInverted Index:")
for term in sorted(inverted_index.keys()):
    postings = inverted_index[term]
    posting_str = ", ".join([f"{doc}: positions {pos}" for doc, pos in postings.items()])
    print(f"  '{term}' -> {posting_str}")

# Search for "tycs journal"
def search_query(query, index):
    terms = query.lower().split()
    results = {}

    for term in terms:
        if term in index:
            for doc_id in index[term]:
                if doc_id not in results:
                    results[doc_id] = set()
                results[doc_id].add(term)

    return results

query = "tycs journal"
print(f"\nSearch Query: '{query}'")
print(f"Query terms: {query.split()}")

results = search_query(query, inverted_index)

print("\nSearch Results:")
for doc_id, matched_terms in results.items():
    print(f"  {doc_id}: matched terms = {matched_terms}")
    print(f"    Content: {documents[doc_id]}")

# ========================================
# PART B: Precision, Recall, F-Measure
# ========================================

print("\n\n========== Precision, Recall, F-Measure ==========\n")

TP = 20
FP = 10
FN = 30

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
