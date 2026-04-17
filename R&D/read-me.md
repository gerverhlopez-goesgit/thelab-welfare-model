# Core Terminology & Concepts

This document defines the key terminology required for the development of our urban intelligence platform. It integrates concepts from environmental economics, data science, applied mathematics, and political economy.
Please do reach out of you find yourself wondering our questioning what to do next or how to proceed. - Gerver
---

## I. Economic Theory (Core Concepts)

### Hedonic Pricing Model
A method that decomposes a good’s price (e.g., housing) into the value of its attributes (structural, neighborhood, environmental).

---

### Willingness to Pay (WTP)
The maximum amount an individual is willing to pay to obtain a good or avoid a negative outcome (e.g., pollution).

---

### Compensating Variation (CV)
The amount of money required to compensate an individual for a loss in utility while keeping their welfare constant.

---

### Consumer Surplus
The difference between what consumers are willing to pay and what they actually pay.

---

### Externalities
Costs or benefits not reflected in market prices (e.g., pollution as a negative externality).

---

### Negative Externality
A cost imposed on others (e.g., air pollution reducing health outcomes).

---

### Welfare (Economic Definition)
A measure of well-being based on preferences, utility, and choices — not government programs.

---

### Social Welfare Function (SWF)
A function that aggregates individual welfare into a measure of overall societal well-being.

---

### Sorting (Spatial Sorting)
The process by which individuals choose locations based on income, preferences, and constraints.

---

### Environmental Inequality
Unequal exposure to environmental risks across socioeconomic groups.

---

## II. Econometrics & Causal Inference

### Regression Analysis
A statistical method used to estimate relationships between variables.

---

### Log-Linear Model (ln(P))
A model where the dependent variable is in logarithmic form (common in housing price models).

---

### Coefficient (β, γ, δ)
Represents the marginal effect of a variable on the dependent variable.

---

### δₖ (Environmental Risk Coefficient)
Captures the implicit price of environmental risk in the hedonic model.

---

### Fixed Effects
Controls for unobserved characteristics across time or space.

---

### Endogeneity
When an explanatory variable is correlated with the error term.

---

### Omitted Variable Bias
Bias caused by leaving out relevant variables.

---

### Difference-in-Differences (DiD)
A method that compares changes across treated and control groups over time.

---

### Instrumental Variables (IV)
A method used to address endogeneity using an external variable (instrument).

---

### Regression Discontinuity Design (RDD)
A causal method using cutoff thresholds (e.g., zoning boundaries).

---

### Robustness Checks
Tests to verify that results hold under different model specifications.

---

### Sensitivity Analysis
Testing how results change when assumptions or inputs are modified.

---

## III. Environmental & Spatial Concepts

### PM2.5
Fine particulate matter (major air pollutant affecting health).

---

### NO₂ (Nitrogen Dioxide)
A pollutant typically associated with traffic and industrial activity.

---

### Ozone (O₃)
A pollutant formed through chemical reactions in sunlight.

---

### Toxic Release Inventory (TRI)
A dataset tracking industrial chemical releases.

---

### Exposure
The degree to which individuals come into contact with environmental hazards.

---

### Environmental Risk Index
A composite measure of pollution and hazard exposure.

---

### Spatial Data
Data that includes geographic location (coordinates, maps).

---

### Geocoding
Converting addresses into geographic coordinates.

---

### GIS (Geographic Information Systems)
Tools used to analyze and visualize spatial data.

---

### Spatial Autocorrelation
When nearby observations are correlated.

---

## IV. Development & Urban Economics

### Development Potential
The likelihood that an area will experience growth or investment.

---

### Building Permits
Indicators of future construction and development activity.

---

### Zoning Regulations
Rules governing land use (residential, commercial, industrial).

---

### Transit Accessibility
Access to transportation infrastructure (rail, bus, etc.).

---

### Amenities
Local features that increase desirability (parks, grocery stores, schools).

---

### Gentrification
The process of neighborhood upgrading and demographic change.

---

### Base Flood Elevation (BFE)
A measure used in flood risk assessment.

---

## V. Data Science & Modeling

### Data Pipeline
The process of collecting, cleaning, and transforming data.

---

### Raw Data
Unprocessed data as collected from sources.

---

### Clean Data
Processed data ready for analysis.

---

### Feature Engineering
Creating new variables from existing data.

---

### Master Dataset
A merged dataset combining all relevant sources.

---

### Index Construction
Combining multiple variables into a single metric (e.g., Development Index).

---

### Normalization / Standardization
Scaling variables (e.g., z-scores).

---

### Missing Data
Data points that are not observed or recorded.

---

### API (Application Programming Interface)
A way to programmatically access data (e.g., NOAA, EPA).

---

## VI. Interpretation & Output

### Marginal Effect
The change in the dependent variable from a one-unit change in an independent variable.

---

### Price Capitalization
The process by which attributes (e.g., risk) are reflected in prices.

---

### Risk Discount
Reduction in property value due to environmental risk.

---

### Development Premium
Increase in value due to expected future growth.

---

### Welfare Estimate ($)
The monetary value of gains or losses in well-being.

---

### Net Welfare
```math
Net Welfare = Amenity Value - Health Damage
