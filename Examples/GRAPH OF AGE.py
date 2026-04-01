import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file
data = pd.read_csv(r'D:\c\csv1.csv')

# Create age group ranges
age_ranges = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']

# Categorize passengers by age group
data['age_group'] = pd.cut(data['age'], bins=range(0, 101, 10), right=False, labels=age_ranges)

# Count occurrences of each age group
age_counts = data['age_group'].value_counts().sort_index()

# Plot the data
ages = list(age_counts.index)
counts = list(age_counts.values)

plt.bar(ages, counts, align='center',color='r')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.title('Count of Passengers by Age Group')
plt.show()
