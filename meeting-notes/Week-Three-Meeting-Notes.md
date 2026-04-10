## Narges, Zhuoni, and Gerver. Week 3 Notes - Sat 04, 2026

The structure of our platform are:  
physical characteristics of the home, the current neighborhood amenities, the environmental hazards, and the indicators of future growth.

The model John created treats the properties price as in itemized receipt of the unique individual feature.

In the original equation, the Net Welfare is calculated as the Amenity Value ($) minus the Health Damage Value ($) and the dollar amount a household is willing to pay for safety is extracted by multiplying the risk coefficient (beta 1) by the total property price (P).

---

## Our measurement and data extraction categories

| Category | Variables to Measure | Potential Data Sources |
|----------|---------------------|------------------------|
| Outcome (Price) | Logs of home sale prices per transaction or Rent Index | Zillow, Redfin, or local real estate transaction logs |
| Environmental Risk | PM 2.5, NO2, Ozone, and proximity to TRI sites or refineries | EPA databases, satellite imagery, and Toxic Release Inventory (TRI) |
| Development Potential | Building permits, proposed transit projects, and grocery store penetration | Municipal planning portals, zoning regulations, and institutional expansion plans |
| Controls | Crime ratios, school test scores, demographics, and commuting times | Census Bureau, local police departments, and school district reports |

---

As for the data to accurately reflect the environmental impact rather than any unrelated market trends, we set on using the following econometric methods:

1. Difference in Differences (the shock approach): will measure the price changes in an area before and after a shock, such as opening or closing an industrial or pollutant firm.  
2. Regression Discontinuity (boundary): we can compare nearly identical homes that could sit in opposite regulations or at the limits of the pollutant firm.  
3. Using instrumental variables: we want to use wind patters or the distance from the freeways/ main streets to isolate the air quality and its impact from other variables in the neighborhood.  

---

## The chemical particles and main pollutants:

### 1. PM 2.5:
It is considered the most critical variable our urban health model. These particles can penetrate the lungs and into the bloodstream, causing respiratory and cardiovascular issues.  

In our model an increase PM 2.5 would lead to a percentage base drop in home prices as it would be an indicator of "contaminated air"

---

### 2. Nitrogen Dioxide (NO_2) and Ozone (O_3)
These are pollutants that would serve as the standard measurement for the exposure to environmental risks.  
These are related to the traffic and how close households are to the major freeways. That is the high concentration of these gases will be used as "proxy" for locations with poor quality, which should lead to lower or negative Willingness to Pay (WTP) even among wealthier households who would have the means and resources to move elsewhere.

---

### 3. Finally, the TRI - Toxic Release Inventory
The survey tracks specific chemicals that pose a threat to the human health and the environment.  
These would include lead, mercury and any other carcinogens that are released from industrial or refineries complexes.  

Our theory is that the opening or closing of a facility that handles these chemicals would act as a shock which would allow us to measure exactly how much the market punishes the proximity to the risks related to toxics.  

This also accounts for the physical proximity to what are considered very dirty and very dangerous places with would create a variable "Value Penalty).  

For example, living near a refinery or a hazardous location would result in the decline of the property value due to the health risks associated with the environmental hazard and the negative aesthetic of the pollutants or the industrial zones in the vicinity.  

---

## Particle/Factor Data

| Particle/Factor | Data Source | Impact on Price (β1) |
|----------------|------------|----------------------|
| PM 2.5 | EPA / Satellite | Negative (Health Penalty) |
| NO2 / Ozone | EPA Monitoring | Negative (Location Discount) |
| TRI Site Proximity | TRI Database | Steep Negative (Risk Penalty) |
| Refinery Emissions | Direct Proximity | Negative (Negative Amenity) |

---

The infrastructure will be treated as "counterweight" to the environmental risks. Therefore, pollution creates a Value Penalty, and infrastructure could generate Potential for Development Index that can offset those losses.  

---

Any questions please don't hesitate to ask!
