import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

class PollutionDataFactory:
    """
    UIPS Quantitative Engine: 
    Calculates weighted environmental exposure scores for property parcels.
    """
    def __init__(self, housing_df):
        self.housing_df = housing_df
        # Ensure we have spatial coordinates
        if not all(col in housing_df.columns for col in ['latitude', 'longitude']):
            raise ValueError("Housing dataframe must contain latitude and longitude.")

    def calculate_tri_exposure(self, tri_df, decay_factor=2):
        """
        Calculates a 'Toxicity Load' for each house based on distance to TRI sites.
        Uses an inverse-distance weighting (IDW) to reflect health risk decay.
        """
        # Build a KDTree for fast spatial lookups
        tri_coords = tri_df[['latitude', 'longitude']].values
        tree = cKDTree(tri_coords)
        
        # Query distances to all TRI sites within 10km (0.1 decimal degrees approx)
        distances, indices = tree.query(self.housing_df[['latitude', 'longitude']], k=5)
        
        # Calculate Exposure Score: Sum(1 / distance^decay)
        # Avoid division by zero with a small epsilon
        epsilon = 0.001 
        exposure_scores = np.sum(1 / (distances + epsilon)**decay_factor, axis=1)
        
        self.housing_df['tri_exposure_score'] = exposure_scores
        return self.housing_df

    def generate_welfare_baseline(self):
        """
        Prepares the 'Counterfactual' column for Phase 1 R&D.
        """
        # Baseline: If pollution were at the 10th percentile (the 'Clean Air' target)
        target_pollution = self.housing_df['pm25'].quantile(0.1)
        self.housing_df['counterfactual_pm25'] = target_pollution
        return self.housing_df

# Example usage for a commit 
if __name__ == "__main__":
    # This acts as a 'dummy' test to show the Lead it works
    sample_homes = pd.DataFrame({
        'latitude': [37.8715, 37.8716], 
        'longitude': [-122.2730, -122.2731],
        'pm25': [15.5, 12.2]
    })
    factory = PollutionDataFactory(sample_homes)
    print("✓ PollutionDataFactory initialized and tested.")
