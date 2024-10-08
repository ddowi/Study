import pandas as pd
import numpy as np
from scipy.stats import norm

# Create example DataFrame
data = {
    'col1': ['A', 'A', 'B', 'B'],
    'col2': ['X', 'X', 'Y', 'Y'],
    'list_col': [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
    'notional': [0.2, 0.8, 0.5, 1.5]  # The weight for each row
}

df = pd.DataFrame(data)

# Z-score for 95% confidence level
z = norm.ppf(0.975)  # For two-tailed 95% CI

# Define a function to compute weighted mean, std and confidence interval of lists
def weighted_mean_and_ci(list_series, weights):
    # Convert lists to numpy arrays
    lists_array = np.array(list_series.tolist())
    weights_array = np.array(weights)
    
    # Compute weighted mean
    weighted_avg = np.average(lists_array, axis=0, weights=weights_array)
    
    # Compute weighted standard deviation
    weighted_var = np.average((lists_array - weighted_avg)**2, axis=0, weights=weights_array)
    weighted_std = np.sqrt(weighted_var)
    
    # Compute standard error
    n = len(weights_array)  # Number of samples in the group
    standard_error = weighted_std / np.sqrt(n)
    
    # Compute confidence interval (mean +/- Z * standard error)
    ci_lower = weighted_avg - z * standard_error
    ci_upper = weighted_avg + z * standard_error
    
    return weighted_avg, (ci_lower, ci_upper)

# Group by col1 and col2, and compute weighted mean and confidence interval for list_col
df_grouped = df.groupby(['col1', 'col2']).apply(
    lambda group: weighted_mean_and_ci(group['list_col'], group['notional'])
).reset_index(name='weighted_mean_and_ci')

# Separate the weighted mean and confidence interval into separate columns
df_grouped['weighted_mean'] = df_grouped['weighted_mean_and_ci'].apply(lambda x: x[0])
df_grouped['ci_lower'] = df_grouped['weighted_mean_and_ci'].apply(lambda x: x[1][0])
df_grouped['ci_upper'] = df_grouped['weighted_mean_and_ci'].apply(lambda x: x[1][1])

# Drop the intermediate column
df_grouped = df_grouped.drop(columns=['weighted_mean_and_ci'])

# Output the result
print(df_grouped)
