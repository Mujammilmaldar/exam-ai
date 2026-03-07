import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Data
group2 = np.array([85, 95, 100, 80, 90, 97, 104, 95, 88, 92, 94, 99])
group3 = np.array([83, 85, 96, 92, 100, 104, 94, 95, 88, 90, 93, 94])

# Significance level
alpha = 0.05

# Two Sample T-Test
t_stat, p_value = stats.ttest_ind(group2, group3)

print("T-statistic:", t_stat)
print("P-value:", p_value)

# Decision
if p_value < alpha:
    print("Decision: Reject Null Hypothesis (H0)")
    print("Conclusion: Significant difference exists between the two groups")
else:
    print("Decision: Fail to Reject Null Hypothesis (H0)")
    print("Conclusion: No significant difference exists between the two groups")

# Plot
plt.figure()
plt.boxplot([group2, group3], tick_labels=["Group 1 (0-1 yr)", "Group 2 (1+ yr)"])
plt.title("Two Sample T-Test - Group Comparison")
plt.ylabel("Values")
plt.show()
