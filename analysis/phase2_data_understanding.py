"""
Phase 2 - Data Understanding
Tourism & Hospitality Industry Analysis Dataset (Kaggle, smithmurphy)

Produces, in outputs/phase2/:
  metadata_table.csv        - variable dictionary with measurement scale
  numeric_profile.csv       - count/missing/min/max/mean/median/std/skew/kurtosis per numeric variable
  categorical_profile.csv   - level counts for every categorical variable
  data_quality_checks.txt   - missing values, duplicates, key uniqueness, derived-column checks
  correlation_matrix.csv    - Pearson correlations between numeric variables
  fig_distributions.png     - histogram of every numeric variable
  fig_correlation_heatmap.png
  fig_categorical_counts.png

Uses only csv + numpy + scipy + matplotlib (pandas could not be loaded on the
author's machine because Windows Smart App Control blocks its compiled DLLs).

Run from the project root:
    python analysis/phase2_data_understanding.py
"""
import csv
import collections
import os
import sys

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "Tourism_Hospitality_Industry_Analysis.csv")
OUT = os.path.join(ROOT, "outputs", "phase2")
os.makedirs(OUT, exist_ok=True)

# --------------------------------------------------------------------------
# Metadata: description, unit, measurement scale, data type, analytical role
# --------------------------------------------------------------------------
META = [
    # name, description, unit, scale, type, role, business question(s)
    ("Country", "Destination country of the record", "-", "Nominal", "Categorical", "Dimension (geography)", "Q1, Q2, Q3, Q4"),
    ("City", "Destination city within the country", "-", "Nominal", "Categorical", "Dimension (geography)", "Q1, Q2, Q3"),
    ("Year", "Calendar year of the observation", "Year", "Interval", "Discrete numeric", "Dimension (time)", "Q1, Q4"),
    ("Month", "Calendar month of the observation (1 = Jan ... 12 = Dec)", "Month", "Ordinal", "Discrete numeric (coded)", "Dimension (time / seasonality)", "Q1, Q4"),
    ("Number_of_Tourists", "Tourist arrivals recorded for the city in that month", "Persons", "Ratio", "Discrete numeric", "Target (predictive model)", "Q1, Q3, Q4"),
    ("Purpose_of_Visit", "Main purpose of travel of the tourist segment", "-", "Nominal", "Categorical", "Dimension (segment)", "Q2, Q4"),
    ("Average_Length_of_Stay", "Average nights stayed per tourist", "Nights", "Ratio", "Continuous numeric", "Predictor / KPI", "Q2, Q3"),
    ("Tourist_Spending_USD", "Average spending per tourist", "USD per tourist", "Ratio", "Continuous numeric", "Predictor / KPI", "Q2"),
    ("Hotel_Occupancy_Rate", "Share of available hotel rooms occupied", "Percent (0-100)", "Ratio", "Continuous numeric", "KPI (capacity utilisation)", "Q3"),
    ("Number_of_Hotels", "Number of hotels operating in the city", "Count", "Ratio", "Discrete numeric", "Predictor (capacity)", "Q3, Q4"),
    ("Hotel_Rating", "Star classification of hotels in the record (1-star ... 5-star, or Unrated)", "Stars", "Ordinal", "Categorical (ordered)", "Dimension (quality tier)", "Q2, Q3"),
    ("Average_Room_Price_USD", "Average nightly room rate", "USD per night", "Ratio", "Continuous numeric", "Predictor / KPI (pricing)", "Q2, Q3"),
    ("Tourism_Revenue_USD", "Tourism revenue; equals Number_of_Tourists x Tourist_Spending_USD / 1000, i.e. effectively in thousand USD", "USD '000 (see quality notes)", "Ratio", "Continuous numeric", "KPI (derived - not a predictor of arrivals)", "Q2"),
    ("Employment_in_Tourism", "Number of people employed in tourism", "Persons", "Ratio", "Discrete numeric", "Predictor / economic impact", "Q2, Q4"),
    ("Contribution_to_GDP_Percent", "Tourism's share of GDP", "Percent", "Ratio", "Continuous numeric", "Economic impact KPI", "Q2"),
    ("Number_of_Flights", "Number of incoming flights", "Count", "Ratio", "Discrete numeric", "Predictor (accessibility)", "Q4"),
    ("Airport_Passenger_Traffic", "Passengers handled by the destination airport(s)", "Persons", "Ratio", "Discrete numeric", "Predictor (accessibility)", "Q4"),
    ("Transport_Infrastructure_Quality", "Quality index of transport infrastructure", "Score 1-10", "Ordinal", "Continuous numeric (index)", "Predictor (accessibility)", "Q4"),
    ("Eco_Tourism_Revenue_USD", "Revenue from eco-tourism; 5%-30% of Tourism_Revenue_USD", "USD '000 (see quality notes)", "Ratio", "Continuous numeric", "KPI (derived - sustainability)", "Q2"),
    ("Carbon_Footprint_kg", "Carbon emissions attributed to tourism; 100-500 kg per tourist", "kg CO2", "Ratio", "Continuous numeric", "Sustainability KPI (derived)", "Supporting"),
    ("Waste_Management_Rating", "Rating of destination waste management", "Score 1-10", "Ordinal", "Continuous numeric (index)", "Sustainability indicator", "Supporting"),
    ("Tourist_Satisfaction_Score", "Average tourist satisfaction", "Score 5-10", "Ordinal", "Continuous numeric (index)", "Predictor / experience KPI", "Q4"),
    ("Number_of_Online_Reviews", "Online reviews posted about the destination", "Count", "Ratio", "Discrete numeric", "Predictor (popularity / awareness)", "Q4"),
]
META_COLS = ["Variable", "Description", "Unit", "Measurement_Scale", "Data_Type",
             "Analytical_Role", "Business_Question"]

HOTEL_RATING_ORDER = ["Unrated", "1-star", "2-star", "3-star", "4-star", "5-star"]


def load(path):
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows, list(rows[0].keys())


def is_numeric(values):
    try:
        [float(v) for v in values if v.strip() != ""]
        return True
    except ValueError:
        return False


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    rows, cols = load(RAW)
    n = len(rows)
    meta_by_name = {m[0]: m for m in META}
    assert set(meta_by_name) == set(cols), "metadata table out of sync with dataset columns"

    num_cols = [c for c in cols if is_numeric([r[c] for r in rows])]
    cat_cols = [c for c in cols if c not in num_cols]
    X = np.array([[float(r[c]) for c in num_cols] for r in rows])

    # ---------------- metadata table (+ observed range / levels) ----------
    meta_rows = []
    for c in cols:
        m = list(meta_by_name[c])
        vals = [r[c] for r in rows]
        if c in num_cols:
            a = X[:, num_cols.index(c)]
            observed = f"{a.min():g} to {a.max():g}"
        else:
            levels = sorted(set(vals))
            if c == "Hotel_Rating":
                levels = HOTEL_RATING_ORDER
            observed = f"{len(levels)} levels: " + ", ".join(levels) if len(levels) <= 10 else f"{len(levels)} levels"
        missing = sum(1 for v in vals if v.strip() == "")
        meta_rows.append(m + [observed, len(set(vals)), missing])
    write_csv(os.path.join(OUT, "metadata_table.csv"),
              META_COLS + ["Observed_Range_or_Levels", "Distinct_Values", "Missing"], meta_rows)

    # ---------------- numeric profile ------------------------------------
    prof = []
    for j, c in enumerate(num_cols):
        a = X[:, j]
        q1, q3 = np.percentile(a, [25, 75])
        prof.append([c, len(a), 0, round(a.min(), 2), round(q1, 2), round(np.median(a), 2),
                     round(a.mean(), 2), round(q3, 2), round(a.max(), 2), round(a.std(ddof=1), 2),
                     round(a.std(ddof=1) / a.mean() * 100, 1),
                     round(float(stats.skew(a)), 2), round(float(stats.kurtosis(a)), 2)])
    write_csv(os.path.join(OUT, "numeric_profile.csv"),
              ["Variable", "Count", "Missing", "Min", "Q1", "Median", "Mean", "Q3", "Max",
               "Std_Dev", "CV_%", "Skewness", "Excess_Kurtosis"], prof)

    # ---------------- categorical profile --------------------------------
    cat_prof = []
    for c in cat_cols:
        cnt = collections.Counter(r[c] for r in rows)
        order = HOTEL_RATING_ORDER if c == "Hotel_Rating" else [k for k, _ in cnt.most_common()]
        for lvl in order:
            cat_prof.append([c, lvl, cnt[lvl], round(cnt[lvl] / n * 100, 1)])
    write_csv(os.path.join(OUT, "categorical_profile.csv"),
              ["Variable", "Level", "Count", "Percent"], cat_prof)

    # ---------------- correlation matrix ---------------------------------
    corr = np.corrcoef(X.T)
    write_csv(os.path.join(OUT, "correlation_matrix.csv"), [""] + num_cols,
              [[c] + [round(v, 3) for v in corr[i]] for i, c in enumerate(num_cols)])

    # ---------------- data quality checks --------------------------------
    col = lambda name: X[:, num_cols.index(name)]
    tourists, spend = col("Number_of_Tourists"), col("Tourist_Spending_USD")
    rev, eco, co2 = col("Tourism_Revenue_USD"), col("Eco_Tourism_Revenue_USD"), col("Carbon_Footprint_kg")
    pax = col("Airport_Passenger_Traffic")
    key_counts = collections.Counter((r["City"], r["Year"], r["Month"]) for r in rows)
    dup_keys = {k: v for k, v in key_counts.items() if v > 1}
    city_country = collections.defaultdict(set)
    for r in rows:
        city_country[r["City"]].add(r["Country"])
    city_ratings = collections.defaultdict(set)
    for r in rows:
        city_ratings[r["City"]].add(r["Hotel_Rating"])
    yrs = collections.Counter(r["Year"] for r in rows)
    mos = collections.Counter(int(r["Month"]) for r in rows)
    i_t = num_cols.index("Number_of_Tourists")
    anova = {}
    for cat in ["Country", "City", "Purpose_of_Visit", "Hotel_Rating", "Year", "Month"]:
        g = collections.defaultdict(list)
        for r in rows:
            g[r[cat]].append(float(r["Number_of_Tourists"]))
        anova[cat] = stats.f_oneway(*[v for v in g.values() if len(v) > 1]).pvalue

    lines = [
        "PHASE 2 - DATA QUALITY CHECKS",
        "=" * 60,
        f"Source file : data/raw/Tourism_Hospitality_Industry_Analysis.csv",
        f"Rows        : {n}",
        f"Columns     : {len(cols)}  ({len(num_cols)} numeric, {len(cat_cols)} categorical text)",
        "",
        "1. Completeness",
        f"   Missing cells (blank)             : {sum(1 for r in rows for c in cols if r[c].strip() == '')}",
        f"   Exact duplicate rows              : {n - len({tuple(r.values()) for r in rows})}",
        "",
        "2. Structure / granularity",
        f"   Countries: {len(set(r['Country'] for r in rows))}, cities: {len(city_country)}",
        f"   Cities mapped to >1 country       : {sum(len(v) > 1 for v in city_country.values())}",
        f"   Years : {dict(sorted(yrs.items()))}",
        f"   Months: {dict(sorted(mos.items()))}",
        f"   Duplicate (City, Year, Month) keys: {len(dup_keys)} keys covering {sum(dup_keys.values())} rows",
        f"   -> a row is a single city-month record, not a unique panel cell; the data is an",
        f"      unbalanced sample (56 cities x 60 months = 3,360 possible cells, only {n} rows).",
        f"   Cities with >1 Hotel_Rating value : {sum(len(v) > 1 for v in city_ratings.values())} of {len(city_ratings)}",
        f"   -> Hotel_Rating describes the record (segment), not a fixed attribute of the city.",
        "",
        "3. Derived / dependent columns",
        f"   max |Revenue - Tourists*Spending/1000| = {np.abs(rev - tourists * spend / 1000).max():.4f}",
        f"   -> Tourism_Revenue_USD = Number_of_Tourists x Tourist_Spending_USD / 1000 (exact, to the cent).",
        f"      The column is therefore effectively in THOUSAND USD, not USD.",
        f"   Eco_Tourism_Revenue / Tourism_Revenue ranges {np.min(eco / rev):.3f} - {np.max(eco / rev):.3f}",
        f"   Carbon_Footprint_kg / Number_of_Tourists ranges {np.min(co2 / tourists):.1f} - {np.max(co2 / tourists):.1f} kg",
        f"   -> Revenue, Eco-tourism revenue and Carbon footprint are computed FROM tourist arrivals and",
        f"      must not be used as predictors of Number_of_Tourists (target leakage).",
        "",
        "4. Logical consistency",
        f"   Rows where Airport_Passenger_Traffic < Number_of_Tourists : {(pax < tourists).sum()}",
        f"   Correlation Number_of_Flights vs Airport_Passenger_Traffic: {corr[num_cols.index('Number_of_Flights'), num_cols.index('Airport_Passenger_Traffic')]:+.3f}",
        f"   -> flights and passengers are unrelated, which would not hold in real airport data.",
        "",
        "5. Distribution shape",
        "   Most numeric variables have skewness ~0 and excess kurtosis ~ -1.2, the signature of a",
        "   uniform distribution (values spread evenly between a min and a max). Only the derived",
        "   columns (revenue, eco revenue, carbon) are right-skewed.",
        "",
        "6. Association with the planned target (Number_of_Tourists)",
    ]
    for j, c in enumerate(num_cols):
        if c != "Number_of_Tourists":
            lines.append(f"   r({c:34s}) = {corr[i_t, j]:+.3f}")
    lines.append("   One-way ANOVA p-values (tourist arrivals differ across groups?):")
    for cat, p in anova.items():
        lines.append(f"   {cat:20s} p = {p:.3f}")
    lines += [
        "   -> Apart from the derived columns, no variable has a meaningful linear association with",
        "      tourist arrivals, and arrivals do not differ significantly by country, city, purpose,",
        "      rating, year or month. See phase2.md section 6 for implications for Phases 4-6.",
    ]
    with open(os.path.join(OUT, "data_quality_checks.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    # ---------------- figures --------------------------------------------
    ncols = 4
    nrows = int(np.ceil(len(num_cols) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 3.0 * nrows))
    for ax, j in zip(axes.flat, range(len(num_cols))):
        ax.hist(X[:, j], bins=20, color="#2a6f97", edgecolor="white")
        ax.set_title(num_cols[j].replace("_", " "), fontsize=9)
        ax.tick_params(labelsize=7)
        ax.set_ylabel("Records", fontsize=7)
    for ax in list(axes.flat)[len(num_cols):]:
        ax.axis("off")
    fig.suptitle("Phase 2 - Distribution of numeric variables (n = 500)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(os.path.join(OUT, "fig_distributions.png"), dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(13, 11))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    labels = [c.replace("_", " ") for c in num_cols]
    ax.set_xticks(range(len(num_cols)), labels, rotation=90, fontsize=8)
    ax.set_yticks(range(len(num_cols)), labels, fontsize=8)
    for i in range(len(num_cols)):
        for j in range(len(num_cols)):
            if i != j and abs(corr[i, j]) >= 0.2:
                ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")
    ax.set_title("Phase 2 - Correlation between numeric variables (|r| >= 0.20 labelled)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_correlation_heatmap.png"), dpi=130)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    for ax, c in zip(axes.flat, ["Country", "Purpose_of_Visit", "Hotel_Rating", "Year"]):
        cnt = collections.Counter(r[c] for r in rows)
        if c == "Hotel_Rating":
            keys = HOTEL_RATING_ORDER
        elif c == "Year":
            keys = sorted(cnt)
        else:
            keys = [k for k, _ in cnt.most_common()]
        ax.barh(keys[::-1], [cnt[k] for k in keys][::-1], color="#2a6f97")
        ax.set_title(f"Records by {c.replace('_', ' ')}")
        ax.set_xlabel("Number of records")
        ax.tick_params(labelsize=8)
    fig.suptitle("Phase 2 - Coverage of categorical / time variables", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(OUT, "fig_categorical_counts.png"), dpi=130)
    plt.close(fig)

    print("\n".join(lines))
    print(f"\nOutputs written to {OUT}")


if __name__ == "__main__":
    sys.exit(main())
