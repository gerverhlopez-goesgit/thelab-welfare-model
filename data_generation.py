"""
Synthetic data generation for hedonic pricing model.
Creates realistic property transaction data with structural, neighborhood, and environmental characteristics.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from config import DataConfig


class SyntheticDataGenerator:
    """Generate synthetic real estate transaction data."""
    
    def __init__(self, config: DataConfig = None):
        """
        Initialize data generator.
        
        Args:
            config: DataConfig object with parameters
        """
        self.config = config or DataConfig()
        np.random.seed(self.config.random_seed)
    
    def generate(self) -> pd.DataFrame:
        """
        Generate complete synthetic dataset.
        
        Returns:
            DataFrame with property transactions
        """
        n = self.config.n_samples
        
        df = pd.DataFrame()
        
        # Transaction metadata
        df['transaction_id'] = range(1, n + 1)
        df['date'] = self._generate_dates(n)
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        
        # Geographic/administrative
        df['region'] = np.random.choice(range(1, self.config.num_regions + 1), n)
        df['latitude'] = np.random.uniform(39.5, 41.5, n)
        df['longitude'] = np.random.uniform(-74.5, -72.5, n)
        
        # STRUCTURAL CHARACTERISTICS
        df['sqft'] = np.random.normal(self.config.sqft_mean, self.config.sqft_std, n)
        df['sqft'] = df['sqft'].clip(lower=500)
        
        df['bedrooms'] = np.random.normal(self.config.bedrooms_mean, self.config.bedrooms_std, n)
        df['bedrooms'] = np.round(df['bedrooms']).astype(int).clip(lower=1, upper=10)
        
        df['bathrooms'] = np.random.normal(self.config.bathrooms_mean, self.config.bathrooms_std, n)
        df['bathrooms'] = np.round(df['bathrooms'], 1).clip(lower=0.5, upper=6)
        
        df['age'] = np.random.normal(self.config.age_mean, self.config.age_std, n)
        df['age'] = np.round(df['age']).astype(int).clip(lower=1, upper=100)
        
        # NEIGHBORHOOD CHARACTERISTICS
        df['school_rating'] = np.random.normal(self.config.school_rating_mean, 
                                               self.config.school_rating_std, n)
        df['school_rating'] = df['school_rating'].clip(lower=1, upper=10)
        
        df['crime_rate'] = np.random.normal(self.config.crime_rate_mean, 
                                            self.config.crime_rate_std, n)
        df['crime_rate'] = df['crime_rate'].clip(lower=0)
        
        df['walkability'] = np.random.normal(self.config.walkability_mean, 
                                             self.config.walkability_std, n)
        df['walkability'] = df['walkability'].clip(lower=1, upper=10)
        
        # ENVIRONMENTAL CHARACTERISTICS
        df['pm25'] = np.random.normal(self.config.pm25_mean, self.config.pm25_std, n)
        df['pm25'] = df['pm25'].clip(lower=0)
        
        df['no2'] = np.random.normal(self.config.no2_mean, self.config.no2_std, n)
        df['no2'] = df['no2'].clip(lower=0)
        
        df['ozone'] = np.random.normal(self.config.ozone_mean, self.config.ozone_std, n)
        df['ozone'] = df['ozone'].clip(lower=0)
        
        df['tri_proximity'] = np.random.exponential(self.config.tri_proximity_mean, n)
        
        df['flood_zone'] = np.random.binomial(1, self.config.flood_zone_probability, n)
        
        # SHOCK VARIABLE (for DiD analysis)
        df['treated'] = (df['region'].isin([3, 4])).astype(int)  # Some regions treated
        df['post_shock'] = (df['year'] >= self.config.shock_year).astype(int)
        df['did_interaction'] = df['treated'] * df['post_shock']
        
        # WIND PATTERN (for IV analysis) - synthetic instrument
        df['wind_pattern'] = np.random.uniform(-1, 1, n)  # -1 (southwesterly) to 1 (northeasterly)
        
        # DISTANCE FROM FREEWAY (for RDD analysis)
        df['distance_from_freeway'] = np.random.exponential(2.0, n)
        
        # PRICE (dependent variable)
        # Hedonic equation with realistic coefficients
        df['price'] = self._calculate_price(df)
        
        return df.sort_values('date').reset_index(drop=True)
    
    def _generate_dates(self, n: int) -> pd.Series:
        """Generate random transaction dates over 10 years."""
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2020, 12, 31)
        date_range = (end_date - start_date).days
        
        random_days = np.random.randint(0, date_range, n)
        dates = [start_date + timedelta(days=int(d)) for d in random_days]
        return pd.Series(dates)
    
    def _calculate_price(self, df: pd.DataFrame) -> np.ndarray:
        """
        Calculate property price based on hedonic equation.
        
        ln(P) = β0 + β1*sqft + β2*bedrooms + β3*bathrooms + β4*age
                + γ1*school_rating + γ2*crime_rate + γ3*walkability
                + δ1*pm25 + δ2*no2 + δ3*ozone + δ4*tri_proximity + δ5*flood_zone
                + shock_effect + ε
        """
        n = len(df)
        
        # Base price (intercept)
        log_price = 12.0  # ln(P) ≈ 12 → P ≈ $162,000
        
        # STRUCTURAL COEFFICIENTS
        log_price += 0.0003 * df['sqft']  # $300/sqft (β1)
        log_price += 0.15 * df['bedrooms']  # ~15% per bedroom (β2)
        log_price += 0.10 * df['bathrooms']  # ~10% per bathroom (β3)
        log_price += -0.01 * df['age']  # -1% per year of age (β4)
        
        # NEIGHBORHOOD COEFFICIENTS
        log_price += 0.08 * df['school_rating']  # ~8% per point (γ1)
        log_price += -0.05 * df['crime_rate']  # -5% per unit crime increase (γ2)
        log_price += 0.05 * df['walkability']  # ~5% per walkability point (γ3)
        
        # ENVIRONMENTAL COEFFICIENTS (THE KEY ONES)
        log_price += -0.03 * df['pm25']  # -3% per µg/m³ (δ1) - HEALTH PENALTY
        log_price += -0.005 * df['no2']  # -0.5% per ppb (δ2) - TRAFFIC PENALTY
        log_price += -0.004 * df['ozone']  # -0.4% per ppb (δ3) - AIR QUALITY PENALTY
        log_price += -0.05 / (df['tri_proximity'] + 0.1)  # Proximity penalty (δ4)
        log_price += -0.20 * df['flood_zone']  # -20% if in flood zone (δ5)
        
        # SHOCK EFFECT (DiD treatment effect)
        shock_effect = -self.config.shock_intensity * df['did_interaction']
        log_price += shock_effect
        
        # Random error term
        epsilon = np.random.normal(0, 0.15, n)  # 15% error term
        log_price += epsilon
        
        # Convert from log to actual price
        price = np.exp(log_price)
        
        return price
    
    def generate_and_save(self, filepath: str) -> pd.DataFrame:
        """
        Generate data and save to CSV.
        
        Args:
            filepath: Path to save CSV file
            
        Returns:
            Generated DataFrame
        """
        df = self.generate()
        df.to_csv(filepath, index=False)
        print(f"✓ Generated {len(df)} synthetic transactions and saved to {filepath}")
        return df


def create_sample_data(n_samples: int = 1000, filepath: str = None) -> pd.DataFrame:
    """
    Convenience function to quickly generate sample data.
    
    Args:
        n_samples: Number of samples to generate
        filepath: Optional path to save to CSV
        
    Returns:
        Generated DataFrame
    """
    config = DataConfig(n_samples=n_samples)
    generator = SyntheticDataGenerator(config)
    
    if filepath:
        return generator.generate_and_save(filepath)
    else:
        return generator.generate()


if __name__ == "__main__":
    # Example usage
    config = DataConfig(n_samples=1000)
    generator = SyntheticDataGenerator(config)
    
    df = generator.generate_and_save('data/synthetic_properties.csv')
    
    print("\n" + "="*60)
    print("SYNTHETIC DATA SUMMARY")
    print("="*60)
    print(f"\nShape: {df.shape}")
    print(f"\nPrice Statistics:")
    print(df['price'].describe())
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nFirst few rows:\n{df.head()}")
