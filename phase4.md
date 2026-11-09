# Phase 4: Descriptive Analytics

## 1. Purpose, source and analytical scope

This phase summarises tourism demand, visitor value and hospitality utilisation to support the business questions in [Phase 1](phase1.md). It builds on [Phase 2](phase2.md) and the [shared project context](https://docs.google.com/document/d/1D7XlrIAmvjOiAvelTXcPIIVQPm9oTd76nJ1OJ8jI_tE/edit).

The repository has no Phase 3 cleaned dataset at the time of this contribution. The input is therefore the unchanged `data/raw/Tourism_Hospitality_Industry_Analysis.csv`: **500 records, 23 variables, 20 countries, 56 cities, 2020–2024**. The script checks completeness, exact duplicates, finite numeric values, time codes, percentages and the revenue identity before calculating statistics. It does not substitute for Phase 3; rerun against an agreed prepared input if that phase later changes the data.

Each row is an observed destination-period record carrying a visit-purpose and hotel-tier label. Some city-year-month keys repeat and segment exclusivity is undocumented. Summed arrivals and revenue below are **sums across observed records**, not verified country totals, unique visitor counts or full-year market totals. Group coverage is uneven, so rankings show record counts and means alongside sums. Means reduce the influence of differing record counts but do not correct sample composition or selection bias.

Phase 2 found evidence consistent with synthetic data (near-uniform distributions and weak relationships), rather than externally verified tourism statistics. Interpret these results as an analytics demonstration; country rankings and apparent seasonality require validation with real, representative data.

## 2. Measures and conventions

| Variable type | Appropriate measures and treatment |
|---|---|
| Ratio measures: arrivals, spend, stay, occupancy, hotels, prices, revenue and other counts | Mean, median, range, sample variance, sample SD, CV, quartiles, P10/P90/P95, adjusted skewness and unbiased excess kurtosis |
| Nominal: country, city, purpose | Frequency, percentage and all tied modes; no numeric averages of labels |
| Hotel tier | Ordered frequencies for 1–5 stars; Unrated is a separate classification, never zero stars |
| Year and cyclical month | Ordered frequency and grouped KPI summaries; no mean year/month or CV of their numeric codes |
| Subjective ordinal scores: infrastructure, waste management, satisfaction | Median, quartiles, percentiles and frequencies; no assumed equal spacing or meaningful ratio scale |

- Variance uses **n−1**, has squared units, and SD has the original unit. SD and range of a percentage are in **percentage points**. These are descriptive statistics of records, not standard errors or forecast intervals.
- CV = 100 × sample SD / mean, used only for positive ratio measures. It compares relative dispersion across units; it does not measure uncertainty or profitability.
- Percentiles use linear interpolation at index (n−1)p, equivalent to NumPy `method='linear'` or Excel `PERCENTILE.INC`. An interpolated quartile need not be an observed value.
- Adjusted Fisher–Pearson sample skewness is reported; positive values indicate a longer right tail. Bias-corrected Fisher **excess** kurtosis uses a normal reference of 0 (not 3). Negative kurtosis indicates a flatter/lighter-tailed shape relative to normal, not proof of low business risk. Phase 2 used unadjusted moments, so small rounding differences are expected.
- Numeric modes include every tied most-frequent value in `ratio_summary.csv`; if all values occur once, the result is “No repeated value.” Repeated rounded continuous values have little planning value; mean and median are the main summaries.
- Following the Phase 2 identity, `Tourism_Revenue_USD = Number_of_Tourists × Tourist_Spending_USD / 1000` within 0.011 stored units, revenue is **interpreted as thousand USD**. The same scale is assumed for eco-revenue; this is inferred, not publisher-confirmed. Original column names and raw values remain intact; outputs explicitly label units.
- Group occupancy and room-price averages weight each record equally. Hotel counts are not room counts, and available room-nights are absent, so a true pooled room occupancy rate or a room-weighted ADR/RevPAR cannot be calculated. Tourist-weighted spending = Σ(arrivals × spend) / Σ(arrivals); it is separate from the simple mean of record spending values.

## 3. Central tendency and dispersion

| Variable | Mean | Median | Range | Sample variance | Sample SD | CV % |
|---|---|---|---|---|---|---|
| Number_of_Tourists | 125,263.88 | 124,629.00 | 149,073.00 | 1,852,216,153.06 | 43,037.38 | 34.36 |
| Tourist_Spending_USD | 2,796.04 | 2,894.23 | 4,482.77 | 1,812,494.66 | 1,346.29 | 48.15 |
| Average_Length_of_Stay | 8.67 | 8.90 | 13.00 | 13.28 | 3.64 | 42.03 |
| Hotel_Occupancy_Rate | 64.84 | 64.10 | 49.80 | 212.64 | 14.58 | 22.49 |
| Number_of_Hotels | 273.62 | 273.50 | 448.00 | 16,646.79 | 129.02 | 47.15 |
| Average_Room_Price_USD | 273.98 | 281.08 | 449.32 | 16,321.10 | 127.75 | 46.63 |
| Tourism_Revenue_USD | 349,737.92 | 304,511.41 | 917,281.39 | 45,856,319,550.03 | 214,140.89 | 61.23 |

Units follow section 2 and `ratio_summary.csv`; revenue figures above are in thousand USD.

- **Demand:** Mean arrivals are **125,264**, close to median **124,629**, with SD **43,037** and CV **34.4%**. A typical record is near 125,000 arrivals, but variation between records is material. A single average is insufficient for local staffing; use the spread alongside destination-specific coverage.
- **Visitor value:** Average record spending is **$2,796.04 per tourist** (median **$2,894.23**), with CV **48.1%**. Spending varies more proportionately than arrivals, so visitor volume alone is an incomplete marketing KPI. The tourist-weighted pooled spending is **$2,792.01**; it answers a different question from the equal-record mean.
- **Hospitality:** Mean occupancy is **64.84%**, median **64.10%**, and SD **14.58 percentage points**. The equal-record mean unoccupied share is 35.16%, but this is neither a pooled vacancy rate nor evidence that building more hotels is warranted.
- **Revenue:** Mean record revenue is **349,737.92 thousand USD**, above median **304,511.41 thousand USD**. CV is **61.2%**, higher than arrivals and spending because revenue combines both. Use the median to describe a typical record and the mean for an arithmetic average; neither establishes future revenue.

## 4. Quartiles, percentiles and shape

| Variable | P10 | Q1 | P50 | Q3 | P90 | P95 | Skewness | Excess kurtosis |
|---|---|---|---|---|---|---|---|---|
| Number_of_Tourists | 66,357.30 | 88,694.75 | 124,629.00 | 164,159.50 | 184,401.60 | 193,016.50 | 0.02 | -1.21 |
| Tourist_Spending_USD | 871.53 | 1,590.33 | 2,894.23 | 4,011.59 | 4,548.17 | 4,776.45 | -0.09 | -1.28 |
| Average_Length_of_Stay | 3.59 | 5.57 | 8.90 | 11.70 | 13.71 | 14.30 | -0.06 | -1.15 |
| Hotel_Occupancy_Rate | 44.59 | 52.58 | 64.10 | 77.65 | 85.22 | 87.80 | 0.03 | -1.23 |
| Number_of_Hotels | 91.90 | 165.75 | 273.50 | 379.25 | 451.00 | 471.10 | -0.04 | -1.18 |
| Average_Room_Price_USD | 91.14 | 168.36 | 281.08 | 381.23 | 444.74 | 470.52 | -0.06 | -1.16 |
| Tourism_Revenue_USD | 95,470.13 | 181,456.24 | 304,511.41 | 496,404.08 | 669,540.40 | 745,093.44 | 0.65 | -0.45 |

The middle 50% of arrivals lie between **88,695 and 164,160**; P90 is **184,402**. This is a descriptive reference for comparing observed records, not a 90% service-level demand forecast. Occupancy's middle 50% spans **52.58%–77.65%**, illustrating why managers should review utilisation locally.

Arrivals have skewness **0.016** and excess kurtosis **-1.212**, consistent with the roughly symmetric, flat distribution identified in Phase 2. Revenue has skewness **0.647**: larger values pull the mean above the median. This pattern is consistent with its arithmetic construction from positive arrivals and spending; it is not independent evidence of a high-growth tourism market.

### Frequency distributions and modes

| Purpose | Records | % of records | Mode? |
|---|---|---|---|
| Business | 71 | 14.20 | No |
| Cultural | 64 | 12.80 | No |
| Educational | 80 | 16.00 | Yes |
| Family Visit | 80 | 16.00 | Yes |
| Leisure | 62 | 12.40 | No |
| Medical | 72 | 14.40 | No |
| Religious | 71 | 14.20 | No |

Purpose percentages describe the **share of records**, not the share of individual tourists. Every tied mode is marked. Hotel-tier frequencies, country/city coverage, chronological year/month counts and exact score frequencies are exported in `category_frequencies.csv`. Unrated records remain separate from the star order.

Occupancy bands below are illustrative reporting bands, not industry thresholds:

| Occupancy interval (%) | Records | % of records |
|---|---|---|
| [0, 40) | 0 | 0.00 |
| [40, 50) | 98 | 19.60 |
| [50, 60) | 109 | 21.80 |
| [60, 70) | 89 | 17.80 |
| [70, 80) | 100 | 20.00 |
| [80, 90) | 104 | 20.80 |
| [90, 100] | 0 | 0.00 |

Numeric frequency tables also use fixed arrivals bands of 50,000, spend bands of USD 1,000 and revenue bands of 200,000 thousand USD. Intervals are left-closed and right-open, with the final interval including its upper endpoint. No observations are dropped.

For the ordinal experience indicator, median satisfaction is **7.40**, Q1–Q3 **6.20–8.70**. This provides an experience benchmark without interpreting a score of 8 as twice the satisfaction of 4. Infrastructure and waste-management score summaries are in `ordinal_summary.csv`.

## 5. Interpretation by business question

### Q1. Which destinations and time periods attract the most tourists?

Top five countries by **mean arrivals per observed record**:

| Country | Records | Observed arrivals sum | Mean arrivals | Median arrivals |
|---|---|---|---|---|
| Singapore | 20 | 2,787,643.00 | 139,382.15 | 133,714.50 |
| United Arab Emirates | 14 | 1,917,437.00 | 136,959.79 | 145,638.50 |
| Egypt | 28 | 3,802,594.00 | 135,806.93 | 142,228.50 |
| South Africa | 30 | 4,007,823.00 | 133,594.10 | 131,876.00 |
| Greece | 21 | 2,763,617.00 | 131,600.81 | 140,852.00 |

**Singapore** ranks highest on mean arrivals (139,382; n=20), whereas **China** ranks highest on the observed arrivals sum (4,273,182; n=33). These metrics answer different questions and are sensitive to sample coverage. The highest city mean is **Las Vegas** (161,085; n=3); city comparisons have especially sparse coverage and should be treated cautiously.

| Month | Records | Mean arrivals | Median arrivals |
|---|---|---|---|
| January | 44 | 134,448.86 | 133,626.50 |
| February | 46 | 123,879.87 | 121,001.50 |
| March | 39 | 121,955.92 | 117,661.00 |
| April | 32 | 123,353.56 | 107,593.50 |
| May | 43 | 124,332.53 | 119,166.00 |
| June | 51 | 129,373.18 | 137,896.00 |
| July | 36 | 132,674.56 | 133,667.00 |
| August | 48 | 115,871.90 | 109,658.50 |
| September | 49 | 121,405.12 | 111,842.00 |
| October | 43 | 128,303.05 | 136,483.00 |
| November | 28 | 122,158.68 | 129,396.00 |
| December | 41 | 125,495.90 | 124,763.00 |

**January** has the highest monthly mean (134,449; n=44), and **August** the lowest (115,872; n=48). These pool different countries and years: they do not establish a seasonal peak. A tourism authority should validate patterns in a balanced destination-month series before scheduling promotions. Year summaries are exported with sample sizes; changes are not national growth rates.

### Q2. Which segments and destinations generate the highest economic value?

| Purpose | Records | Equal-record spend (USD) | Tourist-weighted spend (USD) | Mean revenue (USD 000) |
|---|---|---|---|---|
| Business | 71 | 2,922.60 | 3,002.05 | 375,049.15 |
| Educational | 80 | 2,894.98 | 2,877.27 | 365,492.57 |
| Cultural | 64 | 2,822.74 | 2,844.96 | 331,029.79 |
| Medical | 72 | 2,892.09 | 2,822.60 | 349,926.78 |
| Leisure | 62 | 2,819.69 | 2,757.55 | 347,704.33 |
| Religious | 71 | 2,633.62 | 2,640.04 | 328,623.88 |
| Family Visit | 80 | 2,602.78 | 2,623.21 | 346,630.80 |

**Business** has the highest tourist-weighted spending (**$3,002.05**), versus **$2,623.21** for **Family Visit**. **Singapore** has the highest mean revenue per observed country record (**450,219.57 thousand USD**; n=20). These are candidates for examining value-based marketing, subject to better data. Revenue is mechanically determined by arrivals and spending, and acquisition costs and margins are missing, so this analysis cannot establish segment profitability or marketing ROI.

### Q3. Is existing hospitality capacity being used efficiently?

| Country | Records | Mean occupancy % | Mean hotels per record | Mean arrivals |
|---|---|---|---|---|
| Turkey | 22 | 70.54 | 292.64 | 127,061.64 |
| Singapore | 20 | 59.05 | 223.40 | 139,382.15 |

**Turkey** has the highest equal-record mean occupancy (**70.54%**), while **Singapore** has the lowest (**59.05%**). The spread highlights the value of destination-level utilisation reviews, but does not measure technical efficiency, room shortages or the return on expansion.

| Measure X | Measure Y | Pearson r |
|---|---|---|
| Number_of_Tourists | Hotel_Occupancy_Rate | -0.03 |
| Number_of_Tourists | Number_of_Hotels | 0.06 |
| Number_of_Hotels | Hotel_Occupancy_Rate | 0.06 |

These small linear associations give little descriptive support for assuming that more hotels or higher arrivals imply higher occupancy in this sample. They do not establish causation or rule out nonlinear relationships. Hotel counts are an incomplete capacity measure: obtain room inventories, available room-nights, guest nights and costs before recommending expansion, closures or pricing changes. Summing repeated hotel counts would double-count stocks; only per-record means are shown.

### Q4. Can tourist demand be predicted?

Phase 4 provides descriptive inputs, not an evaluated forecast. In Phase 6, exclude revenue, eco-revenue and carbon totals from arrivals predictors because they are derived from arrivals. Sparse coverage and the apparent synthetic construction limit expected predictive usefulness. Report validation against a simple baseline rather than treating these descriptive means as a model.

## 6. Business implications and limits

1. Use both typical demand (median) and its spread when discussing staffing; the pooled mean hides substantial record variation.
2. Compare spend per tourist alongside arrivals when examining marketing opportunities; higher revenue alone does not show better profitability.
3. Review low-occupancy observations using actual room-night capacity and local costs before allocating investment. The reporting bands are not decision cutoffs.
4. Validate destination rankings and month patterns on a representative panel before operational use. Per-record averages still mix years, cities and segments.
5. Keep the inferred revenue scale explicit and confirm it with the publisher before using dollar totals in a financial plan. No causal or quantified financial impact is claimed.

## 7. Deliverables and reproduction

Run from the repository root:

```sh
python analysis/phase4_descriptive_analytics.py
```

Python 3.10+ is sufficient; no third-party packages are required. All tables and this report are regenerated deterministically. `notebooks/04_Descriptive_Analytics.ipynb` runs the same script and displays the report.

| File | Contents |
|---|---|
| `analysis/phase4_descriptive_analytics.py` | Validated input, statistical calculations, grouped summaries and report generation |
| `outputs/phase4/ratio_summary.csv` | All 14 ratio measures; central tendency, complete tied modes, dispersion, percentiles and shape |
| `outputs/phase4/ordinal_summary.csv` | Median and percentile summaries for three ordinal scores |
| `outputs/phase4/category_frequencies.csv` | Counts, percentages and modes for categories, time codes and ordinal scores |
| `outputs/phase4/numeric_frequencies.csv` | Fixed-interval frequency distributions for four business KPIs |
| `outputs/phase4/grouped_business_summary.csv` | Country, city, purpose, hotel tier, year and month comparisons with sample sizes |
| `outputs/phase4/capacity_correlations.csv` | Descriptive associations among arrivals, hotel count and occupancy |
| `outputs/phase4/source_checks.txt` | Source hash, dimensions, completeness, duplicate/key and revenue-identity checks |
