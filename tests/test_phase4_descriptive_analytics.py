"""Statistical conventions and aggregation checks; standard-library only.

Run: python -m unittest discover -s tests -v
"""

import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "phase4", Path(__file__).resolve().parents[1] / "analysis/phase4_descriptive_analytics.py")
phase4 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(phase4)


class DescriptiveAnalyticsTests(unittest.TestCase):
    def test_linear_percentiles_and_sample_variance(self):
        result = phase4.describe("example", [1, 2, 3, 4], "units")
        self.assertEqual(result["Q1"], 1.75)
        self.assertEqual(result["Median"], 2.5)
        self.assertEqual(result["Q3"], 3.25)
        self.assertAlmostEqual(result["Sample_Variance"], 5 / 3)
        self.assertAlmostEqual(result["Adjusted_Skewness"], 0)
        self.assertAlmostEqual(result["Unbiased_Excess_Kurtosis"], -1.2)
        self.assertEqual(result["Modes"], "No repeated value")

    def test_all_tied_modes_are_retained(self):
        result = phase4.describe("example", [1, 1, 2, 2, 3], "units")
        self.assertEqual(result["Modes"], "1; 2")
        self.assertEqual(result["Mode_Frequency"], 2)
        self.assertEqual(result["Number_of_Modes"], 2)

    def test_zero_variation_has_no_defined_shape(self):
        result = phase4.describe("example", [5] * 4, "units")
        self.assertEqual(result["CV_Percent"], 0)
        self.assertEqual(result["Adjusted_Skewness"], "")
        self.assertEqual(result["Unbiased_Excess_Kurtosis"], "")

    def test_time_order_and_unrated_separation(self):
        self.assertEqual(phase4.level_order("Month", [12, 2, 1]), [1, 2, 12])
        self.assertEqual(phase4.level_label("Month", 2), "February")
        self.assertEqual(phase4.level_order("Hotel_Rating", ["Unrated", "5-star", "1-star"]),
                         ["1-star", "5-star", "Unrated"])

    def test_weighted_spending_differs_from_record_average(self):
        rows = []
        for tourists, spend in [(10, 100), (90, 200)]:
            rows.append(dict(Number_of_Tourists=tourists, Tourist_Spending_USD=spend,
                             Tourism_Revenue_USD=tourists * spend / 1000,
                             Hotel_Occupancy_Rate=60, Number_of_Hotels=10,
                             Average_Room_Price_USD=100))
        result = phase4.group_summary("Country", "Example", rows)
        self.assertEqual(result["Mean_Spending_USD_Per_Tourist"], 150)
        self.assertEqual(result["Tourist_Weighted_Spending_USD"], 190)
        self.assertEqual(result["Mean_Occupancy_Percent"], 60)
        self.assertEqual(result["Mean_Hotels_Per_Record"], 10)

    def test_current_source_and_group_totals(self):
        rows = phase4.load()
        self.assertEqual(len(rows), 500)
        total = sum(r["Number_of_Tourists"] for r in rows)
        self.assertEqual(total, 62631942)
        self.assertAlmostEqual(total / 500, 125263.884)
        for dimension in phase4.DIMENSIONS:
            buckets = phase4.defaultdict(list)
            for row in rows:
                buckets[row[dimension]].append(row)
            summaries = [phase4.group_summary(dimension, level, subset)
                         for level, subset in buckets.items()]
            self.assertEqual(sum(s["Records"] for s in summaries), 500)
            self.assertEqual(sum(s["Observed_Arrivals_Sum"] for s in summaries), total)


if __name__ == "__main__":
    unittest.main()
