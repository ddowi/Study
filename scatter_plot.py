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


    def backtest(df, col_signal, col_price):
    """
    df: DataFrame that contains the data
    col_signal: Name of the column that contains the trading signals
    col_price: Name of the column that contains the price data
    """
    # Initialize variables
    position = 0  # 1 if we currently hold a position, 0 otherwise
    buy_price = 0  # Price at which we bought in
    equity = []  # Equity curve

    # Iterate over the DataFrame
    for i, row in df.iterrows():
        signal = row[col_signal]
        price = row[col_price]
        if signal == 1 and position == 0:  # Buy
            position = 1
            buy_price = price
        elif signal == -1 and position == 1:  # Sell
            position = 0
            equity.append(price - buy_price)
        elif position == 1:  # Holding
            equity.append(price - buy_price)
        else:  # Nothing
            equity.append(0)
            
    # Convert the equity curve into a Series and add it to the DataFrame
    equity_series = pd.Series(equity, index=df.index, name='equity')
    df = pd.concat([df, equity_series], axis=1)

    return df

# Use the backtest function
df = backtest(df, 'predictions', 'weighted_mid_price')

# Plot the equity curve
df['equity'].cumsum().plot()
