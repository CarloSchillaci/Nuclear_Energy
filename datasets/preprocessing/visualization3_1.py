import numpy as np
import pandas as pd

# Half-lives of isotopes (in days)
half_lives = {
    "Iodine-131": 8,          # 8 days
    "Caesium-134": 730,       # 2 years
    "Caesium-137": 10950      # 30 years
}

# Generate time points that are multiples of 10 from 0 to 50,000 days
time = np.arange(0, 50001, 10) 

# Calculate the fraction remaining for each isotope
data = {
    "Time (days)": time,
    "Iodine-131 (Fraction Remaining)": np.exp(-np.log(2) * time / half_lives["Iodine-131"]),
    "Caesium-134 (Fraction Remaining)": np.exp(-np.log(2) * time / half_lives["Caesium-134"]),
    "Caesium-137 (Fraction Remaining)": np.exp(-np.log(2) * time / half_lives["Caesium-137"]),
}

# Create a pandas DataFrame
decay_df = pd.DataFrame(data)

# Reshape the dataset into the desired format with isotopes as rows and time as columns
reshaped_data = decay_df.set_index("Time (days)").T
reshaped_data.index = ["Iodine-131", "Caesium-134", "Caesium-137"]
reshaped_data.columns = reshaped_data.columns.astype(int)

# Reset index and save the result
reshaped_data.reset_index(inplace=True)
reshaped_data.rename(columns={"index": "Isotope"}, inplace=True)

# Save the dataset to a CSV file
file_path = "decay_curves_isotopes.csv"
reshaped_data.to_csv(file_path, index=False)

print(f"Dataset saved to {file_path}")