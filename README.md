# Data Science Portfolio: Raymond Cancino

[![Portfolio](https://img.shields.io/badge/portfolio-cancinoray.netlify.app-0a66c2)](https://cancinoray.netlify.app/)
[![Resume](https://img.shields.io/badge/resume-PDF-informational)](https://cancinoray.netlify.app/assets/resume.pdf)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-cancinoraymond-0a66c2)](https://www.linkedin.com/in/cancinoraymond/)
[![WQU Applied Data Science Lab](https://img.shields.io/badge/WQU-Applied%20Data%20Science%20Lab-ff6600)](https://www.credly.com/badges/c7bfe8cd-3e7e-4c8d-a2c5-c533de00db49)

Hi, I'm [Raymond Cancino](https://cancinoray.netlify.app/): a Data Engineer transitioning into **Forward Deployed Engineering** and **Data Science, Machine Learning, and AI**. Philippines-based.

I help e-commerce and ops teams make sense of data that doesn't agree with itself. Across e-commerce, AdTech, and EdTech I've built pipelines that survive inconsistent schemas and mismatched platforms, then shipped the fix (the mix of client-facing problem-solving and hands-on engineering that FDE work calls for).

That same data-engineering background is what this repo builds on: moving from *delivering clean data* to *extracting the signal in it*, with modeling, forecasting, and experimentation, and an eye toward applied ML/AI next. Mechanical Engineering graduate and former university instructor, comfortable structuring ambiguous problems and explaining results plainly.

- Portfolio: https://cancinoray.netlify.app/
- Resume / CV: https://cancinoray.netlify.app/assets/resume.pdf
- Email: cancinoray@gmail.com · LinkedIn: [/in/cancinoraymond](https://www.linkedin.com/in/cancinoraymond/) · GitHub: [@cancinoray](https://github.com/cancinoray)
- Open to Data Science, ML/AI, FDE, and Data Engineering roles

I completed WorldQuant University's **Applied Data Science Lab** in 2026 ([verify on Credly](https://www.credly.com/badges/c7bfe8cd-3e7e-4c8d-a2c5-c533de00db49)), where I worked through the full applied data science workflow (wrangling, regression, classification, time series, and dashboards) on real-world datasets. WQU's academic policy doesn't allow sharing or reusing coursework, so this repo is how I demonstrate those same skills: **every project here is scaffolded from scratch**, with my own questions, code, and datasets, built to mirror the breadth of what I practiced in the program without reusing any of its assignments, text, or code.

This repo is a focused data science companion to that transition: 7 original notebook projects + 1 packaged volatility pipeline, covering EDA → regression → time series → classification → ensembles → clustering → experimentation. Each project is scoped to practice one core skill end-to-end rather than stack everything into one notebook.

> All projects here are **original work**: my own questions, code, and writing on public datasets. No coursework assignments, text, code, or proprietary datasets are reused here.

## Results at a glance

| # | Project | Question | Headline result |
|---|---|---|---|
| 01 | City Listings EDA | Does size or location drive nightly price? | Size and location are complementary; full model CV R² **0.495**. Location adds +0.175 R² over size + room type; size adds +0.115 over location + room type. |
| 02 | House Price Regression | Can regularized regression beat OLS? | Engineered OLS holdout R² **0.913**, RMSE **$22,788**. Ridge/Lasso cut CV log-RMSE from 0.163 to 0.140/0.138 but did not win the holdout. |
| 03 | Air Quality Time Series | Can I forecast NYC PM2.5? | Ridge lag model 90-day RMSE **6.45 µg/m³** vs 7.08 static seasonal naive; one-day-ahead RMSE **5.42**. Skill fades with horizon. |
| 04 | Hospital Readmission | Can administrative data predict 30-day readmission? | 88.8% accuracy but only **2.5% recall** unweighted; balanced logistic recall **54.3%**, ROC-AUC **0.667**. Prior admissions dominate. |
| 05 | Fraud Detection | How do ensembles handle 0.17% positives? | Random Forest PR-AUC **0.782** (ROC 0.935) vs logistic PR-AUC 0.723 (ROC 0.977). Cost-optimal threshold catches **77%** of frauds. |
| 06 | Customer Segmentation | What customer segments exist? | Five RFM segments; **Champions = 7.8% of customers but 52.9% of revenue**. Log-RFM clustering beats a raw-RFM outlier split. |
| 07 | A/B Testing | Does moving the gate from 30 to 40 hurt retention? | 7-day retention **19.02% vs 18.20%** (+0.82 pp, p = 0.0016), 1-day not significant. Keep gate 30. |

## Projects

| # | Title | Skills shown | Link |
|---|-------|--------------|------|
| 01 | City Listings EDA: does size or location drive price? | wrangling, EDA, correlation, OLS on log price | [01-eda-city-listings](./01-eda-city-listings/) |
| 02 | House Price Regression | feature engineering, overfitting, Ridge, Lasso | [02-regression-house-prices](./02-regression-house-prices/) |
| 03 | Air Quality Time Series | lag features, SARIMA, recursive forecasting | [03-time-series-air-quality](./03-time-series-air-quality/) |
| 04 | Hospital Readmission Classification | leakage-aware splitting, logistic regression, decision tree, classification metrics | [04-classification-hospital-readmission](./04-classification-hospital-readmission/) |
| 05 | Fraud Detection with Ensembles | Random Forest, gradient boosting, class imbalance, PR-AUC | [05-ensembles-fraud-detection](./05-ensembles-fraud-detection/) |
| 06 | Customer Segmentation with Clustering | RFM, K-Means, silhouette, segment naming | [06-clustering-customer-segmentation](./06-clustering-customer-segmentation/) |
| 07 | A/B Testing: Cookie Cats Retention | chi-square, power, SRM, SQLite ETL, Streamlit dashboard | [07-experimentation-ab-testing](./07-experimentation-ab-testing/) |
| 08 | Volatility GARCH Pipeline (separate repo) | GARCH volatility modeling, tests, packaging | [volatility-garch-pipeline](../volatility-garch-pipeline/) |

## What's inside each notebook

Every project notebook is written to be read on its own, not just run. Each one includes:

- a **TL;DR** with the headline numbers;
- the **question and why it matters**, in my own words;
- **data provenance** and licence, with exact download steps;
- **cleaning as decisions**, including what each filter costs;
- **EDA with interpretation** — every chart says what to look for and what it means;
- a **baseline, then an improved model**, with the reasoning for each;
- **metrics explained in plain language**, including what they do and do not imply;
- **limitations and next steps** that are specific to the dataset;
- a short **reference list**.

The notebooks are executed with their outputs saved, so the charts and metrics render on GitHub
without running anything.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook
# open any 0X-*/notebook.ipynb
```

Each project folder has its own `README.md` with the dataset link, licence, download steps, key
results, and skills shown. Datasets are **not committed**; download them into that project's `data/`
folder (git-ignored) following its README.

The A/B testing project also ships a dashboard:

```bash
cd 07-experimentation-ab-testing
jupyter notebook notebook.ipynb   # builds data/cookie_cats.db
streamlit run app.py
```

## Structure

- `templates/`: blank notebook + project README templates
- `01-...` through `07-...`: notebook projects (each: `README.md`, `notebook.ipynb`, `data/.gitkeep`)
- [`07-experimentation-ab-testing/app.py`](./07-experimentation-ab-testing/app.py): Streamlit dashboard for the A/B test
- `../volatility-garch-pipeline/`: separate repo with a GARCH volatility pipeline (`src/`, tests, and
  exploration notebook)

## Data and reproducibility notes

- All datasets are **public** but are not redistributed here. Each project README has the exact source,
  licence note, and download command.
- Where a Kaggle account is required (Ames, credit-card fraud, Cookie Cats), the README documents a
  public mirror (OpenML or GitHub) that was used to fetch the same data. Provenance is stated in the
  notebook and README rather than hidden.
- The New York City Airbnb snapshot, the UCI hospital data, and the UCI Online Retail workbook are
  downloaded directly from their publishers.
- Notebook runs are deterministic where it matters: all splits and models use fixed random seeds.
- Expected runtimes: 01 ≈ 20–40s, 02 ≈ 30–60s, 03 ≈ 50–70s, 04 ≈ 30–60s, 05 ≈ 1–2 min,
  06 ≈ 60–90s (Excel read dominates), 07 ≈ 10s. Times are for a laptop.

## Stack

Python · pandas · NumPy · scikit-learn · statsmodels · SciPy · matplotlib · Streamlit · SQLite ·
Jupyter

The separate volatility repo adds `yfinance` and `arch` for GARCH modelling.

## Why this repo exists

I'm moving from data engineering into Forward Deployed Engineering and data science/ML/AI roles.
WQU's Applied Data Science Lab is where I built the foundation; since that coursework can't be
shared, these projects are how I demonstrate the same range on my own. Each one isolates a core skill
(EDA, regression, time series, classification, ensembles, clustering, experimentation) on a real
public dataset rather than following a tutorial end to end. Next up: deep learning fundamentals and
applied LLM/AI projects, building on the modeling and experimentation habits practiced here.

For work history, credentials, and the full skill set, see the [portfolio](https://cancinoray.netlify.app/) and [resume](https://cancinoray.netlify.app/assets/resume.pdf).
