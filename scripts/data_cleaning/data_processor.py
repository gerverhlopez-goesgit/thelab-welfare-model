"""
Data processing and preprocessing for hedonic pricing model.
Handles data cleaning, feature engineering, and train-test splitting.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, List, Optional
from config import HedonicConfig


class DataProcessor:
    """Process and prepare data for modeling."""
    
    def __init__(self, config: HedonicConfig = None):
        """
        Initialize data processor.
        
        Args:
            config: HedonicConfig object with settings
        """
        self.config = config or HedonicConfig()
        self.scaler = None
        self.feature_means = None
        self.feature_stds = None
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded DataFrame
        """
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {len(df)} records from {filepath}")
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate data.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        df = df.copy()
        initial_rows = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['transaction_id'])
        
        # Remove rows with missing prices
        df = df.dropna(subset=['price'])
        
        # Remove outliers (prices that are unrealistic)
        price_q1 = df['price'].quantile(0.01)
        price_q99 = df['price'].quantile(0.99)
        df = df[(df['price'] >= price_q1) & (df['price'] <= price_q99)]
        
        # Remove negative values for non-negative variables
        non_negative_cols = ['sqft', 'bedrooms', 'bathrooms', 'age', 'pm25', 'no2', 
                            'ozone', 'tri_proximity', 'crime_rate']
        for col in non_negative_cols:
            if col in df.columns:
                df = df[df[col] >= 0]
        
        rows_removed = initial_rows - len(df)
        print(f"✓ Data cleaned: {rows_removed} rows removed ({len(df)} rows remain)")
        return df
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create new features for enhanced modeling.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional features
        """
        df = df.copy()
        
        # Price-related features
        if 'price' in df.columns:
            df['log_price'] = np.log(df['price'])
            df['price_per_sqft'] = df['price'] / df['sqft']
        
        # Age-related features
        if 'age' in df.columns:
            df['age_squared'] = df['age'] ** 2
        
        # Environmental composite indices
        if all(col in df.columns for col in ['pm25', 'no2', 'ozone']):
            # Normalize each pollutant to 0-1 scale
            pm25_norm = (df['pm25'] - df['pm25'].min()) / (df['pm25'].max() - df['pm25'].min())
            no2_norm = (df['no2'] - df['no2'].min()) / (df['no2'].max() - df['no2'].min())
            ozone_norm = (df['ozone'] - df['ozone'].min()) / (df['ozone'].max() - df['ozone'].min())
            
            # Air quality index (higher is worse)
            df['air_quality_index'] = (pm25_norm + no2_norm + ozone_norm) / 3
        
        # Environmental risk composite (for exposure analysis)
        if 'tri_proximity' in df.columns and 'flood_zone' in df.columns:
            df['environmental_risk'] = (
                (1 - df['tri_proximity'] / df['tri_proximity'].max()) * 0.5 +
                df['flood_zone'] * 0.5
            )
        
        # Structural quality index
        if all(col in df.columns for col in ['bedrooms', 'bathrooms', 'sqft']):
            df['rooms_per_sqft'] = (df['bedrooms'] + df['bathrooms']) / df['sqft']
            df['structural_quality'] = (
                (df['bedrooms'] / df['bedrooms'].max()) * 0.4 +
                (df['bathrooms'] / df['bathrooms'].max()) * 0.3 +
                ((1 - df['age'] / df['age'].max())) * 0.3  # Newer is better
            )
        
        # Neighborhood quality index
        if all(col in df.columns for col in ['school_rating', 'crime_rate', 'walkability']):
            school_norm = df['school_rating'] / 10
            crime_norm = 1 - (df['crime_rate'] / df['crime_rate'].max())
            walk_norm = df['walkability'] / 10
            df['neighborhood_quality'] = (school_norm * 0.4 + crime_norm * 0.3 + walk_norm * 0.3)
        
        # Time-based features
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['quarter'] = df['date'].dt.quarter
            df['time_period'] = (df['year'] - df['year'].min()) * 4 + df['quarter']
        
        print(f"✓ Created engineered features: {len(df.columns)} total columns")
        return df
    
    def prepare_for_modeling(self, df: pd.DataFrame, 
                            target_col: str = 'price') -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for model training.
        
        Args:
            df: Input DataFrame
            target_col: Name of target variable
            
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        df = df.copy()
        
        # Select features
        all_features = (self.config.structural_features + 
                       self.config.neighborhood_features + 
                       self.config.environmental_features)
        
        # Keep only features that exist in data
        available_features = [f for f in all_features if f in df.columns]
        
        X = df[available_features].copy()
        y = df[target_col].copy()
        
        if self.config.use_log_price and target_col == 'price':
            y = np.log(y)
        
        # Handle any remaining missing values
        X = X.fillna(X.mean())
        
        print(f"✓ Prepared {len(X)} samples with {len(X.columns)} features")
        return X, y
    
    def standardize_features(self, X_train: pd.DataFrame, 
                            X_test: pd.DataFrame = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Standardize features using training data.
        
        Args:
            X_train: Training features
            X_test: Optional test features
            
        Returns:
            Tuple of (scaled_train, scaled_test or None)
        """
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        X_test_scaled = None
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
        
        print(f"✓ Features standardized (mean=0, std=1)")
        return X_train_scaled, X_test_scaled
    
    def train_test_split_data(self, X: pd.DataFrame, y: pd.Series, 
                             test_size: float = None, 
                             random_state: int = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into train and test sets with optional standardization.
        
        Args:
            X: Features DataFrame
            y: Target Series
            test_size: Proportion for test set
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test) - standardized if configured
        """
        test_size = test_size or self.config.test_size
        random_state = random_state or self.config.random_state
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        if self.config.standardize_features:
            X_train_scaled, X_test_scaled = self.standardize_features(X_train, X_test)
            print(f"✓ Split into train ({len(X_train)}) / test ({len(X_test)}) with standardization")
            return X_train_scaled, X_test_scaled, y_train.values, y_test.values
        else:
            print(f"✓ Split into train ({len(X_train)}) / test ({len(X_test)})")
            return X_train.values, X_test.values, y_train.values, y_test.values
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get categorized feature lists."""
        return {
            'structural': self.config.structural_features,
            'neighborhood': self.config.neighborhood_features,
            'environmental': self.config.environmental_features
        }


def process_pipeline(df: pd.DataFrame, 
                    config: HedonicConfig = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Complete data processing pipeline.
    
    Args:
        df: Raw DataFrame
        config: HedonicConfig object
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, processed_df)
    """
    config = config or HedonicConfig()
    processor = DataProcessor(config)
    
    # Pipeline steps
    df = processor.clean_data(df)
    df = processor.create_features(df)
    X, y = processor.prepare_for_modeling(df)
    X_train, X_test, y_train, y_test = processor.train_test_split_data(X, y)
    
    return X_train, X_test, y_train, y_test, df


if __name__ == "__main__":
    from data_generation import create_sample_data
    from config import HedonicConfig
    
    # Generate and process sample data
    print("Generating sample data...")
    df = create_sample_data(n_samples=1000)
    
    print("\n" + "="*60)
    print("PROCESSING DATA")
    print("="*60 + "\n")
    
    config = HedonicConfig()
    processor = DataProcessor(config)
    
    df = processor.clean_data(df)
    df = processor.create_features(df)
    X, y = processor.prepare_for_modeling(df)
    X_train, X_test, y_train, y_test = processor.train_test_split_data(X, y)
    
    print(f"\nTrain set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    print(f"\nFirst 5 training samples (standardized):")
    print(X_train[:5])
