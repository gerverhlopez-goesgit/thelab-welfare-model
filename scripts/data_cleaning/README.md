# Hedonic Pricing Model: Environmental Shocks & Property Valuation

A comprehensive Python framework for analyzing how environmental characteristics and shocks impact property values using hedonic pricing models and advanced econometric methods.

## Overview

This project implements the hedonic pricing framework described in your research:

$$\ln(P) = \beta_0 + \sum(\beta_i S_i) + \sum(\gamma_j N_j) + \sum(\delta_k E_k) + \epsilon$$

Where:
- **P** = Property price
- **Sᵢ** = Structural characteristics (sqft, bedrooms, bathrooms, age)
- **Nⱼ** = Neighborhood characteristics (school quality, crime, walkability)
- **Eₖ** = Environmental characteristics (PM2.5, NO₂, Ozone, TRI proximity, flood zone)

## Key Features

### 1. **Hedonic Pricing Model**
- Semi-log specification for percentage-based valuation analysis
- Joint implementation with scikit-learn and statsmodels
- Statistical inference with p-values, confidence intervals, and VIF
- Environmental impact quantification
- Marginal Willingness to Pay (MWTP) calculations

### 2. **Econometric Methods**

#### Difference-in-Differences (DiD)
Measures treatment effects by comparing price changes in treated vs control regions before/after environmental shocks: