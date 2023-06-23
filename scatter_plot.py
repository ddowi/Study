import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def plot_regression(X, Y):
    # Create DataFrame from series
    data = pd.DataFrame({'X': X, 'Y': Y})

    # Calculate 2.5% and 97.5% quantiles
    lower_quantile = data['Y'].quantile(0.025)
    upper_quantile = data['Y'].quantile(0.975)

    # Classify data into normal and outliers
    data['Type'] = 'normal'
    data.loc[data['Y'] < lower_quantile, 'Type'] = 'outlier'
    data.loc[data['Y'] > upper_quantile, 'Type'] = 'outlier'

    # Fit regression models
    slope, intercept, r_value, p_value, std_err = stats.linregress(data[data['Type'] == 'normal']['X'], data[data['Type'] == 'normal']['Y'])
    slope_out, intercept_out, r_value_out, p_value_out, std_err_out = stats.linregress(data[data['Type'] == 'outlier']['X'], data[data['Type'] == 'outlier']['Y'])

    # Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='X', y='Y', hue='Type', data=data)

    x_vals = np.array(data['X'])
    y_vals = intercept + slope * x_vals
    y_vals_out = intercept_out + slope_out * x_vals

    plt.plot(x_vals, y_vals, '--', color='blue')
    plt.plot(x_vals, y_vals_out, '--', color='red')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scatter plot with regression lines')

    plt.show()