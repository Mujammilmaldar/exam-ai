# Q8A: Precision, Recall, F-Measure (TP=60, FP=30, FN=20)
# Q8B: Evaluation Toolkit for Average Precision

# ========================================
# PART A: Precision, Recall, F-Measure
# ========================================

print("========== Precision, Recall, F-Measure ==========\n")

# Given values
TP = 60   # True Positives
FP = 30   # False Positives
FN = 20   # False Negatives

print(f"True Positives (TP): {TP}")
print(f"False Positives (FP): {FP}")
print(f"False Negatives (FN): {FN}")

# Recall = TP / (TP + FN)
recall = TP / (TP + FN)
print(f"\nRecall = TP / (TP + FN) = {TP} / ({TP} + {FN}) = {TP} / {TP + FN} = {recall:.4f}")

# Precision = TP / (TP + FP)
precision = TP / (TP + FP)
print(f"Precision = TP / (TP + FP) = {TP} / ({TP} + {FP}) = {TP} / {TP + FP} = {precision:.4f}")

# F-Score = 2 * (Precision * Recall) / (Precision + Recall)
f_score = 2 * (precision * recall) / (precision + recall)
print(f"F-Score = 2 * (P * R) / (P + R) = 2 * ({precision:.4f} * {recall:.4f}) / ({precision:.4f} + {recall:.4f}) = {f_score:.4f}")

print(f"\n--- Summary ---")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
print(f"F-Score:   {f_score:.4f} ({f_score*100:.2f}%)")

# ========================================
# PART B: Evaluation Toolkit (Average Precision)
# ========================================

from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    average_precision_score, classification_report
)
import numpy as np

print("\n\n========== Evaluation Toolkit ==========\n")

# Simulated binary classification results
# 1 = relevant, 0 = not relevant
y_true  = [1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1]
y_pred  = [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1]
y_score = [0.9, 0.85, 0.4, 0.3, 0.8, 0.6, 0.2, 0.75, 0.35, 0.1, 0.7, 0.15, 0.55, 0.8, 0.9]

print(f"True labels:      {y_true}")
print(f"Predicted labels:  {y_pred}")
print(f"Prediction scores: {y_score}")

# Calculate metrics
print(f"\nPrecision: {precision_score(y_true, y_pred):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")

# Average Precision
ap = average_precision_score(y_true, y_score)
print(f"Average Precision (AP): {ap:.4f}")

# Detailed classification report
print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=['Not Relevant', 'Relevant']))
