# Hedonic Pricing Model: Environmental Shocks and Property Valuation

## 1. Summary 
To assess how historical environmental shocks impacted property values and post-disaster development, we use a **Hedonic Pricing Model**. A hedonic model deconstructs a property's total price into its individual components. It assumes that buyers do not just buy a "house"; they buy a bundle of attributes (e.g., square footage, school district, and environmental safety).

---

## 2. The Hedonic Pricing Equation

In real estate economics, the hedonic price ($P$) is a function of **Structural characteristics** ($S$), **Neighborhood characteristics** ($N$), and **Environmental characteristics** ($E$).

$$\ln(P) = \beta_0 + \sum(\beta_i S_i) + \sum(\gamma_j N_j) + \sum(\delta_k E_k) + \epsilon$$

### Variable Definitions:

* **$\ln(P)$ (The Price):** The natural log of the final market price, allowing for percentage-based valuation analysis.
* **$\beta_0$ (The Base Value):** The baseline price of a property before accounting for specific features or risks.
* **$S_i$ (Structural):** Physical traits like square footage, bedrooms, or a swimming pool.
* **$N_j$ (Neighborhood):** Location traits such as school district ratings or crime rates.
* **$E_k$ (Environmental):** Natural surroundings and risks, including air quality index or flood zone status.
* **$\delta_k$ (Environmental Coefficient):** The specific financial premium or penalty the market attaches to an environmental factor.
* **$\epsilon$ (The Error Term):** Random, unmeasurable human factors like emotional attachment or bidding wars.

---

## 3. Quantifying the Magnitude of Risk

The coefficient $\delta_k$ captures the **marginal willingness to pay (WTP)** to avoid environmental risk. A negative value implies that higher exposure reduces property values.

### Real-World Dynamics:
* **The Disaster:** A severe air pollution event or natural disaster can cause $\delta_k$ to shift rapidly from a positive premium (e.g., a "water view") to a massive negative penalty due to insurance costs and perceived danger.
* **Policy & Shocks:** A reduction in environmental penalties ($\delta_k$) often occurs following new regulations or the closure of an industrial complex.

These cases demonstrate that environmental risk is dynamically priced in housing markets and can shift rapidly following shocks, policy changes, or new information.

### Case I: The Great Smog of London (1952)
* **The Disaster:** A severe air pollution event trapped toxic smog over London, causing thousands of deaths.
* **Hedonic Assessment:** Historically, westerly winds pushed smoke to the East End, resulting in a permanent "pollution penalty" and lower property values.
* **Post-Event Reality:** Following the Clean Air Act of 1956, the environmental penalty ($\delta_k$) for bad air decreased. This led to massive long-term redevelopment and gentrification as the hedonic value of air quality equalized across the city.

### Case II: Hurricane Katrina, Louisiana (2005)
* **The Disaster:** Catastrophic flooding and levee failure that inundated New Orleans.
* **Hedonic Assessment:** Katrina broke the existing housing market, making the penalty for being below sea level the single most dominant factor in valuation.
* **Post-Event Reality:** A massive hedonic premium emerged for **Base Flood Elevation (BFE)**. Homes raised above the floodplain saw values surge, while ground-level slab homes suffered permanent value destruction.

### Case III: Palisades Fire, Los Angeles (2021)
* **The Disaster:** A high-visibility brush fire in a wealthy enclave where Neighborhood ($N$) and Structural ($S$) coefficients (ocean views and luxury estates) are incredibly high.
* **Hedonic Assessment:** Historically, the view premium far outweighed the fire risk penalty.
* **Post-Event Reality:** The penalty is currently manifesting through soaring insurance costs and mandatory brush clearance. New builds are now being designed as fire-resistant "bunkers" to maintain their luxury valuation.

### Case IV: Hurricane Sandy, NY/NJ (2012)
* **The Disaster:** A massive storm surge devastated the Northeastern US coastline.
* **Hedonic Assessment:** Before Sandy, proximity to water was a pure premium. After Sandy, FEMA redrew flood maps, placing properties in "V-Zones" (high velocity wave action).
* **Post-Event Reality:** The market split; homes that invested in resilience (raising foundations) retained their premium, while unmitigated homes took an average **15–20% hit** to market value.
