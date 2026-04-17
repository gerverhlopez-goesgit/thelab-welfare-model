"""
Configuration and parameter settings for the hedonic pricing model.
This file centralizes all tunable parameters for data generation and analysis.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict

@dataclass
class DataConfig:
    """Configuration for synthetic data generation."""
    
    n_samples: int = 1000  # Number of property transactions
    random_seed: int = 42
    
    # Structural characteristics ranges
    sqft_mean: float = 2000
    sqft_std: float = 600
    bedrooms_mean: float = 3
    bedrooms_std: float = 1
    bathrooms_mean: float = 2
    bathrooms_std: float = 0.8
    age_mean: float = 30  # years
    age_std: float = 25
    
    # Neighborhood characteristics ranges
    school_rating_mean: float = 7.0  # 1-10 scale
    school_rating_std: float = 2.0
    crime_rate_mean: float = 5.0  # per 1000 residents
    crime_rate_std: float = 3.0
    walkability_mean: float = 6.0  # 1-10 scale
    walkability_std: float = 2.5
    
    # Environmental characteristics ranges
    pm25_mean: float = 12.0  # µg/m³
    pm25_std: float = 4.0
    no2_mean: float = 35.0  # ppb
    no2_std: float = 15.0
    ozone_mean: float = 45.0  # ppb
    ozone_std: float = 15.0
    tri_proximity_mean: float = 5.0  # km from nearest TRI site
    tri_proximity_std: float = 3.0
    flood_zone_probability: float = 0.15  # 15% in flood zone
    
    # Geographic/shock variables
    num_regions: int = 5
    shock_year: int = 2015  # Year of environmental shock
    shock_intensity: float = 0.2  # 20% price penalty post-shock

@dataclass
class HedonicConfig:
    """Configuration for hedonic model estimation."""
    
    use_log_price: bool = True
    test_size: float = 0.2
    random_state: int = 42
    standardize_features: bool = True
    
    # Feature sets
    structural_features: list = None
    neighborhood_features: list = None
    environmental_features: list = None
    
    def __post_init__(self):
        if self.structural_features is None:
            self.structural_features = ['sqft', 'bedrooms', 'bathrooms', 'age']
        if self.neighborhood_features is None:
            self.neighborhood_features = ['school_rating', 'crime_rate', 'walkability']
        if self.environmental_features is None:
            self.environmental_features = ['pm25', 'no2', 'ozone', 'tri_proximity', 'flood_zone']

@dataclass
class EconometricConfig:
    """Configuration for econometric methods."""
    
    # Difference-in-Differences
    did_treatment_year: int = 2015
    did_bandwidth: float = 2.0  # Years before/after shock
    
    # Regression Discontinuity
    rdd_cutoff: float = 2.5  # km distance to TRI site (treatment threshold)
    rdd_bandwidth: float = 1.0  # km bandwidth around cutoff
    rdd_polynomial: int = 1  # 1 for linear, 2 for quadratic
    
    # Instrumental Variables
    iv_use_wind_pattern: bool = True
    iv_distance_threshold: float = 5.0  # km from freeway
    
    # Statistical settings
    robust_se: bool = True  # Use robust standard errors
    cluster_var: str = 'region'  # Variable to cluster standard errors
    confidence_level: float = 0.95


class APIConfig:
    """Configuration for external API connections (for future use)."""
    
    # EPA API
    EPA_BASE_URL: str = "https://api.epa.gov/api/"
    EPA_KEY: str = None  # To be set from environment
    
    # Zillow API
    ZILLOW_BASE_URL: str = "https://api.zillow.com/api/"
    ZILLOW_KEY: str = None
    
    # TRI Database
    TRI_BASE_URL: str = "https://www.epa.gov/enviro/tri_query_api"
    TRI_KEY: str = None


# Default configurations
DEFAULT_DATA_CONFIG = DataConfig()
DEFAULT_HEDONIC_CONFIG = HedonicConfig()
DEFAULT_ECONOMETRIC_CONFIG = EconometricConfig()
DEFAULT_API_CONFIG = APIConfig()