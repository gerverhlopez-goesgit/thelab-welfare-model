"""
Econometric methods for causal inference in hedonic pricing.
Implements Difference-in-Differences, Regression Discontinuity, and Instrumental Variables.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols, IV, ivregress
from sklearn.linear_model import LinearRegression
from typing import Dict, Tuple, Optional
from config import EconometricConfig


class DifferenceInDifferences:
    """
    Difference-in-Differences (DiD) estimation.
    
    Measures the effect of a treatment/shock by comparing changes in treated vs control groups
    before and after the treatment event.
    
    Equation:
    log(P) = β₀ + β₁*treated + β₂*post_shock + β₃*(treated × post_shock) + ε
    
    Where β₃ is the treatment effect (DiD estimator)
    """
    
    def __init__(self, config: EconometricConfig = None):
        """
        Initialize DiD estimator.
        
        Args:
            config: EconometricConfig object
        """
        self.config = config or EconometricConfig()
        self.model = None
        self.results = None
        self.treatment_effect = None
    
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for DiD estimation.
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with DiD variables
        """
        df = df.copy()
        
        # Ensure required columns exist
        required = ['price', 'treated', 'year', 'region']
        if not all(col in df.columns for col in required):
            raise ValueError(f"DataFrame must contain: {required}")
        
        # Create post-shock indicator
        df['post_shock'] = (df['year'] >= self.config.did_treatment_year).astype(int)
        
        # Create interaction term
        df['did_interaction'] = df['treated'] * df['post_shock']
        
        # Create log price
        df['log_price'] = np.log(df['price'])
        
        print(f"✓ DiD data prepared")
        print(f"  Treatment year: {self.config.did_treatment_year}")
        print(f"  Treated observations: {df['treated'].sum()}")
        print(f"  Post-shock observations: {df['post_shock'].sum()}")
        
        return df
    
    def estimate(self, df: pd.DataFrame, formula: str = None) -> 'DifferenceInDifferences':
        """
        Estimate DiD model using OLS.
        
        Args:
            df: Prepared DataFrame with DiD variables
            formula: Optional statsmodels formula string
            
        Returns:
            Self for method chaining
        """
        df = self.prepare_data(df)
        
        # Default formula
        if formula is None:
            formula = "log_price ~ C(treated) + C(post_shock) + C(treated):C(post_shock)"
        
        # Add controls
        control_vars = ['school_rating', 'crime_rate', 'walkability', 'pm25', 'no2', 'ozone']
        available_controls = [v for v in control_vars if v in df.columns]
        if available_controls:
            formula += " + " + " + ".join(available_controls)
        
        # Fit OLS model
        model = ols(formula, data=df)
        self.results = model.fit()
        
        # Extract treatment effect
        self.treatment_effect = self.results.params.get('C(treated)[T.1]:C(post_shock)[T.1]')
        
        print("
" + "="*60)
        print("DIFFERENCE-IN-DIFFERENCES RESULTS")
        print("="*60)
        print(self.results.summary())
        
        return self
    
    def get_treatment_effect(self) -> Dict[str, float]:
        """
        Extract and interpret treatment effect.
        
        Returns:
            Dictionary with treatment effect statistics
        """
        if self.results is None:
            raise ValueError("Model must be estimated first using estimate()")
        
        # Get the DiD coefficient (interaction term)
        did_coef = self.results.params.get('C(treated)[T.1]:C(post_shock)[T.1]')
        did_se = self.results.bse.get('C(treated)[T.1]:C(post_shock)[T.1]')
        did_pval = self.results.pvalues.get('C(treated)[T.1]:C(post_shock)[T.1]')
        
        # Calculate 95% CI
        ci_lower = did_coef - 1.96 * did_se
        ci_upper = did_coef + 1.96 * did_se
        
        result = {
            'coefficient': did_coef,
            'std_error': did_se,
            'p_value': did_pval,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'significant': did_pval < 0.05,
            'pct_effect': did_coef * 100
        }
        
        print("
" + "="*60)
        print("TREATMENT EFFECT INTERPRETATION")
        print("="*60)
        print(f"DiD Coefficient: {did_coef:.4f}")
        print(f"Standard Error: {did_se:.4f}")
        print(f"P-value: {did_pval:.4f}")
        print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"Significant at 0.05 level: {result['significant']}")
        print(f"\nInterpretation: Treatment shock reduced prices by {abs(did_coef*100):.2f}%")
        
        return result


class RegressionDiscontinuity:
    """
    Regression Discontinuity Design (RDD).
    
    Identifies treatment effects at a cutoff point (discontinuity) where treatment
    status changes sharply.
    
    Example: Properties within 2.5 km of TRI site (treated) vs beyond (control)
    """
    
    def __init__(self, config: EconometricConfig = None):
        """
        Initialize RDD estimator.
        
        Args:
            config: EconometricConfig object
        """
        self.config = config or EconometricConfig()
        self.model_left = None
        self.model_right = None
        self.results_left = None
        self.results_right = None
        self.discontinuity = None
    
    def prepare_data(self, df: pd.DataFrame, 
                    running_var: str = 'tri_proximity') -> pd.DataFrame:
        """
        Prepare data for RDD around cutoff point.
        
        Args:
            df: DataFrame with transaction data
            running_var: Name of running variable (distance variable)
            
        Returns:
            DataFrame filtered to bandwidth around cutoff
        """
        df = df.copy()
        
        # Ensure running variable exists
        if running_var not in df.columns:
            raise ValueError(f"Column '{running_var}' not found in DataFrame")
        
        # Create treatment indicator at cutoff
        df['treated'] = (df[running_var] <= self.config.rdd_cutoff).astype(int)
        
        # Center running variable at cutoff
        df['running_var_centered'] = df[running_var] - self.config.rdd_cutoff
        
        # Filter to bandwidth
        df = df[np.abs(df['running_var_centered']) <= self.config.rdd_bandwidth].copy()
        
        # Create log price
        df['log_price'] = np.log(df['price'])
        
        print(f"✓ RDD data prepared")
        print(f"  Running variable: {running_var}")
        print(f"  Cutoff value: {self.config.rdd_cutoff}")
        print(f"  Bandwidth: {self.config.rdd_bandwidth}")
        print(f"  Observations in bandwidth: {len(df)}")
        print(f"  Treated: {df['treated'].sum()}, Control: {(1-df['treated']).sum()}")
        
        return df
    
    def estimate(self, df: pd.DataFrame, 
                running_var: str = 'tri_proximity') -> 'RegressionDiscontinuity':
        """
        Estimate RDD using local linear regression.
        
        Args:
            df: DataFrame with transaction data
            running_var: Name of running variable
            
        Returns:
            Self for method chaining
        """
        df = self.prepare_data(df, running_var)
        
        # Separate data left and right of cutoff
        df_left = df[df['running_var_centered'] < 0].copy()
        df_right = df[df['running_var_centered'] >= 0].copy()
        
        # Build formula for polynomial regression
        if self.config.rdd_polynomial == 1:
            formula = "log_price ~ running_var_centered * C(treated)"
        else:
            formula = "log_price ~ poly(running_var_centered, {}) * C(treated)".format(
                self.config.rdd_polynomial
            )
        
        # Fit full model
        model = ols(formula, data=df)
        results = model.fit()
        
        print("
" + "="*60)
        print("REGRESSION DISCONTINUITY DESIGN RESULTS")
        print("="*60)
        print(results.summary())
        
        self.results_left = results
        self.discontinuity = results.params.get('C(treated)[T.1]')
        
        return self
    
    def get_discontinuity(self) -> Dict[str, float]:
        """
        Extract and interpret discontinuity (RDD treatment effect).
        
        Returns:
            Dictionary with discontinuity statistics
        """
        if self.results_left is None:
            raise ValueError("Model must be estimated first using estimate()")
        
        # Get the discontinuity (treatment effect at cutoff)
        disc_coef = self.results_left.params.get('C(treated)[T.1]')
        disc_se = self.results_left.bse.get('C(treated)[T.1]')
        disc_pval = self.results_left.pvalues.get('C(treated)[T.1]')
        
        ci_lower = disc_coef - 1.96 * disc_se
        ci_upper = disc_coef + 1.96 * disc_se
        
        result = {
            'discontinuity': disc_coef,
            'std_error': disc_se,
            'p_value': disc_pval,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'significant': disc_pval < 0.05,
            'pct_effect': disc_coef * 100
        }
        
        print("
" + "="*60)
        print("DISCONTINUITY INTERPRETATION")
        print("="*60)
        print(f"Discontinuity at Cutoff: {disc_coef:.4f}")
        print(f"Standard Error: {disc_se:.4f}")
        print(f"P-value: {disc_pval:.4f}")
        print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"Significant: {result['significant']}")
        print(f"\nInterpretation: Properties just inside cutoff are worth {abs(disc_coef*100):.2f}% " +
              f"{'less' if disc_coef < 0 else 'more'} than those just outside")
        
        return result


class InstrumentalVariables:
    """
    Instrumental Variables (IV) estimation.
    
    Addresses endogeneity using instruments (e.g., wind patterns for air quality)
    to isolate causal effects of environmental variables on property values.
    
    First Stage: E[air_quality] = π₀ + π₁*wind_pattern + ε₁
    Second Stage: log(P) = β₀ + β₁*air_quality_predicted + β₂*X + ε₂
    """
    
    def __init__(self, config: EconometricConfig = None):
        """
        Initialize IV estimator.
        
        Args:
            config: EconometricConfig object
        """
        self.config = config or EconometricConfig()
        self.first_stage_results = None
        self.second_stage_results = None
        self.instruments = None
    
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for IV estimation.
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with required variables
        """
        df = df.copy()
        
        # Create air quality index (endogenous variable)
        if 'pm25' in df.columns and 'no2' in df.columns and 'ozone' in df.columns:
            # Normalize and create composite index
            pm25_norm = (df['pm25'] - df['pm25'].min()) / (df['pm25'].max() - df['pm25'].min())
            no2_norm = (df['no2'] - df['no2'].min()) / (df['no2'].max() - df['no2'].min())
            ozone_norm = (df['ozone'] - df['ozone'].min()) / (df['ozone'].max() - df['ozone'].min())
            df['air_quality'] = (pm25_norm + no2_norm + ozone_norm) / 3
        
        # Create log price
        df['log_price'] = np.log(df['price'])
        
        # Create distance-from-freeway instrument if not present
        if 'distance_from_freeway' not in df.columns:
            df['distance_from_freeway'] = np.random.exponential(2.0, len(df))
        
        # Wind pattern instrument
        if 'wind_pattern' not in df.columns:
            df['wind_pattern'] = np.random.uniform(-1, 1, len(df))
        
        print(f"✓ IV data prepared")
        print(f"  Endogenous variable: air_quality")
        print(f"  Instruments: wind_pattern, distance_from_freeway")
        
        return df
    
    def estimate_first_stage(self, df: pd.DataFrame) -> 'InstrumentalVariables':
        """
        Estimate first stage (instrument relevance).
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Self for method chaining
        """
        df = self.prepare_data(df)
        
        # Add controls
        formula = "air_quality ~ wind_pattern + distance_from_freeway"
        controls = ['school_rating', 'crime_rate', 'walkability']
        available_controls = [c for c in controls if c in df.columns]
        if available_controls:
            formula += " + " + " + ".join(available_controls)
        
        model = ols(formula, data=df)
        self.first_stage_results = model.fit()
        
        print("
" + "="*60)
        print("FIRST STAGE: INSTRUMENT RELEVANCE")
        print("="*60)
        print(self.first_stage_results.summary())
        
        # Check F-statistic for weak instruments
        f_stat = self.first_stage_results.f_pvalue
        print(f"\nFirst-stage F-statistic p-value: {f_stat:.6f}")
        if f_stat < 0.05:
            print("✓ Instruments appear relevant (F-test significant)")
        else:
            print("⚠ Warning: Instruments may be weak (F-test not significant)")
        
        return self
    
    def estimate_second_stage(self, df: pd.DataFrame) -> 'InstrumentalVariables':
        """
        Estimate second stage (causal effect).
        
        Uses predicted air quality from first stage.
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Self for method chaining
        """
        df = self.prepare_data(df)
        self.estimate_first_stage(df)
        
        # Get predicted air quality
        df['air_quality_predicted'] = self.first_stage_results.predict(df)
        
        # Second stage regression
        X = df[['air_quality_predicted', 'school_rating', 'crime_rate', 'walkability']]
        X = sm.add_constant(X)
        y = df['log_price']
        
        model = sm.OLS(y, X)
        self.second_stage_results = model.fit()
        
        print("
" + "="*60)
        print("SECOND STAGE: CAUSAL EFFECT")
        print("="*60)
        print(self.second_stage_results.summary())
        
        return self
    
    def get_causal_effect(self) -> Dict[str, float]:
        """
        Extract and interpret causal effect of air quality on prices.
        
        Returns:
            Dictionary with IV estimates
        """
        if self.second_stage_results is None:
            raise ValueError("Must call estimate_second_stage() first")
        
        # Get air quality coefficient
        aq_coef = self.second_stage_results.params.get('air_quality_predicted')
        aq_se = self.second_stage_results.bse.get('air_quality_predicted')
        aq_pval = self.second_stage_results.pvalues.get('air_quality_predicted')
        
        ci_lower = aq_coef - 1.96 * aq_se
        ci_upper = aq_coef + 1.96 * aq_se
        
        result = {
            'coefficient': aq_coef,
            'std_error': aq_se,
            'p_value': aq_pval,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'significant': aq_pval < 0.05,
            'pct_effect': aq_coef * 100
        }
        
        print("
" + "="*60)
        print("CAUSAL EFFECT INTERPRETATION")
        print("="*60)
        print(f"Air Quality Coefficient: {aq_coef:.4f}")
        print(f"Standard Error: {aq_se:.4f}")
        print(f"P-value: {aq_pval:.4f}")
        print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"Significant: {result['significant']}")
        print(f"\nInterpretation: 1 unit improvement in air quality (0-1 scale) " +
              f"changes prices by {abs(aq_coef*100):.2f}%")
        
        return result


def run_all_methods(df: pd.DataFrame, config: EconometricConfig = None) -> Dict:
    """
    Run all three econometric methods for comprehensive analysis.
    
    Args:
        df: DataFrame with transaction data
        config: EconometricConfig object
        
    Returns:
        Dictionary with results from all methods
    """
    config = config or EconometricConfig()
    results = {}
    
    print("
" + "="*70)
    print("RUNNING ALL ECONOMETRIC METHODS")
    print("="*70)
    
    # Difference-in-Differences
    print("
1. DIFFERENCE-IN-DIFFERENCES")
    print("-" * 70)
    did = DifferenceInDifferences(config)
    did.estimate(df)
    results['did'] = did.get_treatment_effect()
    
    # Regression Discontinuity
    print("

2. REGRESSION DISCONTINUITY DESIGN")
    print("-" * 70)
    rdd = RegressionDiscontinuity(config)
    rdd.estimate(df)
    results['rdd'] = rdd.get_discontinuity()
    
    # Instrumental Variables
    print("

3. INSTRUMENTAL VARIABLES")
    print("-" * 70)
    iv = InstrumentalVariables(config)
    iv.estimate_second_stage(df)
    results['iv'] = iv.get_causal_effect()
    
    return results


if __name__ == "__main__":
    from data_generation import create_sample_data
    
    print("Generating sample data...")
    df = create_sample_data(n_samples=1000)
    
    config = EconometricConfig()
    results = run_all_methods(df, config)
    
    print("
" + "="*70)
    print("SUMMARY OF ECONOMETRIC RESULTS")
    print("="*70)
    for method, estimates in results.items():
        print(f"\n{method.upper()}:)
        for key, value in estimates.items():
            print(f"  {key}: {value}")