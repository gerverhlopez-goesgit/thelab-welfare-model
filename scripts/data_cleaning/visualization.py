"""
Visualization tools for hedonic pricing model and econometric analysis.
Creates publication-quality plots for model results.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple


class HedonicVisualizer:
    """Create visualizations for hedonic pricing analysis."""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid', figsize: Tuple = (12, 8)):
        """Initialize visualizer."""
        
        Args:
            style: Matplotlib style
            figsize: Default figure size
        """
        plt.style.use(style)
        self.figsize = figsize
        self.colors = sns.color_palette("husl", 8)
    
    def plot_price_distribution(self, prices: pd.Series, log_scale: bool = True) -> plt.Figure:
        """Plot distribution of property prices."""
        
        Args:
            prices: Series of property prices
            log_scale: Whether to use log scale
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 2, figsize=self.figsize)
        
        # Histogram
        if log_scale:
            log_prices = np.log(prices)
            axes[0].hist(log_prices, bins=50, color=self.colors[0], alpha=0.7, edgecolor='black')
            axes[0].set_xlabel('Log(Price)')
            axes[0].set_title('Distribution of Log Prices')
        else:
            axes[0].hist(prices, bins=50, color=self.colors[0], alpha=0.7, edgecolor='black')
            axes[0].set_xlabel('Price ($)')
            axes[0].set_title('Distribution of Prices')
        
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        box_data = np.log(prices) if log_scale else prices
        bp = axes[1].boxplot(box_data, vert=True, patch_artist=True)
        bp['boxes'][0].set_facecolor(self.colors[0])
        axes[1].set_ylabel('Log(Price)' if log_scale else 'Price ($)')
        axes[1].set_title('Price Distribution Summary')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_coefficients(self, coef_df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
        """Plot model coefficients with error bars."""
        
        Args:
            coef_df: DataFrame with coefficient information
            top_n: Number of top coefficients to display
            
        Returns:
            Matplotlib figure
        """
        # Sort by absolute value and get top N
        plot_df = coef_df.nlargest(top_n, 'Abs_Coefficient')
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        colors = [self.colors[1] if x > 0 else self.colors[2] for x in plot_df['Coefficient']]
        
        y_pos = np.arange(len(plot_df))
        
        ax.barh(y_pos, plot_df['Coefficient'], color=colors, alpha=0.7, edgecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(plot_df['Feature'])
        ax.set_xlabel('Coefficient Value')
        ax.set_title('Top Hedonic Pricing Coefficients')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, v in enumerate(plot_df['Coefficient']):
            ax.text(v, i, f' {v:.4f}', va='center', ha='left' if v > 0 else 'right')
        
        plt.tight_layout()
        return fig
    
    def plot_environmental_impact(self, coef_df: pd.DataFrame) -> plt.Figure:
        """Plot environmental characteristics impact on prices."""
        
        Args:
            coef_df: DataFrame with environmental coefficients
            
        Returns:
            Matplotlib figure
        """
        env_features = ['pm25', 'no2', 'ozone', 'tri_proximity', 'flood_zone']
        env_coef = coef_df[coef_df['Feature'].isin(env_features)]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Bar plot of coefficients
        colors = [self.colors[2] if x < 0 else self.colors[1] for x in env_coef['Coefficient']]
        ax1.bar(env_coef['Feature'], env_coef['Coefficient'], color=colors, alpha=0.7, edgecolor='black')
        ax1.set_ylabel('Coefficient Value')
        ax1.set_title('Environmental Impact on Log(Price)')
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax1.grid(True, alpha=0.3, axis='y')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Percentage impact
        pct_impact = env_coef['Coefficient'] * 100
        colors = [self.colors[2] if x < 0 else self.colors[1] for x in pct_impact]
        ax2.bar(env_coef['Feature'], pct_impact, color=colors, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('Percentage Impact (%)')
        ax2.set_title('Environmental Impact on Price (%)')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax2.grid(True, alpha=0.3, axis='y')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def plot_residuals(self, residuals: np.ndarray, predictions: np.ndarray) -> plt.Figure:
        """Plot model residuals diagnostics."""
        
        Args:
            residuals: Model residuals
            predictions: Model predictions
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        
        # Residuals vs fitted
        axes[0, 0].scatter(predictions, residuals, alpha=0.5, color=self.colors[0])
        axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
        axes[0, 0].set_xlabel('Fitted Values')
        axes[0, 0].set_ylabel('Residuals')
        axes[0, 0].set_title('Residuals vs Fitted Values')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Q-Q Plot')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Histogram of residuals
        axes[1, 0].hist(residuals, bins=50, color=self.colors[1], alpha=0.7, edgecolor='black')
        axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
        axes[1, 0].set_xlabel('Residuals')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Distribution of Residuals')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Scale-location plot
        standardized_residuals = residuals / np.std(residuals)
        axes[1, 1].scatter(predictions, np.sqrt(np.abs(standardized_residuals)), 
                          alpha=0.5, color=self.colors[2])
        axes[1, 1].set_xlabel('Fitted Values')
        axes[1, 1].set_ylabel('√|Standardized Residuals|')
        axes[1, 1].set_title('Scale-Location Plot')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_actual_vs_predicted(self, actual: np.ndarray, predicted: np.ndarray) -> plt.Figure:
        """Plot actual vs predicted prices."""
        
        Args:
            actual: Actual log prices
            predicted: Predicted log prices
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.scatter(actual, predicted, alpha=0.5, color=self.colors[0], edgecolor='black', linewidth=0.5)
        
        # Perfect prediction line
        min_val = min(actual.min(), predicted.min())
        max_val = max(actual.max(), predicted.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        ax.set_xlabel('Actual Log(Price)')
        ax.set_ylabel('Predicted Log(Price)')
        ax.set_title('Actual vs Predicted Property Prices')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add R² annotation
        from sklearn.metrics import r2_score
        r2 = r2_score(actual, predicted)
        ax.text(0.05, 0.95, f'R² = {r2:.4f}', transform=ax.transAxes, 
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        return fig


class EconometricVisualizer:
    """Create visualizations for econometric analysis."""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid', figsize: Tuple = (12, 8)):
        """Initialize visualizer."""
        plt.style.use(style)
        self.figsize = figsize
        self.colors = sns.color_palette("husl", 8)
    
    def plot_did_trends(self, df: pd.DataFrame, years: Optional[List] = None) -> plt.Figure:
        """Plot DiD trends for treated and control groups."""
        
        Args:
            df: DataFrame with transaction data and treatment variables
            years: Optional specific years to plot
            
        Returns:
            Matplotlib figure
        """
        df = df.copy()
        df['log_price'] = np.log(df['price'])
        
        # Group by year and treatment status
        trend_data = df.groupby(['year', 'treated'])['log_price'].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        for treated in [0, 1]:
            data = trend_data[trend_data['treated'] == treated]
            label = 'Treated' if treated == 1 else 'Control'
            color = self.colors[1] if treated == 1 else self.colors[0]
            ax.plot(data['year'], data['log_price'], marker='o', label=label, 
                   color=color, linewidth=2, markersize=8)
        
        # Add shock year line
        shock_year = df['year'].max() - 5  # Approximate shock year
        ax.axvline(x=shock_year, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Shock Year')
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Log(Price)')
        ax.set_title('Difference-in-Differences: Price Trends')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_rdd_discontinuity(self, df: pd.DataFrame, running_var: str = 'tri_proximity') -> plt.Figure:
        """Plot regression discontinuity with cutoff point."""
        
        Args:
            df: DataFrame with transaction data
            running_var: Name of running variable
            
        Returns:
            Matplotlib figure
        """
        df = df.copy()
        df['log_price'] = np.log(df['price'])
        
        cutoff = 2.5
        bandwidth = 1.0
        
        # Filter to bandwidth
        df_window = df[np.abs(df[running_var] - cutoff) <= bandwidth].copy()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Separate treated and control
        treated = df_window[df_window[running_var] <= cutoff]
        control = df_window[df_window[running_var] > cutoff]
        
        # Scatter plots
        ax.scatter(treated[running_var], treated['log_price'], alpha=0.5, 
                  color=self.colors[1], label='Treated (≤ cutoff)', s=50)
        ax.scatter(control[running_var], control['log_price'], alpha=0.5, 
                  color=self.colors[0], label='Control (> cutoff)', s=50)
        
        # Add local linear fits
        from scipy.stats import linregress
        
        for group, color in [(treated, self.colors[1]), (control, self.colors[0])]:
            if len(group) > 1:
                slope, intercept, _, _, _ = linregress(group[running_var], group['log_price'])
                x_line = np.array([group[running_var].min(), group[running_var].max()])
                y_line = slope * x_line + intercept
                ax.plot(x_line, y_line, color=color, linewidth=2)
        
        # Cutoff line
        ax.axvline(x=cutoff, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Cutoff')
        
        ax.set_xlabel(f'{running_var}')
        ax.set_ylabel('Log(Price)')
        ax.set_title('Regression Discontinuity Design: Treatment Effect at Cutoff')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_effects_comparison(self, results: Dict) -> plt.Figure:
        """Compare treatment effects across all three methods."""
        
        Args:
            results: Dictionary with results from DiD, RDD, and IV
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        methods = []
        effects = []
        errors = []
        
        # Extract results
        if 'did' in results:
            methods.append('DiD')
            effects.append(results['did']['coefficient'])
            errors.append(results['did']['std_error'])
        
        if 'rdd' in results:
            methods.append('RDD')
            effects.append(results['rdd']['discontinuity'])
            errors.append(results['rdd']['std_error'])
        
        if 'iv' in results:
            methods.append('IV')
            effects.append(results['iv']['coefficient'])
            errors.append(results['iv']['std_error'])
        
        # Bar plot with error bars
        colors = [self.colors[i] for i in range(len(methods))]
        x_pos = np.arange(len(methods))
        
        ax.bar(x_pos, effects, yerr=errors, capsize=10, color=colors, alpha=0.7, edgecolor='black')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(methods)
        ax.set_ylabel('Treatment Effect (Coefficient)')
        ax.set_title('Comparison of Causal Effects Across Methods')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(effects):
            ax.text(i, v, f'{v:.4f}', ha='center', va='bottom' if v > 0 else 'top')
        
        plt.tight_layout()
        return fig


def save_figure(fig: plt.Figure, filepath: str, dpi: int = 300) -> None:
    """Save figure to file."""
    
    Args:
        fig: Matplotlib figure
        filepath: Path to save to
        dpi: Resolution in dpi
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"✓ Figure saved to {filepath}")


if __name__ == "__main__":
    from data_generation import create_sample_data
    from data_processor import DataProcessor
    from hedonic_model import HedonicPricingModel
    
    # Generate data
    print("Generating sample data...")
    df = create_sample_data(n_samples=500)
    
    # Process data
    processor = DataProcessor()
    df = processor.clean_data(df)
    df = processor.create_features(df)
    X, y = processor.prepare_for_modeling(df)
    X_train, X_test, y_train, y_test = processor.train_test_split_data(X, y)
    
    # Fit model
    model = HedonicPricingModel()
    model.fit_sklearn(X_train, y_train, feature_names=X.columns.tolist())
    model.evaluate(X_test, y_test)
    coef_df = model.get_coefficients()
    
    # Create visualizations
    visualizer = HedonicVisualizer()
    
    fig1 = visualizer.plot_price_distribution(df['price'])
    save_figure(fig1, 'price_distribution.png')
    
    fig2 = visualizer.plot_coefficients(coef_df)
    save_figure(fig2, 'coefficients.png')
    
    fig3 = visualizer.plot_environmental_impact(coef_df)
    save_figure(fig3, 'environmental_impact.png')
    
    fig4 = visualizer.plot_actual_vs_predicted(y_test, model.predictions)
    save_figure(fig4, 'actual_vs_predicted.png')
    
    print("\n✓ All visualizations created!")