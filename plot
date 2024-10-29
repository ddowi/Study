import pandas as pd

# 计算各比例
total_orders = len(orders_df)
against_ratio = orders_df['isAgainst'].sum() / total_orders
in_favor_ratio = (orders_df['isAgainst'] == False).sum() / total_orders
no_move_ratio = orders_df['timeInterval'].isna().sum() / total_orders

# 分布情况
against_intervals = orders_df[orders_df['isAgainst'] == True]['timeInterval'].dropna()
in_favor_intervals = orders_df[orders_df['isAgainst'] == False]['timeInterval'].dropna()

against_interval_mean = against_intervals.mean()
against_interval_median = against_intervals.median()
in_favor_interval_mean = in_favor_intervals.mean()
in_favor_interval_median = in_favor_intervals.median()

# 输出分析结果
results = {
    "Against Ratio": against_ratio,
    "In Favor Ratio": in_favor_ratio,
    "No Move Ratio": no_move_ratio,
    "Against Avg Interval": against_interval_mean,
    "Against Median Interval": against_interval_median,
    "In Favor Avg Interval": in_favor_interval_mean,
    "In Favor Median Interval": in_favor_interval_median
}
analysis_df = pd.DataFrame([results])
print(analysis_df)


import matplotlib.pyplot as plt
import pandas as pd

# 假设 orders_df 已存在，包含 `timeInterval`, `isAgainst` 和 `moveSize` 列

# 生成示例数据
data = {
    'timeInterval': [100, 200, 300, None, 800, 150, None, 400, 200, 500, 300, None, 250],
    'isAgainst': [True, False, True, False, True, True, False, False, True, True, False, None, False]
}
orders_df = pd.DataFrame(data)

# 1. Proportion Bar Plot for Against, In Favor, and No Move Ratios
total_orders = len(orders_df)
against_ratio = orders_df['isAgainst'].sum() / total_orders
in_favor_ratio = (orders_df['isAgainst'] == False).sum() / total_orders
no_move_ratio = orders_df['timeInterval'].isna().sum() / total_orders

# Ratios bar plot
plt.figure(figsize=(8, 6))
plt.bar(['Against', 'In Favor', 'No Move'], [against_ratio, in_favor_ratio, no_move_ratio], color=['red', 'green', 'gray'])
plt.title("Proportion of Against, In Favor, and No Move")
plt.ylabel("Ratio")
plt.ylim(0, 1)
plt.show()

# 2. Histogram of `timeInterval` for `Against` and `In Favor`
plt.figure(figsize=(10, 6))
against_intervals = orders_df[orders_df['isAgainst'] == True]['timeInterval'].dropna()
in_favor_intervals = orders_df[orders_df['isAgainst'] == False]['timeInterval'].dropna()

plt.hist(against_intervals, bins=10, alpha=0.7, label="Against", color='red')
plt.hist(in_favor_intervals, bins=10, alpha=0.7, label="In Favor", color='green')
plt.title("Distribution of timeInterval for Against and In Favor")
plt.xlabel("timeInterval (seconds)")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# 3. Box Plot for timeInterval by Against/In Favor
plt.figure(figsize=(8, 6))
orders_df['Outcome'] = orders_df['isAgainst'].map({True: 'Against', False: 'In Favor'})
filtered_df = orders_df.dropna(subset=['timeInterval', 'Outcome'])
filtered_df.boxplot(column='timeInterval', by='Outcome', grid=False)
plt.title("Box Plot of timeInterval by Outcome")
plt.suptitle("")
plt.xlabel("Outcome")
plt.ylabel("timeInterval (seconds)")
plt.show()

# 4. Stacked Bar Chart for Counts by timeInterval Range and Outcome
interval_bins = [0, 300, 600, 900]
orders_df['IntervalRange'] = pd.cut(orders_df['timeInterval'], bins=interval_bins)
interval_outcome_counts = orders_df.groupby(['IntervalRange', 'Outcome']).size().unstack(fill_value=0)

interval_outcome_counts.plot(kind='bar', stacked=True, color=['green', 'red'], figsize=(10, 6))
plt.title("Stacked Bar Chart of Interval Ranges by Outcome")
plt.xlabel("Interval Range (seconds)")
plt.ylabel("Count")
plt.legend(title="Outcome")
plt.show()
