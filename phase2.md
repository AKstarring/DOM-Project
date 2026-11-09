# Phase 2: Data Understanding

Supporting files:

| File | Contents |
|---|---|
| `data/raw/Tourism_Hospitality_Industry_Analysis.csv` | Raw dataset, unchanged from Kaggle |
| `analysis/phase2_data_understanding.py` | Script that produces every number and figure in this phase |
| `outputs/phase2/metadata_table.csv` | Metadata table (section 3), ready for Excel or the report |
| `outputs/phase2/numeric_profile.csv` | Min, quartiles, mean, SD, CV, skewness and kurtosis of every numeric variable |
| `outputs/phase2/categorical_profile.csv` | Level counts and percentages for every categorical variable |
| `outputs/phase2/correlation_matrix.csv` | Pearson correlation matrix |
| `outputs/phase2/data_quality_checks.txt` | Completeness, structure and consistency checks |
| `outputs/phase2/fig_*.png` | Distributions, correlation heatmap and category coverage charts |

To reproduce, run `python analysis/phase2_data_understanding.py` from the project folder.

---

## 1. Data source

| Item | Detail |
|---|---|
| Dataset | Tourism & Hospitality Industry Analysis Dataset |
| Publisher | Kaggle user `smithmurphy` |
| URL | https://www.kaggle.com/datasets/smithmurphy/tourism-and-hospitality-industry-analysis-dataset |
| File | `Tourism_Hospitality_Industry_Analysis.csv` (73.6 KB; file timestamp 13 Mar 2025) |
| Type | Public secondary dataset (Kaggle) |
| Access | Public download; no login, scraping or paywall bypass |
| Privacy | No PII or PHI. Records are aggregated at the city and month level, with no names, emails, phone numbers or individual tourists. |

### Data sourcing log (for the report appendix)

| Source URL | Date of collection | Tool / method |
|---|---|---|
| https://www.kaggle.com/datasets/smithmurphy/tourism-and-hospitality-industry-analysis-dataset | 9 November 2026 | Direct download of the public ZIP through Kaggle's dataset download endpoint (`curl`), then unzipped. The file was not modified. |

---

## 2. Dataset description

| Property | Value |
|---|---|
| Observations (rows) | **500** (meets the minimum of 500) |
| Variables (columns) | **23** (meets the minimum of 8): 19 numeric and 4 text categorical |
| Geographic coverage | 20 countries, 56 cities (2 to 5 cities per country) |
| Time coverage | Years 2020–2024, all 12 months |
| Unit of observation | One record for one **city in one month** (and year), with a purpose-of-visit segment and a hotel-rating tier |
| Missing values | 0 |
| Duplicate rows | 0 |

**Countries:** Australia, Brazil, Canada, China, Egypt, France, Germany, Greece, India, Italy, Japan, Mexico, Singapore, South Africa, Spain, Thailand, Turkey, United Arab Emirates, United Kingdom and United States. Each country has between 14 records (UAE) and 33 records (Italy, China).

**Variable groups:**

| Group | Variables | Business question |
|---|---|---|
| Location and time | Country, City, Year, Month | Q1, Q4 |
| Demand | Number_of_Tourists, Purpose_of_Visit, Average_Length_of_Stay | Q1, Q2, Q4 |
| Spending and economic value | Tourist_Spending_USD, Tourism_Revenue_USD, Employment_in_Tourism, Contribution_to_GDP_Percent | Q2 |
| Hospitality capacity | Number_of_Hotels, Hotel_Occupancy_Rate, Hotel_Rating, Average_Room_Price_USD | Q3 |
| Accessibility | Number_of_Flights, Airport_Passenger_Traffic, Transport_Infrastructure_Quality | Q4 |
| Sustainability | Eco_Tourism_Revenue_USD, Carbon_Footprint_kg, Waste_Management_Rating | Supporting |
| Experience and popularity | Tourist_Satisfaction_Score, Number_of_Online_Reviews | Q4 |

---

## 3. Metadata table

| # | Variable | Description | Unit | Measurement scale | Data type | Role in analysis | Observed range / levels |
|---|---|---|---|---|---|---|---|
| 1 | Country | Destination country | – | **Nominal** | Categorical | Dimension (geography) | 20 countries |
| 2 | City | Destination city | – | **Nominal** | Categorical | Dimension (geography) | 56 cities |
| 3 | Year | Calendar year of the record | Year | **Interval** | Discrete numeric | Dimension (time) | 2020 – 2024 |
| 4 | Month | Calendar month (1 = Jan … 12 = Dec) | Month | **Ordinal** | Discrete (coded) | Dimension (seasonality) | 1 – 12 |
| 5 | Number_of_Tourists | Tourist arrivals in the city for the month | Persons | **Ratio** | Discrete numeric | **Target** (Phase 6) | 50,887 – 199,960 |
| 6 | Purpose_of_Visit | Main purpose of travel | – | **Nominal** | Categorical | Segment | 7 levels: Business, Cultural, Educational, Family Visit, Leisure, Medical, Religious |
| 7 | Average_Length_of_Stay | Average nights per tourist | Nights | **Ratio** | Continuous | Predictor / KPI | 2.0 – 15.0 |
| 8 | Tourist_Spending_USD | Average spend per tourist | USD | **Ratio** | Continuous | Predictor / KPI | 501 – 4,984 |
| 9 | Hotel_Occupancy_Rate | Share of rooms occupied | % | **Ratio** | Continuous | Capacity-utilisation KPI | 40.0 – 89.8 |
| 10 | Number_of_Hotels | Hotels operating in the city | Count | **Ratio** | Discrete numeric | Capacity predictor | 50 – 498 |
| 11 | Hotel_Rating | Hotel star tier | Stars | **Ordinal** | Categorical (ordered) | Quality tier | Unrated, 1-star … 5-star |
| 12 | Average_Room_Price_USD | Average nightly room rate | USD / night | **Ratio** | Continuous | Pricing KPI | 50.57 – 499.89 |
| 13 | Tourism_Revenue_USD | Tourism revenue (= Tourists × Spending ÷ 1000, see §5) | USD '000 in effect | **Ratio** | Continuous | Economic KPI (derived) | 34,185 – 951,467 |
| 14 | Employment_in_Tourism | People employed in tourism | Persons | **Ratio** | Discrete numeric | Economic impact | 5,009 – 49,918 |
| 15 | Contribution_to_GDP_Percent | Tourism share of GDP | % | **Ratio** | Continuous | Economic KPI | 1.1 – 20.0 |
| 16 | Number_of_Flights | Incoming flights | Count | **Ratio** | Discrete numeric | Accessibility predictor | 505 – 4,997 |
| 17 | Airport_Passenger_Traffic | Airport passengers handled | Persons | **Ratio** | Discrete numeric | Accessibility predictor | 50,801 – 998,202 |
| 18 | Transport_Infrastructure_Quality | Transport quality index | Score 1–10 | **Ordinal** | Index score | Accessibility predictor | 1.0 – 10.0 |
| 19 | Eco_Tourism_Revenue_USD | Eco-tourism revenue (5–30 % of tourism revenue) | USD '000 in effect | **Ratio** | Continuous | Sustainability KPI (derived) | 2,299 – 228,408 |
| 20 | Carbon_Footprint_kg | Tourism carbon emissions (100–500 kg per tourist) | kg CO₂ | **Ratio** | Continuous | Sustainability KPI (derived) | 6.3 M – 99.9 M |
| 21 | Waste_Management_Rating | Waste-management rating | Score 1–10 | **Ordinal** | Index score | Sustainability indicator | 1.0 – 9.9 |
| 22 | Tourist_Satisfaction_Score | Average tourist satisfaction | Score 5–10 | **Ordinal** | Index score | Experience KPI / predictor | 5.0 – 10.0 |
| 23 | Number_of_Online_Reviews | Online reviews of the destination | Count | **Ratio** | Discrete numeric | Popularity predictor | 110 – 9,979 |

### Measurement scale summary

| Scale | Count | Variables |
|---|---|---|
| Nominal | 3 | Country, City, Purpose_of_Visit |
| Ordinal | 5 | Month, Hotel_Rating, Transport_Infrastructure_Quality, Waste_Management_Rating, Tourist_Satisfaction_Score |
| Interval | 1 | Year |
| Ratio | 14 | Number_of_Tourists, Average_Length_of_Stay, Tourist_Spending_USD, Hotel_Occupancy_Rate, Number_of_Hotels, Average_Room_Price_USD, Tourism_Revenue_USD, Employment_in_Tourism, Contribution_to_GDP_Percent, Number_of_Flights, Airport_Passenger_Traffic, Eco_Tourism_Revenue_USD, Carbon_Footprint_kg, Number_of_Online_Reviews |
| **Total** | **23** | |

### Justification of the scale choices that can be argued

- **Year: interval.** Differences are meaningful (2024 − 2020 = 4 years), but year 0 is not a true zero, so ratios such as "2024 is 1.002 × 2020" mean nothing.
- **Month: ordinal.** Months have a natural order, but the scale is cyclical: December is next to January, not 11 units away from it. For modelling, Month should be treated as a category or as a season, not as a linear number.
- **Hotel_Rating: ordinal.** 1-star < 2-star < … < 5-star is ordered, but the gap between tiers is not equal. "Unrated" is a missing classification rather than "0 stars", so it is kept as a separate level and not placed at the bottom of the scale.
- **Rating and score variables (Transport infrastructure, Waste management, Satisfaction): ordinal.** These are subjective index scores. A rise from 4 to 5 is not guaranteed to be the same improvement as a rise from 8 to 9. By convention they may be *treated* as approximately interval when computing means (Phase 4), and we state that assumption.
- **Hotel_Occupancy_Rate and Contribution_to_GDP_Percent: ratio.** Percentages have a true zero (0 % occupancy means no rooms are occupied), and 80 % occupancy is twice 40 %.
- **Counts and money (tourists, hotels, flights, revenue, price): ratio.** They have a true zero and ratios are meaningful.

---

## 4. First look at the variables

Full figures are in `outputs/phase2/numeric_profile.csv` and `outputs/phase2/categorical_profile.csv`.

| Variable | Mean | Median | Std dev | CV % | Skewness |
|---|---|---|---|---|---|
| Number_of_Tourists | 125,264 | 124,629 | 43,037 | 34.4 | 0.02 |
| Tourist_Spending_USD | 2,796 | 2,894 | 1,346 | 48.1 | −0.09 |
| Average_Length_of_Stay | 8.67 | 8.90 | 3.64 | 42.0 | −0.05 |
| Hotel_Occupancy_Rate | 64.8 | 64.1 | 14.6 | 22.5 | 0.03 |
| Number_of_Hotels | 274 | 274 | 129 | 47.2 | −0.04 |
| Average_Room_Price_USD | 274 | 281 | 128 | 46.6 | −0.06 |
| Tourism_Revenue_USD | 349,738 | 304,511 | 214,141 | 61.2 | 0.64 |
| Tourist_Satisfaction_Score | 7.44 | 7.40 | 1.45 | 19.4 | 0.06 |

**Categorical balance:**

- *Purpose_of_Visit* is roughly balanced: Educational and Family Visit have 80 records each (16 %), and Leisure has 62 (12.4 %).
- *Hotel_Rating* is roughly balanced: 5-star has 91 records, 2-star has 73, and Unrated has 82.
- *Year* has between 86 records (2021) and 116 (2023).
- *Month* has between 28 records (November) and 51 (June).

No category is so rare that it cannot be analysed. Some cities have only 2–3 records, so we will compare cities mainly at country level, or aggregated across years.

---

## 5. Data quality assessment

Full output is in `outputs/phase2/data_quality_checks.txt`.

| Check | Result | Consequence for Phase 3 |
|---|---|---|
| Missing values | 0 cells | No imputation needed |
| Duplicate rows | 0 | No rows to remove |
| City–country mapping | Each city maps to exactly one country | Consistent |
| Data types | All numeric columns parse as numbers. Year and Month are stored as integers. | Convert Month and Hotel_Rating to ordered categories, and Year and Month to a date |
| Repeated (City, Year, Month) keys | 30 keys repeat, covering 61 rows | A row is a segment record, not a unique city-month panel cell. Do **not** treat these rows as duplicates: they differ in every measure. |
| Panel coverage | 500 of 3,360 possible city-month cells | The time series per city are sparse, so seasonality analysis should aggregate across cities and years |
| Hotel_Rating within city | Every city has records under several rating tiers | Rating describes the record, not a fixed city attribute |
| **Tourism_Revenue_USD is derived** | Equals Number_of_Tourists × Tourist_Spending_USD ÷ 1000 exactly, to the cent | The column is effectively in **thousand USD**. Relabel it in Phase 3 (e.g. `Tourism_Revenue_USD_000`). |
| **Eco_Tourism_Revenue_USD is derived** | Always 5 %–30 % of Tourism_Revenue | Use it as a share of revenue, not as an independent measure |
| **Carbon_Footprint_kg is derived** | Always 100–500 kg × Number_of_Tourists | Report it per tourist |
| Airport passengers vs tourists | 36 rows have fewer airport passengers than tourist arrivals; flights and passengers are uncorrelated (r = −0.03) | Possible in principle (land arrivals), but treat the accessibility variables with caution |
| Distribution shape | Nearly every numeric variable is flat (skewness ≈ 0, excess kurtosis ≈ −1.2), i.e. **uniformly distributed** between a fixed minimum and maximum (see `fig_distributions.png`) | Few or no statistical outliers are expected under IQR or Z-score tests in Phase 3. Only the derived revenue, eco-revenue and carbon columns are right-skewed. |

---

## 6. Important finding: the dataset is synthetic, and what that means for later phases

The evidence in section 5 indicates that this is a **simulated (synthetic) dataset**, not real tourism statistics:

1. Almost every numeric variable follows a uniform distribution between round bounds (e.g. tourists 50k–200k, occupancy 40–90 %, hotels 50–500). Real tourism data is typically right-skewed, with a few very large destinations.
2. The variables are statistically independent of each other. The only correlations above |0.2| are among the columns calculated from tourists and spending (`fig_correlation_heatmap.png`).
3. Values that should be linked in reality are not. For example, flights and airport passengers have r = −0.03. Hotel rating and room price are not linked either.

**Association with the planned Phase 6 target (Number_of_Tourists):**

| Predictor type | Result |
|---|---|
| Legitimate predictors (hotels, flights, passengers, infrastructure, reviews, satisfaction, price, year, month, etc.) | All have \|r\| < 0.07 |
| Country, city, purpose, rating, year, month | One-way ANOVA p-values from 0.54 to 0.81: no significant difference in arrivals between groups |
| Revenue, eco revenue, carbon footprint | r = 0.45–0.64, but only because they are **calculated from** tourist numbers. Using them would be target leakage. |

### Implications (to decide as a group before Phases 4–6)

- **Phases 3–5 can go ahead as planned.** Cleaning, descriptive statistics, visualisations and the Tableau dashboard all work on this data, and the 500 × 23 size meets the requirements.
- **Business Question 4 / Phase 6 (predicting tourist arrivals) will probably give a model with R² close to 0** when only legitimate predictors are used. That is a valid and reportable result: the model says these destination and time variables do not explain demand. The report should explain it rather than hide it. The leakage columns must be excluded.
- The data's synthetic nature must be stated as a **limitation** in the report. Business recommendations in Phase 7 should then be framed as a demonstration of the method, not as real-world market facts.
- Alternatives, if the group prefers a model with signal:
  - (a) Keep this dataset and predict a target with a real structural relationship. For example, predict Tourism_Revenue from tourists and spending; this mainly confirms the formula, so the business story is weaker.
  - (b) Replace the dataset with real open data (e.g. UN Tourism / World Bank arrivals, or a real hotel-booking dataset) before Phase 3 starts.

---

## 7. Phase 2 summary

- The data comes from a public Kaggle dataset with 500 observations and 23 variables, covering 20 countries and 56 cities over 2020–2024. It meets the 500 × 8 minimum.
- The metadata table classifies every variable: 3 nominal, 5 ordinal, 1 interval and 14 ratio.
- The data is complete: no missing values and no duplicate rows. The main Phase 3 tasks are type conversions, relabelling the revenue unit, and handling the derived columns.
- Three columns are derived from tourist arrivals, and the data appears synthetic with near-independent uniform variables. This limits what the predictive model in Phase 6 can find and must be acknowledged in the report.
