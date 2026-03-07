import numpy as np
from scipy.stats import chi2_contingency

# Contingency table
data = np.array([
    [20, 15, 5],
    [10, 25, 10],
    [5, 10, 20]
])

# Chi-Square Test
chi2, p_value, dof, expected = chi2_contingency(data)

print("Chi-square value:", chi2)
print("P-value:", p_value)
print("Degrees of Freedom:", dof)
print("Expected Frequencies:\n", expected)

# Significance level
alpha = 0.05

if p_value < alpha:
    print("Decision: Reject Null Hypothesis")
    print("Conclusion: Aptitude and Job Proficiency are related")
else:
    print("Decision: Fail to Reject Null Hypothesis")
    print("Conclusion: No relationship between Aptitude and Job Proficiency")
