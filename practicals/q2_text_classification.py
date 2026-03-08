# Q2A: Text Classification Algorithm
# Q2B: Train classifier on labeled dataset and evaluate

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ========================================
# PART A & B: Text Classification using Naive Bayes
# ========================================

# Load dataset (4 categories)
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

print("Loading 20 Newsgroups dataset...")
newsgroups = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

print(f"Total documents: {len(newsgroups.data)}")
print(f"Categories: {newsgroups.target_names}")

# Convert text to TF-IDF features
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(newsgroups.data)
y = newsgroups.target

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# Train Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=newsgroups.target_names))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Test with custom text
print("\n========== Custom Text Classification ==========")
test_texts = [
    "God created the universe and everything in it",
    "The patient needs surgery for heart disease",
    "OpenGL rendering and 3D graphics programming"
]

test_vectors = vectorizer.transform(test_texts)
predictions = model.predict(test_vectors)

for text, pred in zip(test_texts, predictions):
    print(f"Text: '{text[:50]}...'")
    print(f"Category: {newsgroups.target_names[pred]}\n")
