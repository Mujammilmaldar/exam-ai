# Q10A: Naive Bayes Classifier on 20 Newsgroups
# Q10B: SVM Classifier on 20 Newsgroups

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ========================================
# PART A: Naive Bayes Classifier
# ========================================

from sklearn.naive_bayes import MultinomialNB

print("========== Naive Bayes on 20 Newsgroups ==========\n")

# Load dataset
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

print(f"Categories: {categories}")
newsgroups = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

print(f"Total documents: {len(newsgroups.data)}")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(newsgroups.data)
y = newsgroups.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training: {X_train.shape[0]} | Testing: {X_test.shape[0]}")

# Train Naive Bayes
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Evaluate
y_pred_nb = nb_model.predict(X_test)
print(f"\nNaive Bayes Accuracy: {accuracy_score(y_test, y_pred_nb):.4f}")
print("\nClassification Report (Naive Bayes):")
print(classification_report(y_test, y_pred_nb, target_names=newsgroups.target_names))

# ========================================
# PART B: SVM Classifier
# ========================================

from sklearn.svm import LinearSVC

print("\n========== SVM on 20 Newsgroups ==========\n")

# Train SVM
svm_model = LinearSVC(random_state=42, max_iter=10000)
svm_model.fit(X_train, y_train)

# Evaluate
y_pred_svm = svm_model.predict(X_test)
print(f"SVM Accuracy: {accuracy_score(y_test, y_pred_svm):.4f}")
print("\nClassification Report (SVM):")
print(classification_report(y_test, y_pred_svm, target_names=newsgroups.target_names))

# ========================================
# Comparison
# ========================================

print("\n========== Comparison ==========")
print(f"Naive Bayes Accuracy: {accuracy_score(y_test, y_pred_nb):.4f}")
print(f"SVM Accuracy:         {accuracy_score(y_test, y_pred_svm):.4f}")

winner = "SVM" if accuracy_score(y_test, y_pred_svm) > accuracy_score(y_test, y_pred_nb) else "Naive Bayes"
print(f"Better model: {winner}")
