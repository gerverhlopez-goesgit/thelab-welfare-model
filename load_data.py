import os
import requests
import pandas as pd

def fetch_housing_and_pollution(zip_code):
    # 1. Fetch Air Quality (EPA AirNow)
    air_key = os.getenv("AIRNOW_API_KEY")
    air_url = f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zip_code}&API_KEY={air_key}"
    
    # 2. Fetch Housing Value (Census Bureau ACS)
    # B25077_001E is the code for Median Value of Owner-Occupied Housing Units
    census_key = os.getenv("CENSUS_API_KEY")
    census_url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B25077_001E&for=zip%20code%20tabulation%20area:{zip_code}&key={census_key}"

    # Example Logic: In a real run, you'd loop through multiple zip codes
    # For now, we return a single-row DataFrame for your model to process
    return pd.DataFrame({
        'zip': [zip_code],
        'price': [540000],  # This would come from the Census JSON response
        'pm25': [12.4]      # This would come from the AirNow JSON response
    })