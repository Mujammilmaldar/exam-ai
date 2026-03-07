import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Student scores
scores = np.array([72, 88, 64, 74, 67, 79, 85, 75, 89, 77])

# Hypothesized population mean
mu = 78

# Significance level
alpha = 0.05

# Calculate sample mean
sample_mean = np.mean(scores)

# One Sample T-Test
t_stat, p_value = stats.ttest_1samp(scores, mu)

print("Sample Mean:", sample_mean)
print("T-statistic:", t_stat)
print("P-value:", p_value)

# Decision
if p_value < alpha:
    print("Decision: Reject Null Hypothesis (H0)")
    print("Conclusion: Mean student score is significantly different from 78")
else:
    print("Decision: Fail to Reject Null Hypothesis (H0)")
    print("Conclusion: Mean student score is not significantly different from 78")

# Plot scores (optional - include only if question asks to draw/plot)
# plt.hist(scores, bins=5, edgecolor='black')
# plt.axvline(mu, color='red', linestyle='--', label=f'Hypothesized Mean = {mu}')
# plt.axvline(sample_mean, color='green', linestyle='--', label=f'Sample Mean = {sample_mean:.2f}')
# plt.xlabel('Scores')
# plt.ylabel('Frequency')
# plt.title('One Sample T-Test - Score Distribution')
# plt.legend()
# plt.show()
