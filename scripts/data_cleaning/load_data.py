# load_data.py

import pandas as pd

# Example: Load housing data
housing = pd.read_csv("../../data/raw/housing.csv")

# Example: Load pollution data
pollution = pd.read_csv("../../data/raw/pollution.csv")

# Preview
print("Housing Data:")
print(housing.head())

print("\nPollution Data:")
print(pollution.head())
