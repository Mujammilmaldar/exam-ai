# Q3A: Edit Distance between "nature" and "creature"
# Q3B: Boolean Retrieval Model

# ========================================
# PART A: Edit Distance (Spelling Correction)
# ========================================

def edit_distance(str1, str2):
    m = len(str1)
    n = len(str2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

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

str1 = "nature"
str2 = "creature"

distance = edit_distance(str1, str2)
print(f"\nEdit Distance between '{str1}' and '{str2}': {distance}")

# ========================================
# PART B: Boolean Retrieval Model
# ========================================

print("\n\n========== Boolean Retrieval Model ==========")

# Corpus
documents = {
    "Document 1": "The cat chased the dog around the garden",
    "Document 2": "She was sitting in the garden last night",
    "Document 3": "I read the book the night before"
}

# Build inverted index
def build_inverted_index(docs):
    index = {}
    for doc_id, text in docs.items():
        words = text.lower().split()
        for word in set(words):  # Use set to avoid duplicates
            if word not in index:
                index[word] = set()
            index[word].add(doc_id)
    return index

inverted_index = build_inverted_index(documents)

print("\nInverted Index:")
for term, doc_list in sorted(inverted_index.items()):
    print(f"  '{term}': {doc_list}")

# Process Boolean query: "garden OR night"
def boolean_query(query, index, all_docs):
    tokens = query.lower().split()
    result = set()
    operator = "or"  # default

    for token in tokens:
        if token in ("and", "or", "not"):
            operator = token
        else:
            if token in index:
                term_docs = index[token]
            else:
                term_docs = set()

            if operator == "or":
                result = result | term_docs
            elif operator == "and":
                result = result & term_docs
            elif operator == "not":
                result = result - term_docs

    return result

query = "garden or night"
result = boolean_query(query, inverted_index, set(documents.keys()))

print(f"\nQuery: '{query}'")
print(f"Result: {result}")
for doc_id in result:
    print(f"  {doc_id}: {documents[doc_id]}")
