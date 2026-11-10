"""Reproduce Phase 4 using Python 3.10+ and the standard library only.

Run from any directory: python analysis/phase4_descriptive_analytics.py
Raw data is read without modification. See phase4.md for statistical conventions.
"""

import calendar
import csv
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path
import statistics as st

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/Tourism_Hospitality_Industry_Analysis.csv"
OUT = ROOT / "outputs/phase4"
RATIO_UNITS = {
    "Number_of_Tourists": "persons per record",
    "Average_Length_of_Stay": "nights per tourist",
    "Tourist_Spending_USD": "USD per tourist",
    "Hotel_Occupancy_Rate": "% (SD/range in percentage points)",
    "Number_of_Hotels": "hotels per record",
    "Average_Room_Price_USD": "USD per night",
    "Tourism_Revenue_USD": "thousand USD (inferred)",
    "Employment_in_Tourism": "persons per record",
    "Contribution_to_GDP_Percent": "% (SD/range in percentage points)",
    "Number_of_Flights": "flights per record",
    "Airport_Passenger_Traffic": "passengers per record",
    "Eco_Tourism_Revenue_USD": "thousand USD (inferred)",
    "Carbon_Footprint_kg": "kg per record",
    "Number_of_Online_Reviews": "reviews per record",
}
SCORES = ["Transport_Infrastructure_Quality", "Waste_Management_Rating",
          "Tourist_Satisfaction_Score"]
DIMENSIONS = ["Country", "City", "Purpose_of_Visit", "Hotel_Rating", "Year", "Month"]


def percentile(values, p):
    """Linear interpolation at (n-1)*p/100 (Excel PERCENTILE.INC / NumPy linear)."""
    a = sorted(values)
    h = (len(a) - 1) * p / 100
    lo, hi = math.floor(h), math.ceil(h)
    return a[lo] + (a[hi] - a[lo]) * (h - lo)


def describe(name, values, unit):
    n = len(values)
    mean = st.mean(values)
    m2 = st.mean([(x - mean) ** 2 for x in values])
    m3 = st.mean([(x - mean) ** 3 for x in values])
    m4 = st.mean([(x - mean) ** 4 for x in values])
    counts = Counter(values)
    peak = max(counts.values())
    modes = sorted(x for x, count in counts.items() if count == peak)
    # Continuous data may have accidental ties; expose all modes instead of selecting one.
    return dict(
        Variable=name, Unit=unit, Count=n, Mean=mean, Median=st.median(values),
        Modes="; ".join(f"{x:g}" for x in modes) if peak > 1 else "No repeated value",
        Mode_Frequency=peak, Number_of_Modes=len(modes) if peak > 1 else 0,
        Min=min(values), Max=max(values), Range=max(values) - min(values),
        Sample_Variance=st.variance(values), Sample_SD=st.stdev(values),
        CV_Percent=100 * st.stdev(values) / mean if mean else "",
        P10=percentile(values, 10), Q1=percentile(values, 25),
        Q3=percentile(values, 75), P90=percentile(values, 90),
        P95=percentile(values, 95), IQR=percentile(values, 75) - percentile(values, 25),
        Adjusted_Skewness=(math.sqrt(n * (n - 1)) / (n - 2) * m3 / m2**1.5
                           if n > 2 and m2 else ""),
        Unbiased_Excess_Kurtosis=((n - 1) / ((n - 2) * (n - 3)) *
                                  ((n + 1) * (m4 / m2**2 - 3) + 6)
                                  if n > 3 and m2 else ""),
    )


def write_csv(filename, records):
    with (OUT / filename).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def load():
    with RAW.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        expected = set(RATIO_UNITS) | set(SCORES) | set(DIMENSIONS)
        if set(reader.fieldnames or []) != expected:
            raise ValueError("Source schema changed; review Phase 4 variable definitions.")
        rows = list(reader)
    if len(rows) < 4:
        raise ValueError("At least four records required for the distribution statistics.")
    numeric = list(RATIO_UNITS) + SCORES + ["Year", "Month"]
    for i, row in enumerate(rows, 2):
        if any(v is None or not v.strip() for v in row.values()):
            raise ValueError(f"Missing value on CSV line {i}; resolve in Phase 3 first.")
        for col in numeric:
            row[col] = float(row[col])
            if not math.isfinite(row[col]):
                raise ValueError(f"Nonfinite {col} on line {i}.")
        if any(row[c] <= 0 for c in RATIO_UNITS):
            raise ValueError(f"Nonpositive ratio measure on line {i}; review assumptions.")
        if not (1 <= row["Month"] <= 12 and row["Month"].is_integer()
                and row["Year"].is_integer()):
            raise ValueError(f"Invalid time code on line {i}.")
        if not all(0 <= row[c] <= 100 for c in
                   ["Hotel_Occupancy_Rate", "Contribution_to_GDP_Percent"]):
            raise ValueError(f"Invalid percentage on line {i}.")
        expected_rev = row["Number_of_Tourists"] * row["Tourist_Spending_USD"] / 1000
        if abs(row["Tourism_Revenue_USD"] - expected_rev) > 0.011:
            raise ValueError("Revenue-unit identity changed; review the thousand-USD convention.")
    if len({tuple(r.values()) for r in rows}) != len(rows):
        raise ValueError("Exact duplicate rows found; resolve in Phase 3 first.")
    return rows


def level_label(dimension, value):
    if dimension == "Month":
        return calendar.month_name[int(value)]
    if dimension == "Year":
        return str(int(value))
    return str(value)


def level_order(dimension, values):
    if dimension == "Hotel_Rating":
        return [x for x in ["1-star", "2-star", "3-star", "4-star", "5-star", "Unrated"]
                if x in values]
    return sorted(values)


def group_summary(dimension, level, rows):
    tourists = [r["Number_of_Tourists"] for r in rows]
    arrivals = sum(tourists)
    revenue = sum(r["Tourism_Revenue_USD"] for r in rows)
    return dict(
        Dimension=dimension, Level=level_label(dimension, level), Records=len(rows),
        Observed_Arrivals_Sum=arrivals,
        Mean_Arrivals_Per_Record=st.mean(tourists), Median_Arrivals_Per_Record=st.median(tourists),
        Mean_Spending_USD_Per_Tourist=st.mean(r["Tourist_Spending_USD"] for r in rows),
        Tourist_Weighted_Spending_USD=sum(r["Number_of_Tourists"] * r["Tourist_Spending_USD"]
                                        for r in rows) / arrivals,
        Observed_Revenue_Sum_USD_000=revenue,
        Mean_Revenue_USD_000_Per_Record=revenue / len(rows),
        Mean_Occupancy_Percent=st.mean(r["Hotel_Occupancy_Rate"] for r in rows),
        Median_Occupancy_Percent=st.median(r["Hotel_Occupancy_Rate"] for r in rows),
        Mean_Hotels_Per_Record=st.mean(r["Number_of_Hotels"] for r in rows),
        Mean_Room_Price_USD=st.mean(r["Average_Room_Price_USD"] for r in rows),
    )


def pearson(a, b):
    ma, mb = st.mean(a), st.mean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(
        sum((x - ma)**2 for x in a) * sum((y - mb)**2 for y in b))


def md_table(records, columns):
    def fmt(v):
        if isinstance(v, int):
            return f"{v:,}"
        return f"{v:,.2f}" if isinstance(v, float) else str(v)
    return "\n".join([
        "| " + " | ".join(label for _, label in columns) + " |",
        "|" + "---|" * len(columns),
        *["| " + " | ".join(fmt(r[key]) for key, _ in columns) + " |" for r in records],
    ])


def report(rows, profiles, frequencies, groups, bands, correlations):
    p = {r["Variable"]: r for r in profiles}
    n = len(rows)
    def top(dimension, metric, reverse=True):
        return sorted((r for r in groups if r["Dimension"] == dimension),
                      key=lambda r: r[metric], reverse=reverse)
    country = top("Country", "Mean_Arrivals_Per_Record")[0]
    total_country = top("Country", "Observed_Arrivals_Sum")[0]
    city = top("City", "Mean_Arrivals_Per_Record")[0]
    months = top("Month", "Mean_Arrivals_Per_Record")
    spending = top("Purpose_of_Visit", "Tourist_Weighted_Spending_USD")
    value_country = top("Country", "Mean_Revenue_USD_000_Per_Record")[0]
    occupancy = top("Country", "Mean_Occupancy_Percent")
    a, s, o, rev = [p[x] for x in ["Number_of_Tourists", "Tourist_Spending_USD",
                                   "Hotel_Occupancy_Rate", "Tourism_Revenue_USD"]]
    primary = [a, s, p["Average_Length_of_Stay"], o, p["Number_of_Hotels"],
               p["Average_Room_Price_USD"], rev]
    text = f"""# Phase 4: Descriptive Analytics

## 1. Purpose, source and analytical scope

This phase summarises tourism demand, visitor value and hospitality utilisation to support the business questions in [Phase 1](phase1.md). It builds on [Phase 2](phase2.md) and the [shared project context](https://docs.google.com/document/d/1D7XlrIAmvjOiAvelTXcPIIVQPm9oTd76nJ1OJ8jI_tE/edit).

The repository has no Phase 3 cleaned dataset at the time of this contribution. The input is therefore the unchanged `data/raw/Tourism_Hospitality_Industry_Analysis.csv`: **{n} records, 23 variables, 20 countries, 56 cities, 2020–2024**. The script checks completeness, exact duplicates, finite numeric values, time codes, percentages and the revenue identity before calculating statistics. It does not substitute for Phase 3; rerun against an agreed prepared input if that phase later changes the data.

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

{md_table(primary, [('Variable','Variable'), ('Mean','Mean'), ('Median','Median'), ('Range','Range'), ('Sample_Variance','Sample variance'), ('Sample_SD','Sample SD'), ('CV_Percent','CV %')])}

Units follow section 2 and `ratio_summary.csv`; revenue figures above are in thousand USD.

- **Demand:** Mean arrivals are **{a['Mean']:,.0f}**, close to median **{a['Median']:,.0f}**, with SD **{a['Sample_SD']:,.0f}** and CV **{a['CV_Percent']:.1f}%**. A typical record is near 125,000 arrivals, but variation between records is material. A single average is insufficient for local staffing; use the spread alongside destination-specific coverage.
- **Visitor value:** Average record spending is **${s['Mean']:,.2f} per tourist** (median **${s['Median']:,.2f}**), with CV **{s['CV_Percent']:.1f}%**. Spending varies more proportionately than arrivals, so visitor volume alone is an incomplete marketing KPI. The tourist-weighted pooled spending is **${sum(r['Number_of_Tourists'] * r['Tourist_Spending_USD'] for r in rows) / sum(r['Number_of_Tourists'] for r in rows):,.2f}**; it answers a different question from the equal-record mean.
- **Hospitality:** Mean occupancy is **{o['Mean']:.2f}%**, median **{o['Median']:.2f}%**, and SD **{o['Sample_SD']:.2f} percentage points**. The equal-record mean unoccupied share is {100-o['Mean']:.2f}%, but this is neither a pooled vacancy rate nor evidence that building more hotels is warranted.
- **Revenue:** Mean record revenue is **{rev['Mean']:,.2f} thousand USD**, above median **{rev['Median']:,.2f} thousand USD**. CV is **{rev['CV_Percent']:.1f}%**, higher than arrivals and spending because revenue combines both. Use the median to describe a typical record and the mean for an arithmetic average; neither establishes future revenue.

## 4. Quartiles, percentiles and shape

{md_table(primary, [('Variable','Variable'), ('P10','P10'), ('Q1','Q1'), ('Median','P50'), ('Q3','Q3'), ('P90','P90'), ('P95','P95'), ('Adjusted_Skewness','Skewness'), ('Unbiased_Excess_Kurtosis','Excess kurtosis')])}

The middle 50% of arrivals lie between **{a['Q1']:,.0f} and {a['Q3']:,.0f}**; P90 is **{a['P90']:,.0f}**. This is a descriptive reference for comparing observed records, not a 90% service-level demand forecast. Occupancy's middle 50% spans **{o['Q1']:.2f}%–{o['Q3']:.2f}%**, illustrating why managers should review utilisation locally.

Arrivals have skewness **{a['Adjusted_Skewness']:.3f}** and excess kurtosis **{a['Unbiased_Excess_Kurtosis']:.3f}**, consistent with the roughly symmetric, flat distribution identified in Phase 2. Revenue has skewness **{rev['Adjusted_Skewness']:.3f}**: larger values pull the mean above the median. This pattern is consistent with its arithmetic construction from positive arrivals and spending; it is not independent evidence of a high-growth tourism market.

### Frequency distributions and modes

{md_table([r for r in frequencies if r['Variable'] == 'Purpose_of_Visit'], [('Level','Purpose'), ('Count','Records'), ('Percent','% of records'), ('Is_Mode','Mode?')])}

Purpose percentages describe the **share of records**, not the share of individual tourists. Every tied mode is marked. Hotel-tier frequencies, country/city coverage, chronological year/month counts and exact score frequencies are exported in `category_frequencies.csv`. Unrated records remain separate from the star order.

Occupancy bands below are illustrative reporting bands, not industry thresholds:

{md_table([r for r in bands if r['Variable'] == 'Hotel_Occupancy_Rate'], [('Interval','Occupancy interval (%)'), ('Count','Records'), ('Percent','% of records')])}

Numeric frequency tables also use fixed arrivals bands of 50,000, spend bands of USD 1,000 and revenue bands of 200,000 thousand USD. Intervals are left-closed and right-open, with the final interval including its upper endpoint. No observations are dropped.

For the ordinal experience indicator, median satisfaction is **{st.median(r['Tourist_Satisfaction_Score'] for r in rows):.2f}**, Q1–Q3 **{percentile([r['Tourist_Satisfaction_Score'] for r in rows],25):.2f}–{percentile([r['Tourist_Satisfaction_Score'] for r in rows],75):.2f}**. This provides an experience benchmark without interpreting a score of 8 as twice the satisfaction of 4. Infrastructure and waste-management score summaries are in `ordinal_summary.csv`.

## 5. Interpretation by business question

### Q1. Which destinations and time periods attract the most tourists?

Top five countries by **mean arrivals per observed record**:

{md_table(top('Country','Mean_Arrivals_Per_Record')[:5], [('Level','Country'), ('Records','Records'), ('Observed_Arrivals_Sum','Observed arrivals sum'), ('Mean_Arrivals_Per_Record','Mean arrivals'), ('Median_Arrivals_Per_Record','Median arrivals')])}

**{country['Level']}** ranks highest on mean arrivals ({country['Mean_Arrivals_Per_Record']:,.0f}; n={country['Records']}), whereas **{total_country['Level']}** ranks highest on the observed arrivals sum ({total_country['Observed_Arrivals_Sum']:,.0f}; n={total_country['Records']}). These metrics answer different questions and are sensitive to sample coverage. The highest city mean is **{city['Level']}** ({city['Mean_Arrivals_Per_Record']:,.0f}; n={city['Records']}); city comparisons have especially sparse coverage and should be treated cautiously.

{md_table([r for r in groups if r['Dimension']=='Month'], [('Level','Month'), ('Records','Records'), ('Mean_Arrivals_Per_Record','Mean arrivals'), ('Median_Arrivals_Per_Record','Median arrivals')])}

**{months[0]['Level']}** has the highest monthly mean ({months[0]['Mean_Arrivals_Per_Record']:,.0f}; n={months[0]['Records']}), and **{months[-1]['Level']}** the lowest ({months[-1]['Mean_Arrivals_Per_Record']:,.0f}; n={months[-1]['Records']}). These pool different countries and years: they do not establish a seasonal peak. A tourism authority should validate patterns in a balanced destination-month series before scheduling promotions. Year summaries are exported with sample sizes; changes are not national growth rates.

### Q2. Which segments and destinations generate the highest economic value?

{md_table(spending, [('Level','Purpose'), ('Records','Records'), ('Mean_Spending_USD_Per_Tourist','Equal-record spend (USD)'), ('Tourist_Weighted_Spending_USD','Tourist-weighted spend (USD)'), ('Mean_Revenue_USD_000_Per_Record','Mean revenue (USD 000)')])}

**{spending[0]['Level']}** has the highest tourist-weighted spending (**${spending[0]['Tourist_Weighted_Spending_USD']:,.2f}**), versus **${spending[-1]['Tourist_Weighted_Spending_USD']:,.2f}** for **{spending[-1]['Level']}**. **{value_country['Level']}** has the highest mean revenue per observed country record (**{value_country['Mean_Revenue_USD_000_Per_Record']:,.2f} thousand USD**; n={value_country['Records']}). These are candidates for examining value-based marketing, subject to better data. Revenue is mechanically determined by arrivals and spending, and acquisition costs and margins are missing, so this analysis cannot establish segment profitability or marketing ROI.

### Q3. Is existing hospitality capacity being used efficiently?

{md_table([occupancy[0], occupancy[-1]], [('Level','Country'), ('Records','Records'), ('Mean_Occupancy_Percent','Mean occupancy %'), ('Mean_Hotels_Per_Record','Mean hotels per record'), ('Mean_Arrivals_Per_Record','Mean arrivals')])}

**{occupancy[0]['Level']}** has the highest equal-record mean occupancy (**{occupancy[0]['Mean_Occupancy_Percent']:.2f}%**), while **{occupancy[-1]['Level']}** has the lowest (**{occupancy[-1]['Mean_Occupancy_Percent']:.2f}%**). The spread highlights the value of destination-level utilisation reviews, but does not measure technical efficiency, room shortages or the return on expansion.

{md_table(correlations, [('Variable_X','Measure X'), ('Variable_Y','Measure Y'), ('Pearson_r','Pearson r')])}

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

"""
    (ROOT / "phase4.md").write_text(text.rstrip() + "\n", encoding="utf-8")


def main():
    rows = load()
    OUT.mkdir(parents=True, exist_ok=True)
    profiles = [describe(c, [r[c] for r in rows], unit) for c, unit in RATIO_UNITS.items()]
    write_csv("ratio_summary.csv", profiles)
    ordinal = []
    for c in SCORES:
        a = [r[c] for r in rows]
        ordinal.append(dict(Variable=c, Count=len(a), Min=min(a), P10=percentile(a, 10),
                            Q1=percentile(a, 25), Median=st.median(a), Q3=percentile(a, 75),
                            P90=percentile(a, 90), P95=percentile(a, 95), Max=max(a)))
    write_csv("ordinal_summary.csv", ordinal)
    frequencies, groups = [], []
    for c in DIMENSIONS + SCORES:
        buckets = defaultdict(list)
        for r in rows:
            buckets[r[c]].append(r)
        peak = max(map(len, buckets.values()))
        for level in level_order(c, buckets):
            subset = buckets[level]
            frequencies.append(dict(Variable=c, Level=level_label(c, level), Count=len(subset),
                                    Percent=100 * len(subset) / len(rows),
                                    Is_Mode="Yes" if len(subset) == peak else "No"))
            if c in DIMENSIONS:
                groups.append(group_summary(c, level, subset))
    write_csv("category_frequencies.csv", frequencies)
    write_csv("grouped_business_summary.csv", groups)
    bins = {
        "Number_of_Tourists": ("persons", [0, 50000, 100000, 150000, 200000]),
        "Tourist_Spending_USD": ("USD per tourist", [0, 1000, 2000, 3000, 4000, 5000]),
        "Hotel_Occupancy_Rate": ("percent", [0, 40, 50, 60, 70, 80, 90, 100]),
        "Tourism_Revenue_USD": ("thousand USD (inferred)", [0, 200000, 400000, 600000, 800000, 1000000]),
    }
    bands = []
    for c, (unit, edges) in bins.items():
        counts = []
        for i, (lo, hi) in enumerate(zip(edges, edges[1:])):
            final = i == len(edges) - 2
            count = sum(lo <= r[c] <= hi if final else lo <= r[c] < hi for r in rows)
            counts.append(count)
            bands.append(dict(Variable=c, Unit=unit, Lower_Inclusive=lo, Upper=hi,
                              Upper_Inclusive="Yes" if final else "No",
                              Interval=f"[{lo:,}, {hi:,}{']' if final else ')'}",
                              Count=count, Percent=100 * count / len(rows)))
        if sum(counts) != len(rows):
            raise ValueError(f"Frequency bins no longer cover {c}; review edges.")
    write_csv("numeric_frequencies.csv", bands)
    correlations = [dict(Variable_X=x, Variable_Y=y, Count=len(rows),
                         Pearson_r=pearson([r[x] for r in rows], [r[y] for r in rows]))
                    for x, y in [("Number_of_Tourists", "Hotel_Occupancy_Rate"),
                                 ("Number_of_Tourists", "Number_of_Hotels"),
                                 ("Number_of_Hotels", "Hotel_Occupancy_Rate")]]
    write_csv("capacity_correlations.csv", correlations)
    keys = Counter((r["City"], r["Year"], r["Month"]) for r in rows)
    checks = [
        "PHASE 4 SOURCE CHECKS",
        f"Source: {RAW.relative_to(ROOT).as_posix()}",
        f"SHA256: {hashlib.sha256(RAW.read_bytes()).hexdigest()}",
        f"Rows: {len(rows)}; columns: {len(rows[0])}",
        "Missing cells: 0; exact duplicate rows: 0; all numeric values finite",
        "Time codes and percentage bounds: PASS",
        f"Distinct city-year-month keys: {len(keys)}",
        f"Repeated city-year-month keys: {sum(v > 1 for v in keys.values())} (retained)",
        f"Rows in repeated keys: {sum(v for v in keys.values() if v > 1)}",
        "Revenue = arrivals * spending / 1000 within 0.011 stored units: PASS",
        "Raw dataset modified: No; no Phase 3 prepared input available",
        "Frequency bin coverage and category totals: checked by construction",
    ]
    (OUT / "source_checks.txt").write_text("\n".join(checks) + "\n", encoding="utf-8")
    report(rows, profiles, frequencies, groups, bands, correlations)
    print(f"Phase 4 complete: {len(rows)} records; 7 output files and phase4.md regenerated.")


if __name__ == "__main__":
    main()
