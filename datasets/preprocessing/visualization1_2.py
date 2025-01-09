import pandas as pd

# Load your dataset
df = pd.read_csv('/Users/alessiocarnevale/Documents/Coding/SUPSI/Year 2/3rd Semester/Data Visualization/Datasets/Global-Nuclear-Power-Tracker-July-2024 1(Data).csv', delimiter=';', encoding='Windows-1252')

# Filter the dataset for reactors with status 'operating'
df_operating = df[df['Status'] == 'operating']

# Select only the necessary columns
df_subset = df_operating[['Country/Area', 'Capacity (MW)']]

# Convert to JSON
json_data = df_subset.to_json(orient='records')

# Save to a file
with open('nuclear_data.json', 'w') as f:
    f.write(json_data)

# Find the lowest 'start year' in the dataset
lowest_start_year = df['Start Year'].min()  # Assuming 'Start Year' is the correct column name
print(lowest_start_year)