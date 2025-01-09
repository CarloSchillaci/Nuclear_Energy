import pandas as pd

# Load the dataset
df = pd.read_json('/Users/alessiocarnevale/Documents/Coding/SUPSI/Year 2/3rd Semester/Data Visualization/Datasets/nuclear_data.json')

# Ensure the dataset has the necessary columns
if 'Country/Area' not in df.columns or 'Capacity (MW)' not in df.columns:
    raise ValueError("Dataset must include 'Country/Area' and 'Capacity (MW)' columns.")

# Filter out rows with zero or missing capacities
df = df[df['Capacity (MW)'] > 0]

# Group by country and calculate total capacity
df_grouped = df.groupby('Country/Area', as_index=False).agg({
    'Capacity (MW)': 'sum'  # Sum of capacities
}).rename(columns={'Capacity (MW)': 'Capacity (MW)'})  # Rename capacity column for clarity

# Calculate the number of reactors per country
reactor_counts = df.groupby('Country/Area').size().reset_index(name='Active Reactors')

# Merge capacity and reactor counts
final_df = pd.merge(df_grouped, reactor_counts, on='Country/Area')

# Save the reduced dataset to a new JSON file
output_file = 'summed_nuclear_data.json'
final_df.to_json(output_file, orient='records', indent=2)

print(f"Summed capacities and active reactors saved to {output_file}")
