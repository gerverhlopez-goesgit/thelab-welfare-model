import requests
import pandas as pd

def fetch_air_quality(zip_code, api_key):
    url = f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zip_code}&API_KEY={api_key}"
    response = requests.get(url)
    return response.json()

# You would then pass this real data into your HedonicPricingModel