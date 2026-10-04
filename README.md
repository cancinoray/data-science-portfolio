# Data Science Portfolio: Raymond Cancino

[![Portfolio](https://img.shields.io/badge/portfolio-cancinoray.netlify.app-0a66c2)](https://cancinoray.netlify.app/)
[![Resume](https://img.shields.io/badge/resume-PDF-informational)](https://cancinoray.netlify.app/assets/resume.pdf)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-cancinoraymond-0a66c2)](https://www.linkedin.com/in/cancinoraymond/)
[![WQU Applied Data Science Lab](https://img.shields.io/badge/WQU-Applied%20Data%20Science%20Lab-ff6600)](https://www.credly.com/badges/c7bfe8cd-3e7e-4c8d-a2c5-c533de00db49)

Hi, I'm [Raymond Cancino](https://cancinoray.netlify.app/): a Data Engineer transitioning into **Forward Deployed Engineering** and **Data Science, Machine Learning, and AI**. Philippines-based.

I help e-commerce and ops teams make sense of data that doesn't agree with itself. Across e-commerce, AdTech, and EdTech I've built pipelines that survive inconsistent schemas and mismatched platforms, then shipped the fix (the mix of client-facing problem-solving and hands-on engineering that FDE work calls for). That same data-engineering background is what this repo builds on: moving from *delivering clean data* to *extracting the signal in it*, with modeling, forecasting, and experimentation, and an eye toward applied ML/AI next. Mechanical Engineering graduate and former university instructor, comfortable structuring ambiguous problems and explaining results plainly.

- Portfolio: https://cancinoray.netlify.app/
- Resume / CV: https://cancinoray.netlify.app/assets/resume.pdf
- Email: cancinoray@gmail.com · LinkedIn: [/in/cancinoraymond](https://www.linkedin.com/in/cancinoraymond/) · GitHub: [@cancinoray](https://github.com/cancinoray)
- Open to Data Science, ML/AI, FDE, and Data Engineering roles

I completed WorldQuant University's **Applied Data Science Lab** in 2026 ([verify on Credly](https://www.credly.com/badges/c7bfe8cd-3e7e-4c8d-a2c5-c533de00db49)), where I worked through the full applied data science workflow (wrangling, regression, classification, time series, and dashboards) on real-world datasets. WQU's academic policy doesn't allow sharing or reusing coursework, so this repo is how I demonstrate those same skills: **every project here is scaffolded from scratch**, with my own questions, code, and datasets, built to mirror the breadth of what I practiced in the program without reusing any of its assignments, text, or code.

This repo is a focused data science companion to that transition: 7 original notebook projects + 1 packaged volatility pipeline, covering EDA → regression → time series → classification → ensembles → clustering → experimentation. Each project is scoped to practice one core skill end-to-end rather than stack everything into one notebook.

> All projects here are **original work**: my own questions, code, and writing on public datasets. No coursework assignments, text, code, or proprietary datasets are reused here.

## Projects

| # | Title | Skills shown | Link |
|---|-------|--------------|------|
| 01 | City Listings EDA: does size or location drive price? | wrangling, EDA, correlation | [01-eda-city-listings](./01-eda-city-listings/) |
| 02 | House Price Regression | linear regression, overfitting, Ridge, Lasso | [02-regression-house-prices](./02-regression-house-prices/) |
| 03 | Air Quality Time Series | lag features, AR, ARMA forecasting | [03-time-series-air-quality](./03-time-series-air-quality/) |
| 04 | Hospital Readmission Classification | logistic regression, decision tree, classification metrics | [04-classification-hospital-readmission](./04-classification-hospital-readmission/) |
| 05 | Fraud Detection with Ensembles | Random Forest, gradient boosting, class imbalance | [05-ensembles-fraud-detection](./05-ensembles-fraud-detection/) |
| 06 | Customer Segmentation with Clustering | clustering, interpretability, segment naming | [06-clustering-customer-segmentation](./06-clustering-customer-segmentation/) |
| 07 | A/B Testing: Cookie Cats Retention | hypothesis testing (chi-square), ETL into SQLite, Streamlit dashboard | [07-experimentation-ab-testing](./07-experimentation-ab-testing/) |
| 08 | Volatility GARCH Pipeline (separate repo) | GARCH volatility modeling, tests, packaging | [volatility-garch-pipeline](../volatility-garch-pipeline/) |

## How to run

```bash
pip install -r requirements.txt
jupyter notebook
# open any 0X-*/notebook.ipynb
```

Each project folder has its own `README.md` with dataset link + license, download steps, key results, and skills shown. Datasets are **not** committed; download them following the instructions in each project README into that project's `data/` folder.

## Structure

- `templates/`: blank notebook + project README templates
- `01-...` through `07-...`: notebook projects (each: `README.md`, `notebook.ipynb`, `data/.gitkeep`)
- `../volatility-garch-pipeline/`: separate repo with a GARCH volatility pipeline (`src/`, tests, and exploration notebook)

## Stack

Python · pandas · scikit-learn · statsmodels · imbalanced-learn · plotly · Streamlit · SQLite/SQLAlchemy · yfinance · arch

## Why this repo exists

I'm moving from data engineering into Forward Deployed Engineering and data science/ML/AI roles. WQU's Applied Data Science Lab is where I built the foundation; since that coursework can't be shared, these projects are how I demonstrate the same range on my own. Each one isolates a core skill (EDA, regression, time series, classification, ensembles, clustering, experimentation) on a real public dataset rather than following a tutorial end to end. Next up: deep learning fundamentals and applied LLM/AI projects, building on the modeling and experimentation habits practiced here.

For work history, credentials, and the full skill set, see the [portfolio](https://cancinoray.netlify.app/) and [resume](https://cancinoray.netlify.app/assets/resume.pdf).
