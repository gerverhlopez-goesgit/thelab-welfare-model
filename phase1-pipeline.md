# ⚙️ TheLAB — Project Roadmap (Phase 1)

---

## 📘 Logic Model

| Milestone | Status | Deliverable | Notes |
|----------|--------|------------|-------|
| Finalize research questions | Completed | File (Gerver O Hernandez Lopez) | Clear framing |
| Defining the unit of Analysis | In progress | File (Gerver O Hernandez Lopez) | Using Census.gov, zipcode, land registry, EPA, ACS, Zillow, Redfin |
| Defined the metric to value WTP and CV (park utility)* | In progress | File (John Keun Kim, Gerver O Hernandez Lopez) | The economic structure |
| Defined the valuation of how much money bad health is worth | Not started | File (Gerver O Hernandez Lopez, Narges Mariam Abdul) | Mortality added to “being sick” (morbidity) |
| Finalizing the Social Welfare Function* | Not started | File (John Keun Kim) | Calculating benefits minus the damage |
| Phase 1 Completed | In progress | File | |

---

## Environmental Risk Framework

| Milestone | Status | Deliverable | Notes |
|----------|--------|------------|-------|
| Standardize risk metrics | Not started | File (Gerver O Hernandez Lopez, Narges Mariam Abdul) | How exposure converts to loss in welfare? Weighing tests, analysis under uncertain bounds and identification of assumptions considered weak |
| Identify and classify pollution sources | Not started | File | How infrastructure amplifies or mitigates risk |

---

## Data Structure

**Soft deadline:** Savio HPC (high-performance computing) cluster  
Contact: Tianyi Tina Li  
Link: https://www.ocf.berkeley.edu/docs/services/hpc/

| Milestone | Status | Deliverable | Notes |
|----------|--------|------------|-------|
| Pollution dataset | Not started | File (Tianyi Tina Li, Zhuoni Huang) | EPA / PM2.5 / TRI* |
| Housing dataset | In progress | File (Tianyi Tina Li, Zhuoni Huang, Gerver O Hernandez Lopez) | Zillow / Redfin / public housing records |
| Amenity dataset | Not started | File (Tianyi Tina Li, Zhuoni Huang) | OpenStreetMap (OSM), USDA Economic Research Service, Rausser’s College* |
| Demographic controls* | Not started | File (Tianyi Tina Li, Zhuoni Huang) | American Community Surveys* |
| Combining the datasets / data manipulation | Not started | File (Tianyi Tina Li, Zhuoni Huang) | This should include regressions ready with a master dataframe |

---

## Estimating and Building the Model

**Owners:** Narges and Gerver  
**Deadline:** Apr 4, 2026

| Milestone | Status | Deliverable | Notes |
|----------|--------|------------|-------|
| Generation of the Hedonic Model | Not started | File (John Keun Kim, Gerver O Hernandez Lopez) | Regression. To measure people we use log. ln(p) model |
| Added fixed effects | Not started | File | Adding variables such as time in the neighborhood |
| Checked for robustness | Not started | File | Adding alternative specifications |
| Analyzed sensitivity | Not started | File | Think of it as scaling / data normalization / standardization (z-score) |
| Worked on causal strategy | Not started | File | Think of it as adjusting the range or the distribution of the variables |

---

## Content Integration

| Milestone | Status | Deliverable | Notes |
|----------|--------|------------|-------|
| Drafting the introduction | In progress | File (Gerver O Hernandez Lopez) | |
| Drafted framework of the concept | In progress | File | |
| Research design and implementation | In progress | File | |
| Phase 1 - Final draft | Not started | File | |

---

## Notes

- *CV = Non market valuation. We use hypothetical values.*  
- *SWF = is used to aggregate how happy each person is to find a number for how better off everyone is.*  
- *TRI = Toxics Release Inventory (TRI) Program. Link: https://www.epa.gov/toxics-release-inventory-tri-program*  
- *Rausser College main contacts will be added briefly*  
- *Demographic Controls = just selecting the kinds of people (groups)*  
- *American Community Surveys = 5 years or 26 years.*
