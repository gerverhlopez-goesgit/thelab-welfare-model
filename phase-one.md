# Environmental Impact — Pricing a Location

This is a work in progress… will keep you updated once this draft is completed. Will walk you through during our next meeting - Gerver.

---

## Main topic:

Prices under environmental harm and the potential for development: once we account for the baseline of current amenities, environmental health risk, and expected development. 

In short terms: Current Risks vs. Future Rewards

---

## Motivation:

How should we price a location's welfare value when both the damage derived from environmental health and future amenities matter?

This is welfare (WTP = willingness to pay).

Some places are cheap because of the disparities in infrastructure and health outcomes, but these places may also be “promising” because development will come. This includes new housing, jobs, transportation, grocery stores.

The bad: environmental health risks (pollution) lower property values.

The good: current amenities and potential for development (public transportation, grocery stores, and housing permits) that are driving the value up.

The goal: we are trying to quantify the Willingness to Pay (WTP) the specific currency amount people sacrifice to either avoid risks or gain access to future growth.

---

## Main research question:

Can we quantify, in currency, the net welfare value in an area with unknown or known health risks related to the environment once we account for the current amenities and potential expected development?

---

## Three methods to quantify the welfare (these are all legit):

1. Using the Hedonic model WTP (as we reveal preferences):  
   - We could technically use housing prices or the price of rent to make an inference of the WTP for cleaner air/ low health related risks and for the amenities.  

2. The Compensating Variation:  
   - This is a method where the central question is “how much money would a household need to be compensated for them to accept to move into a higher known health/ risk area, but we hold their utility (satisfaction) constant?”  

3. A simple math equation  
   - Net Welfare ($) = Amenity Value ($) - Health Damage Value ($)  
   - The previous equation could include values that account for equity and the distribution of weight.

---

## Three Hypothesis (must be testable):

1. H1 If we hold amenities constant, places with higher environmental health risks will have lower offerings/sale prices equivalent to a negative WTP for risk. This is how negative externalities/implicit costs change the prices of a location approach.  

2. H2 People are willing to pay more for a bad spot today because they expect development / amenities to grow in the future. Imagine a house in a location with unhealthy air quality. This would be a bad thing, but if it is closer to a train station, a park, and jobs, then the price might not change that much.  

3. H3 Lower income households accept higher risk to save money. For every unit of money they save, the more danger and risk they face to their health outcomes compared to wealthier households. This is the sorting/inequality. Only those with the means and high WTP are able to live in better conditions.

---

## The Null Hypothesis:

The known environmental risks are not priced into the value of a location once we control for the characteristics in the neighborhood and the potential for development in the future. 

---

## How can we identify causality:

### 1. Difference in Differences

This will be the using a “shock” approach:

- We could track the opening or the closing of an industrial complex  
- We could also trace the change on regulations  
- Look for any changes in the air quality (enforcement)  
- Are there any new amenities? New transportation, schools, grocery stores openings?

After we account for similar factors, we can estimate the following questions:

- Did prices/rents change in affected vs. unaffected areas?  
- Did health outcomes change? (reports of asthma, mortality, ER visits)?  

---

### 2. Regression Discontinuity / Boundary

We could compare homes across previously set boundaries:

- School attendance  
- Industrial or manufacturing zone  
- Very dirty and very dangerous places  

Think of this as comparing South Oakland to North Oakland or Compton in Los Angeles to Huntington Beach.

---

### 3. Using Instrumental Variables  

- Two things can happen at the same time. For example: a place can have dirty air, but the houses there cost less money. Is the air the only reason the price is low?  
- Distance from highways  
- Weather and the wind  

---

This would be the design for a small scale “pilot” version. The purpose is to highlight risk factors of land management to help people make more informed decisions in purchasing.

---

## How we plan to measure it

### 1. Using outcome as a variable   
- Using logs of the home sale prices per transaction if possible or using Zillow and Redfin  
- Looking into the rent transactions if any (The Rent Index)  

---

### 2. Exposure to environmental risks  

- Measures of the PM 2.5, NO2, The ozone. For this, we could use the EPA or satellite imagery.  
- The proximity to refineries, main roads, and the Toxic Release Inventory (TRI)  
- Are there any hazardous sites?  
- Health Risk Index  

---

### 3. Future development  

- Observe changes in services such as new schools, universities, grocery stores, transit, and permits  
- Use proxies to predict future development  

Examples:  
- Clouds = proxy → rain (future outcome)  
- Rail construction → future population growth  
- Job expectations → migration signals  

---

## Development Index

permits + planned transit + jobs expected + zoning regulations + institutional expansion

---

## Controls

- Test scores  
- Crime ratio  
- Commuting times, public transit  
- Demographics (income, education, race)  
- Housing characteristics (year built, lot size)

---

## TLDR:

| Category | Data Source |
|----------|------------|
| Price (Outcome) | Zillow/ Redfin, Rent index, public records |
| Environmental Risks | PM2.5, NO2, Ozone (EPA/Satellite), TRI proximity |
| Potential for Development | Permits, transit, institutional expansion |
| Controls | Crime, schools, demographics, housing characteristics |

---

## Quant (Mathematical Framework)

### Hedonic Model:

ln(price_it) = β1 Risk_it + β2 PotentialforDevelopment_it + β3 (Risk × PotentialforDevelopment)_it + X_it + α_area + γ_t + ε_it

- β1 → WTP to avoid risk (risk discount)  
- β2 → speculation premium  
- β3 → “hope factor”

---

## Welfare Conversion

WTP to reduce risk = -β1 × P

Where:
- β1 = effect of risk  
- P = property value  

---

## Remember:

Welfare does not mean government programs.  
It represents how happy or safe a person is based on preferences.

---

## Phase One Outputs

1. Welfare framework  
2. Map (risk vs development)  
3. Regression analysis + causal design  
4. Strategy for next phase  

---

## Final Thought

This helps determine whether improving environmental conditions is worth the cost in terms of real welfare gains.
