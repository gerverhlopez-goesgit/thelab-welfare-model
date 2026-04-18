"""
Hedonic pricing model implementation.
Core regression models for property valuation analysis.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import Dict, Tuple, Optional
from config import HedonicConfig


class HedonicPricingModel:
    """
    Hedonic pricing model for real estate valuation.
    
    The hedonic pricing equation:
    ln(P) = β₀ + Σ(βᵢSᵢ) + Σ(γⱼNⱼ) + Σ(δₖEₖ) + ε
    
    Where:
    - P = Property price
    - Sᵢ = Structural characteristics
    - Nⱼ = Neighborhood characteristics
    - Eₖ = Environmental characteristics
    - ε = Error term
    """
    
    def __init__(self, config: HedonicConfig = None):
        """
        Initialize hedonic model.
        
        Args:
            config: HedonicConfig object
        """
        self.config = config or HedonicConfig()
        self.sklearn_model = None
        self.statsmodels_result = None
        self.feature_names = None
        self.feature_categories = None
        self.coefficients = None
        self.predictions = None
        self.residuals = None
    
    def fit_sklearn(self, X_train: np.ndarray, y_train: np.ndarray, 
                   feature_names: list = None) -> 'HedonicPricingModel':
        """
        Fit model using scikit-learn LinearRegression.
        
        Args:
            X_train: Training features
            y_train: Training target (log-transformed)
            feature_names: List of feature names
            
        Returns:
            Self for method chaining
        """
        self.sklearn_model = LinearRegression()
        self.sklearn_model.fit(X_train, y_train)
        self.feature_names = feature_names or [f"Feature_{i}" for i in range(X_train.shape[1])]
        
        print(f"✓ Model fitted (sklearn)")
        print(f"  Intercept: {self.sklearn_model.intercept_:.4f}")
        print(f"  R² (training): {self.sklearn_model.score(X_train, y_train):.4f}")
        
        return self
    
    def fit_statsmodels(self, X_train: np.ndarray, y_train: np.ndarray, 
                       feature_names: list = None) -> 'HedonicPricingModel':
        """
        Fit model using statsmodels OLS for statistical inference.
        
        Args:
            X_train: Training features
            y_train: Training target (log-transformed)
            feature_names: List of feature names
            
        Returns:
            Self for method chaining
        """
        # Add constant for intercept
        X_train_with_const = sm.add_constant(X_train)
        
        # Fit OLS model
        model = sm.OLS(y_train, X_train_with_const)
        self.statsmodels_result = model.fit()
        
        self.feature_names = feature_names or [f"Feature_{i}" for i in range(X_train.shape[1])]
        
        print(f"✓ Model fitted (statsmodels OLS)")
        print(f"\n{self.statsmodels_result.summary()}")
        
        return self
    
    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Make predictions on test data.
        
        Args:
            X_test: Test features
            
        Returns:
            Predicted log-prices
        """
        if self.sklearn_model is None:
            raise ValueError("Model must be fitted first using fit_sklearn() or fit_statsmodels()")
        
        self.predictions = self.sklearn_model.predict(X_test)
        return self.predictions
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance on test set.
        
        Args:
            X_test: Test features
            y_test: Test target (log-transformed)
            
        Returns:
            Dictionary of evaluation metrics
        """
        predictions = self.predict(X_test)
        self.residuals = y_test - predictions
        
        metrics = {
            'r2_score': r2_score(y_test, predictions),
            'rmse': np.sqrt(mean_squared_error(y_test, predictions)),
            'mae': mean_absolute_error(y_test, predictions),
            'mean_residual': np.mean(self.residuals),
            'std_residual': np.std(self.residuals)
        }
        
        print("\n" + "="*60)
        print("MODEL EVALUATION METRICS")
        print("="*60)
        print(f"R² Score: {metrics['r2_score']:.4f}")
        print(f"RMSE: {metrics['rmse']:.4f}")
        print(f"MAE: {metrics['mae']:.4f}")
        print(f"Mean Residual: {metrics['mean_residual']:.6f}")
        print(f"Std Residual: {metrics['std_residual']:.4f}")
        
        return metrics
    
    def get_coefficients(self) -> pd.DataFrame:
        """
        Extract and return model coefficients.
        
        Returns:
            DataFrame with feature names and coefficients
        """
        if self.sklearn_model is None:
            raise ValueError("Model must be fitted first")
        
        coef_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Coefficient': self.sklearn_model.coef_,
            'Abs_Coefficient': np.abs(self.sklearn_model.coef_)
        })
        
        # Add statsmodels info if available
        if self.statsmodels_result is not None:
            coef_df['P_Value'] = self.statsmodels_result.pvalues[1:]  # Skip constant
            coef_df['Std_Error'] = self.statsmodels_result.bse[1:]
            coef_df['T_Statistic'] = self.statsmodels_result.tvalues[1:]
            coef_df['Significant'] = coef_df['P_Value'] < 0.05
        
        coef_df = coef_df.sort_values('Abs_Coefficient', ascending=False)
        
        print("\n" + "="*60)
        print("MODEL COEFFICIENTS")
        print("="*60)
        print(coef_df.to_string(index=False))
        
        self.coefficients = coef_df
        return coef_df
    
    def get_environmental_coefficients(self, env_features: list = None) -> pd.DataFrame:
        """
        Extract environmental feature coefficients specifically.
        
        Args:
            env_features: List of environmental feature names
            
        Returns:
            DataFrame of environmental coefficients with interpretation
        """
        if self.coefficients is None:
            self.get_coefficients()
        
        env_features = env_features or self.config.environmental_features
        
        env_coef = self.coefficients[self.coefficients['Feature'].isin(env_features)].copy()
        
        # Add interpretation
        def interpret_coef(coef: float) -> str:
            if coef < -0.02:
                return "Strong Negative Impact (Value Penalty)"
            elif coef < -0.005:
                return "Moderate Negative Impact (Discount)"
            elif coef < 0:
                return "Weak Negative Impact"
            else:
                return "Positive Impact"
        
        env_coef['Interpretation'] = env_coef['Coefficient'].apply(interpret_coef)
        
        print("\n" + "="*60)
        print("ENVIRONMENTAL CHARACTERISTICS IMPACT")
        print("="*60)
        print(env_coef[['Feature', 'Coefficient', 'Interpretation']].to_string(index=False))
        
        return env_coef
    
    def calculate_vif(self, X_train: np.ndarray, feature_names: list = None) -> pd.DataFrame:
        """
        Calculate Variance Inflation Factor for multicollinearity detection.
        
        Args:
            X_train: Training features
            feature_names: List of feature names
            
        Returns:
            DataFrame with VIF values
        """
        feature_names = feature_names or self.feature_names
        
        vif_data = pd.DataFrame()
        vif_data['Feature'] = feature_names
        vif_data['VIF'] = [variance_inflation_factor(X_train, i) for i in range(X_train.shape[1])]
        vif_data = vif_data.sort_values('VIF', ascending=False)
        
        print("\n" + "="*60)
        print("MULTICOLLINEARITY CHECK (VIF)")
        print("="*60)
        print("VIF > 10: High multicollinearity (problematic)")
        print("VIF 5-10: Moderate multicollinearity (caution)")
        print("VIF < 5: Low multicollinearity (acceptable)")
        print(vif_data.to_string(index=False))
        
        return vif_data
    
    def marginal_willingness_to_pay(self, feature_name: str, 
                                   base_price: float = None) -> Dict[str, float]:
        """
        Calculate Marginal Willingness to Pay (MWTP) for a feature.
        
        For a hedonic model in log-price form:
        MWTP = β * P (where P is base price)
        
        Args:
            feature_name: Name of feature
            base_price: Reference price (median if None)
            
        Returns:
            Dictionary with MWTP calculations
        """
        if self.coefficients is None:
            self.get_coefficients()
        
        coef_row = self.coefficients[self.coefficients['Feature'] == feature_name]
        if coef_row.empty:
            raise ValueError(f"Feature '{feature_name}' not found in model")
        
        coef = coef_row['Coefficient'].values[0]
        
        # Use median price as reference if not provided
        if base_price is None:
            base_price = 300000  # Assumed median from synthetic data
        
        # MWTP = coefficient * price (for semi-log model)
        mwtp = coef * base_price
        
        # Percentage change in price
        pct_change = coef * 100
        
        result = {
            'feature': feature_name,
            'coefficient': coef,
            'base_price': base_price,
            'mwtp': mwtp,
            'pct_change': pct_change
        }
        
        print(f"\nMarginal Willingness to Pay for '{feature_name}':")
        print(f"  Coefficient: {coef:.6f}")
        print(f"  Base Price: ${base_price:,.0f}")
        print(f"  MWTP (for 1 unit): ${mwtp:,.2f}")
        print(f"  Percentage Change: {pct_change:.3f}%")
        
        return result
    
    def summary_statistics(self) -> Dict:
        """Generate comprehensive model summary statistics."""
        if self.statsmodels_result is None:
            return {
                'message': 'Summary statistics available only after fit_statsmodels() is called'
            }
        
        return {
            'r_squared': self.statsmodels_result.rsquared,
            'adj_r_squared': self.statsmodels_result.rsquared_adj,
            'f_statistic': self.statsmodels_result.fvalue,
            'f_pvalue': self.statsmodels_result.f_pvalue,
            'aic': self.statsmodels_result.aic,
            'bic': self.statsmodels_result.bic,
            'nobs': self.statsmodels_result.nobs
        }


def compare_models(X_train: np.ndarray, X_test: np.ndarray, 
                  y_train: np.ndarray, y_test: np.ndarray,
                  feature_names: list = None) -> Dict[str, Dict]:
    """
    Compare sklearn and statsmodels implementations.
    
    Args:
        X_train, X_test, y_train, y_test: Training and test data
        feature_names: List of feature names
        
    Returns:
        Dictionary comparing both models
    """
    results = {}
    
    # Sklearn model
    print("Training scikit-learn model...")
    sklearn_model = HedonicPricingModel()
    sklearn_model.fit_sklearn(X_train, y_train, feature_names)
    sklearn_metrics = sklearn_model.evaluate(X_test, y_test)
    results['sklearn'] = sklearn_metrics
    
    # Statsmodels model
    print("\n\nTraining statsmodels OLS model...")
    sm_model = HedonicPricingModel()
    sm_model.fit_statsmodels(X_train, y_train, feature_names)
    sm_metrics = sm_model.evaluate(X_test, y_test)
    results['statsmodels'] = sm_metrics
    
    return results


if __name__ == "__main__":
    from data_generation import create_sample_data
    from data_processor import DataProcessor
    
    print("Generating and processing data...")
    df = create_sample_data(n_samples=500)
    
    processor = DataProcessor()
    df = processor.clean_data(df)
    df = processor.create_features(df)
    X, y = processor.prepare_for_modeling(df)
    X_train, X_test, y_train, y_test = processor.train_test_split_data(X, y)
    
    print("\n" + "="*60)
    print("HEDONIC MODEL ANALYSIS")
    print("="*60)
    
    # Fit and evaluate
    model = HedonicPricingModel()
    model.fit_sklearn(X_train, y_train, feature_names=X.columns.tolist())
    model.evaluate(X_test, y_test)
    model.get_coefficients()
    model.get_environmental_coefficients()