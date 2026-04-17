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

## Configuration Framework

The pipeline now uses a layered configuration framework with this precedence:

1. Dataclass defaults in `config.py`
2. JSON config file overrides
3. Environment variable overrides
4. CLI overrides (for sample size and output path)

### JSON config

Copy and edit `config.example.json`, then run:

```bash
python main.py --config config.example.json
```

### Environment overrides

Use `HEDONIC_` prefixed variables with `__` for nested keys:

```powershell
$env:HEDONIC_DATA__N_SAMPLES = "5000"
$env:HEDONIC_HEDONIC__TEST_SIZE = "0.3"
$env:HEDONIC_OUTPUT_DIR = "output_custom"
python main.py
```

### CLI overrides

```bash
python main.py --config config.example.json --samples 3000 --output-dir output_exp_01
```