"""
Main pipeline orchestrator for hedonic pricing model.
Coordinates data generation, processing, modeling, and analysis.
"""

import os
import sys
import pandas as pd
from datetime import datetime

from config import (
    DataConfig, HedonicConfig, EconometricConfig,
    DEFAULT_DATA_CONFIG, DEFAULT_HEDONIC_CONFIG, DEFAULT_ECONOMETRIC_CONFIG
)
from data_generation import SyntheticDataGenerator
from data_processor import DataProcessor, process_pipeline
from hedonic_model import HedonicPricingModel
from econometric_methods import (
    DifferenceInDifferences, RegressionDiscontinuity, 
    InstrumentalVariables, run_all_methods
)
from visualization import HedonicVisualizer, EconometricVisualizer, save_figure


class HedonicPricingPipeline:
    """Complete pipeline for hedonic pricing analysis."""
    
    def __init__(self, 
                 data_config: DataConfig = None,
                 hedonic_config: HedonicConfig = None,
                 econometric_config: EconometricConfig = None,
                 output_dir: str = 'output'):
        """
        Initialize pipeline.
        
        Args:
            data_config: DataConfig for data generation
            hedonic_config: HedonicConfig for modeling
            econometric_config: EconometricConfig for econometric methods
            output_dir: Directory to save outputs
        """
        self.data_config = data_config or DEFAULT_DATA_CONFIG
        self.hedonic_config = hedonic_config or DEFAULT_HEDONIC_CONFIG
        self.econometric_config = econometric_config or DEFAULT_ECONOMETRIC_CONFIG
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'data'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'figures'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'results'), exist_ok=True)
        
        # Results storage
        self.df_raw = None
        self.df_processed = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.hedonic_model = None
        self.econometric_results = None
        
        self._log(f"Pipeline initialized | Output: {output_dir}")
    
    def _log(self, message: str) -> None:
        """Print timestamped log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def step_1_generate_data(self, n_samples: int = None, save: bool = True) -> pd.DataFrame:
        """
        Step 1: Generate synthetic data.
        
        Args:
            n_samples: Number of samples to generate
            save: Whether to save to CSV
            
        Returns:
            Generated DataFrame
        """
        self._log("="*70)
        self._log("STEP 1: GENERATING SYNTHETIC DATA")
        self._log("="*70)
        
        if n_samples:
            self.data_config.n_samples = n_samples
        
        generator = SyntheticDataGenerator(self.data_config)
        
        if save:
            filepath = os.path.join(self.output_dir, 'data', 'synthetic_properties.csv')
            self.df_raw = generator.generate_and_save(filepath)
        else:
            self.df_raw = generator.generate()
            self._log(f"Generated {len(self.df_raw)} synthetic transactions")
        
        print(f"\nDataset shape: {self.df_raw.shape}")
        print(f"Price range: ${self.df_raw['price'].min():,.0f} - ${self.df_raw['price'].max():,.0f}")
        print(f"Mean price: ${self.df_raw['price'].mean():,.0f}")
        
        return self.df_raw
    
    def step_2_process_data(self) -> pd.DataFrame:
        """
        Step 2: Clean and process data.
        
        Returns:
            Processed DataFrame
        """
        if self.df_raw is None:
            raise ValueError("Must run step_1_generate_data() first")
        
        self._log("\n" + "="*70)
        self._log("STEP 2: PROCESSING DATA")
        self._log("="*70)
        
        processor = DataProcessor(self.hedonic_config)
        
        self.df_processed = self.df_raw.copy()
        self.df_processed = processor.clean_data(self.df_processed)
        self.df_processed = processor.create_features(self.df_processed)
        
        # Save processed data
        filepath = os.path.join(self.output_dir, 'data', 'processed_properties.csv')
        self.df_processed.to_csv(filepath, index=False)
        self._log(f"Processed data saved to {filepath}")
        
        print(f"\nProcessed dataset shape: {self.df_processed.shape}")
        print(f"Engineered features: {len(self.df_processed.columns)}")
        
        return self.df_processed
    
    def step_3_prepare_for_modeling(self) -> tuple:
        """
        Step 3: Prepare features for modeling.
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test, df_processed)
        """
        if self.df_processed is None:
            raise ValueError("Must run step_2_process_data() first")
        
        self._log("\n" + "="*70)
        self._log("STEP 3: PREPARING FOR MODELING")
        self._log("="*70)
        
        self.X_train, self.X_test, self.y_train, self.y_test, self.df_processed = \
            process_pipeline(self.df_processed, self.hedonic_config)
        
        return self.X_train, self.X_test, self.y_train, self.y_test, self.df_processed
    
    def step_4_fit_hedonic_model(self, use_statsmodels: bool = True) -> HedonicPricingModel:
        """
        Step 4: Fit hedonic pricing model.
        
        Args:
            use_statsmodels: Whether to use statsmodels for statistical inference
            
        Returns:
            Fitted HedonicPricingModel
        """
        if self.X_train is None:
            raise ValueError("Must run step_3_prepare_for_modeling() first")
        
        self._log("\n" + "="*70)
        self._log("STEP 4: FITTING HEDONIC PRICING MODEL")
        self._log("="*70)
        
        self.hedonic_model = HedonicPricingModel(self.hedonic_config)
        
        # Get feature names
        if hasattr(self.X_train, 'columns'):
            feature_names = self.X_train.columns.tolist()
        else:
            feature_names = [f"Feature_{i}" for i in range(self.X_train.shape[1])]
        
        # Fit model
        self.hedonic_model.fit_sklearn(self.X_train, self.y_train, feature_names)
        
        if use_statsmodels:
            self.hedonic_model.fit_statsmodels(self.X_train, self.y_train, feature_names)
        
        # Evaluate
        metrics = self.hedonic_model.evaluate(self.X_test, self.y_test)
        
        # Get coefficients
        coef_df = self.hedonic_model.get_coefficients()
        
        # Environmental impact
        self.hedonic_model.get_environmental_coefficients()
        
        # Save results
        filepath = os.path.join(self.output_dir, 'results', 'hedonic_coefficients.csv')
        coef_df.to_csv(filepath, index=False)
        self._log(f"Coefficients saved to {filepath}")
        
        return self.hedonic_model
    
    def step_5_run_econometric_methods(self) -> dict:
        """
        Step 5: Run econometric methods (DiD, RDD, IV).
        
        Returns:
            Dictionary with econometric results
        """
        if self.df_processed is None:
            raise ValueError("Must run step_2_process_data() first")
        
        self._log("\n" + "="*70)
        self._log("STEP 5: RUNNING ECONOMETRIC METHODS")
        self._log("="*70)
        
        self.econometric_results = run_all_methods(
            self.df_processed, 
            self.econometric_config
        )
        
        # Save results
        filepath = os.path.join(self.output_dir, 'results', 'econometric_results.csv')
        results_df = pd.DataFrame({
            'Method': list(self.econometric_results.keys()),
            'Coefficient': [v.get('coefficient', v.get('discontinuity')) 
                          for v in self.econometric_results.values()],
            'Std_Error': [v.get('std_error') for v in self.econometric_results.values()],
            'P_Value': [v.get('p_value') for v in self.econometric_results.values()],
            'Significant': [v.get('significant') for v in self.econometric_results.values()]
        })
        results_df.to_csv(filepath, index=False)
        self._log(f"Econometric results saved to {filepath}")
        
        return self.econometric_results
    
    def step_6_create_visualizations(self) -> None:
        """Step 6: Create and save visualizations."""
        self._log("\n" + "="*70)
        self._log("STEP 6: CREATING VISUALIZATIONS")
        self._log("="*70)
        
        fig_dir = os.path.join(self.output_dir, 'figures')
        
        # Hedonic visualizations
        hv = HedonicVisualizer()
        
        fig1 = hv.plot_price_distribution(self.df_processed['price'])
        save_figure(fig1, os.path.join(fig_dir, '01_price_distribution.png'))
        
        coef_df = self.hedonic_model.get_coefficients()
        
        fig2 = hv.plot_coefficients(coef_df)
        save_figure(fig2, os.path.join(fig_dir, '02_coefficients.png'))
        
        fig3 = hv.plot_environmental_impact(coef_df)
        save_figure(fig3, os.path.join(fig_dir, '03_environmental_impact.png'))
        
        fig4 = hv.plot_actual_vs_predicted(self.y_test, self.hedonic_model.predictions)
        save_figure(fig4, os.path.join(fig_dir, '04_actual_vs_predicted.png'))
        
        fig5 = hv.plot_residuals(self.hedonic_model.residuals, self.hedonic_model.predictions)
        save_figure(fig5, os.path.join(fig_dir, '05_residuals_diagnostics.png'))
        
        # Econometric visualizations
        ev = EconometricVisualizer()
        
        fig6 = ev.plot_did_trends(self.df_processed)
        save_figure(fig6, os.path.join(fig_dir, '06_did_trends.png'))
        
        fig7 = ev.plot_rdd_discontinuity(self.df_processed)
        save_figure(fig7, os.path.join(fig_dir, '07_rdd_discontinuity.png'))
        
        fig8 = ev.plot_effects_comparison(self.econometric_results)
        save_figure(fig8, os.path.join(fig_dir, '08_effects_comparison.png'))
        
        self._log(f"✓ All visualizations saved to {fig_dir}")
    
    def run_full_pipeline(self, n_samples: int = 1000) -> None:
        """
        Run the complete pipeline from start to finish.
        
        Args:
            n_samples: Number of synthetic samples to generate
        """
        self._log("\n" + "█"*70)
        self._log("█" + " ".join(" "*68 + "█"))
        self._log("█" + "  HEDONIC PRICING MODEL - COMPLETE ANALYSIS PIPELINE  ".center(68) + "█")
        self._log("█" + " ".join(" "*68 + "█"))
        self._log("█"*70)
        
        try:
            # Run all steps
            self.step_1_generate_data(n_samples=n_samples)
            self.step_2_process_data()
            self.step_3_prepare_for_modeling()
            self.step_4_fit_hedonic_model()
            self.step_5_run_econometric_methods()
            self.step_6_create_visualizations()
            
            self._log("\n" + "█"*70)
            self._log("█" + "  ✓ PIPELINE COMPLETE  ".center(68) + "█")
            self._log("█"*70)
            self._log(f"\nAll outputs saved to: {os.path.abspath(self.output_dir)}")
            
        except Exception as e:
            self._log(f"\n✗ PIPELINE FAILED: {str(e)}")
            raise


def main():
    """Main entry point."""
    
    # Configure models
    data_config = DataConfig(n_samples=1000)
    hedonic_config = HedonicConfig()
    econometric_config = EconometricConfig()
    
    # Create and run pipeline
    pipeline = HedonicPricingPipeline(
        data_config=data_config,
        hedonic_config=hedonic_config,
        econometric_config=econometric_config,
        output_dir='output'
    )
    
    pipeline.run_full_pipeline(n_samples=1000)


if __name__ == "__main__":
    main()
