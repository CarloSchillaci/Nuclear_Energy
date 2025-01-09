import pandas as pd

# Load the CSV file
file_path = '/mnt/data/yearly_full_release_long_format.csv'
df = pd.read_csv(file_path)

# Filter for 'Electricity generation' in the 'Category' column and 'Nuclear' in the 'Variable' column
df_filtered = df[(df['Category'] == 'Electricity generation') & (df['Variable'] == 'Nuclear')]

# Group by Country and Year, summing the values
df_grouped = df_filtered.groupby(['Country', 'Year'])['Value'].sum().reset_index()

# Pivot to make Year columns and Country rows
df_pivot = df_grouped.pivot(index='Country', columns='Year', values='Value')

# Save the result to a CSV file or display it
df_pivot.to_csv('/mnt/data/electricity_generation_nuclear_pivot.csv')
print(df_pivot)