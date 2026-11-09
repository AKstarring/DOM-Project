# Business Analytics Project

## Business Analytics Workflow

Your project must follow the complete **Business Analytics** workflow, in seven phases:

| Phase | Focus | Key output |
|---|---|---|
| 1 | Business Understanding & Problem Definition | Problem statement and business objectives |
| 2 | Data Understanding | Dataset description and variable classification |
| 3 | Data Preprocessing & Preparation | Before-and-after comparison of the dataset |
| 4 | Descriptive Analytics | Summary statistics interpreted in business terms |
| 5 | Data Visualization & Dashboard | 6–8 visualizations and one interactive dashboard |
| 6 | Predictive Analytics | At least one evaluated model with business interpretation |
| 7 | Prescriptive Insights & Recommendations | Findings and recommendations |

## 1. Project Overview

You will work in **groups of 5 (2 groups will have 6 students)** to solve a real-world business problem using the complete analytics process covered in this course.

Each group will select a **business domain and problem**, obtain a relevant dataset, prepare and analyze the data, build meaningful visualizations and an interactive dashboard, and generate **descriptive, predictive, and prescriptive insights**.

The emphasis of this project is on using **analytics to support managerial decision-making**, not merely applying software or algorithms. Every number, chart, and model you present should help answer a business question.

## 2. Project Theme

**“From Raw Data to Business Decisions”**

### Choose a Domain

Each group must select a business problem from one of the following domains:

|  |  |
|---|---|
| Retail and E-commerce | Marketing and Customer Analytics |
| Finance and Banking | Supply Chain and Logistics |
| Human Resource Analytics | Healthcare Analytics |
| Manufacturing | Education Analytics |
| Sustainability and Energy | Hospitality and Tourism |

> **Important:** Your selected business problem and dataset must support all required phases of the project, including predictive analytics. Therefore, choose a problem for which a meaningful predictive model can be developed and evaluated.

## Phase 1: Business Understanding and Problem Definition

You must:

- Introduce the business context.
- Clearly define the business problem.
- Identify the stakeholders.
- Formulate **3–4 specific business questions**.
- Explain how analytics can help address the problem.

### Expected output

A clear problem statement and business objectives.

## Phase 2: Data Understanding

You must:

- Describe the data source.
- Explain the dataset and its variables and prepare a metadata table.
- Identify the measurement scale of each variable:
  - Nominal
  - Ordinal
  - Interval
  - Ratio

### Minimum dataset requirement

The dataset must contain:

- **At least 500 observations**
- **At least 8 relevant variables**

### Acceptable data sources

- Public datasets
- Kaggle datasets
- Government / open datasets
- Company datasets, where available

## Phase 3: Data Preprocessing and Preparation

Demonstrate the data preprocessing techniques covered in the course. Include the following wherever applicable:

### A. Data Cleaning

- Missing value identification and treatment
- Duplicate identification and removal
- Inconsistent data correction
- Data type corrections

### B. Outlier Detection

Identify and discuss potential outliers using appropriate techniques such as:

- Box plots
- Interquartile range (IQR)
- Z-score

> **Important:** You must justify how identified potential outliers are handled, whether they are removed, retained, or treated.

### C. Data Transformation

Where appropriate:

- Scaling or normalization
- Encoding categorical variables
- Data aggregation
- Creation of new variables/features

### D. Data Integration

- If applicable, combine multiple datasets.

### Expected output

- A **before-and-after comparison** demonstrating how the dataset was prepared for analysis (e.g., number of rows, missing values, duplicates, and data types before and after cleaning).

## Phase 4: Descriptive Analytics

Summarise and explore the data using appropriate measures:

| Category | Measures |
|---|---|
| Central tendency | Mean, Median, Mode |
| Dispersion | Range, Variance, Standard deviation, Coefficient of variation |
| Distribution | Quartiles and percentiles, Frequency distribution, Skewness, Kurtosis |

Use measures appropriate to the variable type and business question; it is not necessary to calculate every measure for every variable.

You must interpret the results in the business context.

## Phase 5: Data Visualization and Dashboard

Your project should include at least:

- **6 meaningful visualizations**
- **One interactive dashboard developed using Tableau**

Select charts based on the business question being answered. All the prepared charts should be properly labeled.

### Dashboard requirements

The dashboard should:

- Answer specific business questions.
- Highlight important KPIs.
- Allow easy interpretation.
- Follow good visualization principles.
- Avoid unnecessary charts or clutter.

## Phase 6: Predictive Analytics

Apply **at least one appropriate predictive model**. The choice of model should depend on your business problem.

The model should be trained and evaluated using an appropriate validation approach (e.g., train-test split), and appropriate evaluation metrics should be reported and interpreted.

### Model choice and interpretation matter more than complexity

You will not earn extra marks for using a more complex algorithm. A well-justified, correctly evaluated simple model with a clear business interpretation will score higher than a complex model that is poorly explained.

Do not simply report the accuracy or R² value. You must explain: **What does the model tell the business?**

## Phase 7: Prescriptive Insights and Recommendations

This is an important component of the project. For this project, prescriptive analytics refers to translating analytical findings into actionable business recommendations. Students may also use what-if analysis and scenario analysis. Convert your analysis into actionable business recommendations. For example:

| Analytical finding | Business recommendation |
|---|---|
| Customers aged 18–25 have a high probability of churn. | Develop targeted retention offers for customers aged 18–25. |

You should provide:

1. **Key Findings** – at least 5 important findings.
2. **Business Recommendations** – at least 3–5 actionable recommendations.
3. **Expected Business Impact** – Where numerical impact estimates are provided, students must state the assumptions or basis used to derive the estimate. Avoid presenting speculative estimates as established results.

## 4. Project Deliverables

| Deliverable | Description |
|---|---|
| Dataset | Both raw and cleaned datasets |
| Analysis Files | Files from the tools actually used for analysis (e.g., Excel, R, Python, and/or Tableau). |
| Dashboard | Tableau dashboard file |
| Presentation | Summary slides of the project |
| Contribution Statement | Individual contribution of each group member |

## Ethical Data Collection Guidelines

As you are working on your Business Analytics Project, you will be gathering and analyzing real-world datasets. While data collection is a powerful skill for any analyst, doing it responsibly and ethically is just as critical as the analysis itself.

To ensure our projects meet professional, legal, and academic standards, everyone must strictly adhere to the following ethical data collection guidelines:

- **Respect Public Boundaries:** Use data that is publicly accessible. Do not attempt to scrape or harvest data that sits behind a login screen, registration form, or paywall.
- **Check the Rules (ToS and Robots.txt):** Always review the target website’s Terms of Service and its `/robots.txt` file. If a platform explicitly forbids automated scraping or data harvesting, you must find an alternative data source.
- **Protect Privacy (No PII/PHI):** Your datasets must not contain any Personally Identifiable Information (PII) such as customer names, emails, phone numbers, or addresses. If your project touches on healthcare or pharmacy metrics, patient-level data is strictly off-limits.
- **Document Your Data Provenance:** In the appendix of your final report, you must include a data sourcing log detailing the source URL, the exact date of collection, and the tool or method used to extract the data.

It is advisable to go for publicly available data.
