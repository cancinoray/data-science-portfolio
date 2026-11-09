"""Unified portfolio dashboard for the seven data science projects.

Run from the repository root:

    streamlit run dashboard/app.py

The app is intentionally data-independent: it summarises results from the
executed notebooks (already committed) and links back to each notebook for the
full analysis. That keeps it deployable without committing the datasets.
"""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page config and design tokens
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Raymond Cancino · Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#12355B"
TEAL = "#1B998B"
ORANGE = "#E07A5F"
GITHUB = "https://github.com/cancinoray/data-science-portfolio"
BLOB = f"{GITHUB}/blob/main"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .stApp { background: #F6F7F9; }
    .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 4rem; }
    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E4E7EC;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

    h1, h2, h3, h4 {
        font-family: 'Source Serif 4', Georgia, serif;
        color: #102A43;
        letter-spacing: -0.01em;
    }
    a { color: #1B5E8C; }

    .eyebrow {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #1B998B;
        margin-bottom: 0.35rem;
    }
    .hero { padding: 1.2rem 0 2.2rem; }
    .hero h1 {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: clamp(2.5rem, 5vw, 4rem);
        line-height: 1.02;
        color: #102A43;
        margin: 0.35rem 0 1rem;
        letter-spacing: -0.025em;
    }
    .hero p {
        max-width: 760px;
        color: #475467;
        font-size: 1.06rem;
        line-height: 1.65;
        margin-bottom: 0.9rem;
    }
    .tag-row { margin-top: 1rem; }
    .tag {
        display: inline-block;
        padding: 0.26rem 0.62rem;
        border-radius: 999px;
        background: #EEF4F3;
        color: #1F5F58;
        font-size: 0.73rem;
        font-weight: 600;
        margin: 0 0.3rem 0.35rem 0;
        border: 1px solid #D6E7E4;
    }

    .page-title { font-size: clamp(2rem, 4vw, 2.9rem); margin-bottom: 0.15rem; }
    .page-sub { color: #5B6B7C; font-size: 1.05rem; margin-top: 0; margin-bottom: 1.6rem; }

    .kpi {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 14px;
        padding: 0.95rem 1.05rem;
        min-height: 108px;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
    }
    .kpi-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #667085;
        margin-bottom: 0.35rem;
    }
    .kpi-value { font-size: 1.65rem; font-weight: 700; color: #12355B; line-height: 1.15; }
    .kpi-note { font-size: 0.73rem; color: #667085; margin-top: 0.3rem; line-height: 1.35; }
    .context {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        min-height: 96px;
    }
    .context-label {
        font-size: 0.64rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #667085;
    }
    .context-value { font-size: 0.94rem; font-weight: 600; color: #12355B; margin-top: 0.2rem; line-height: 1.3; }
    .context-note { font-size: 0.72rem; color: #667085; margin-top: 0.15rem; }

    .card-kicker {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #1B998B;
        margin-bottom: 0.25rem;
    }
    .card-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #102A43;
        line-height: 1.2;
        margin-bottom: 0.35rem;
    }
    .card-result { color: #475467; font-size: 0.9rem; line-height: 1.5; min-height: 3.4rem; }
    .card-tags { margin: 0.55rem 0 0.9rem; }

    .takeaway {
        border-left: 3px solid #1B998B;
        background: #F0F7F6;
        padding: 0.95rem 1.1rem;
        border-radius: 0 10px 10px 0;
        color: #1F3A3A;
        font-size: 0.95rem;
        line-height: 1.55;
        margin: 1.2rem 0 0.4rem;
    }
    .chart-title {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #667085;
        margin-bottom: 0.15rem;
    }
    .footer {
        border-top: 1px solid #E4E7EC;
        margin-top: 2.6rem;
        padding-top: 1rem;
        color: #667085;
        font-size: 0.8rem;
        line-height: 1.6;
    }
    .brand-mark {
        width: 40px; height: 40px; border-radius: 50%;
        background: #12355B; color: #FFFFFF;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 0.85rem; letter-spacing: 0.03em;
        margin-bottom: 0.65rem;
    }

    .stButton > button {
        border-radius: 999px;
        border: 1px solid #12355B;
        color: #12355B;
        background: #FFFFFF;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 0.42rem 0.9rem;
    }
    .stButton > button:hover {
        background: #12355B;
        color: #FFFFFF;
        border-color: #12355B;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #E4E7EC;
        border-radius: 12px;
        background: #FFFFFF;
    }
    div[data-testid="stDataFrame"] { border-radius: 12px; }

    @media (max-width: 768px) {
        .hero h1 { font-size: 2.35rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .kpi { min-height: auto; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Small rendering helpers
# ---------------------------------------------------------------------------
def kpi_row(metrics: list[tuple[str, str, str]]) -> None:
    columns = st.columns(len(metrics), gap="medium")
    for column, (label, value, note) in zip(columns, metrics):
        column.markdown(
            f"""
            <div class="kpi">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{value}</div>
              <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def context_row(items: list[tuple[str, str, str]]) -> None:
    columns = st.columns(len(items), gap="medium")
    for column, (label, value, note) in zip(columns, items):
        column.markdown(
            f"""
            <div class="context">
              <div class="context-label">{label}</div>
              <div class="context-value">{value}</div>
              <div class="context-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)


def page_header(project: dict) -> None:
    st.markdown(
        f"""
        <div class="eyebrow">Project {project['id']} · {project['eyebrow']}</div>
        <h1 class="page-title">{project['icon']} {project['title']}</h1>
        <p class="page-sub">{project['subtitle']}</p>
        """,
        unsafe_allow_html=True,
    )


def style_chart(chart: alt.Chart, height: int = 340) -> alt.Chart:
    return (
        chart.properties(height=height)
        .configure_view(stroke=None)
        .configure_axis(
            labelFont="Inter",
            titleFont="Inter",
            labelColor="#475467",
            titleColor="#475467",
            gridColor="#E4E7EC",
            domain=False,
            ticks=False,
            labelFontSize=11,
            titleFontSize=11,
            titlePadding=10,
        )
        .configure_legend(
            labelFont="Inter",
            titleFont="Inter",
            labelColor="#475467",
            orient="bottom",
            direction="horizontal",
        )
    )


def show_chart(chart: alt.Chart, height: int = 340) -> None:
    st.altair_chart(style_chart(chart, height), width="stretch", theme=None)


def link_row(project: dict) -> None:
    columns = st.columns(3, gap="small")
    columns[0].link_button("Notebook", project["notebook"], width="stretch")
    columns[1].link_button("README", project["readme"], width="stretch")
    columns[2].link_button("Repository", GITHUB, width="stretch")


def navigate(label: str) -> None:
    st.session_state["nav"] = label


# ---------------------------------------------------------------------------
# Project data: headline metrics and short narratives from the notebooks
# ---------------------------------------------------------------------------
PROJECTS = [
    {
        "id": "01",
        "slug": "city-listings",
        "nav": "🏙️  01 · City Listings",
        "eyebrow": "Exploratory analysis",
        "title": "City Listings EDA",
        "subtitle": "Does size or location drive nightly price?",
        "icon": "🏙️",
        "tags": ["EDA", "OLS", "Cross-validation"],
        "card_result": "Size and location are complementary; the full model reaches CV R² 0.495.",
        "metrics": [
            ("Listings analysed", "20,320", "after cleaning"),
            ("Median price", "$172", "per night"),
            ("Full-model CV R²", "0.495", "5-fold"),
            ("Holdout MAE", "$92", "per night"),
        ],
        "findings": [
            "Location alone (CV R² 0.265) slightly beats size alone (0.234), but the two together nearly double either (0.469).",
            "Adding location to a size + room-type model lifts R² by 0.175; adding size the other way adds 0.115.",
            "The full model explains about half of log-price variation; a 36.6% median percentage error is too wide to price individual listings.",
            "29% of listings have no price, and missingness is not random across boroughs — the sample is not the whole market.",
        ],
        "method": (
            "Inside Airbnb NYC snapshot (2026-06-14): 30,259 listings, 20,320 after dropping missing prices "
            "and filtering to $20–$1,000 and minimum nights ≤ 30. Target is log price; 5-fold CV and an "
            "80/20 holdout; OLS with median imputation and one-hot neighbourhoods."
        ),
        "caveat": "Asking prices, not transactions; 50% of variation is unexplained; one snapshot.",
        "chart_title": "Model comparison — 5-fold CV R²",
        "chart2_title": "Median nightly price by borough",
        "context": [
            ("Dataset", "Inside Airbnb NYC", "2026 snapshot"),
            ("Sample", "20,320 listings", "after cleaning"),
            ("Validation", "5-fold CV + 80/20", "log-price OLS"),
        ],
        "table_title": "Model comparison",
        "table": pd.DataFrame(
            {
                "Model": ["Median baseline", "Size", "Location", "Size + location", "Full (+ room type)"],
                "CV R²": [0.000, 0.234, 0.265, 0.469, 0.495],
                "Holdout R²": [0.000, 0.239, 0.252, 0.468, 0.498],
                "MAE": ["$126", "$114", "$108", "$94", "$92"],
            }
        ),
        "notebook": f"{BLOB}/01-eda-city-listings/notebook.ipynb",
        "readme": f"{BLOB}/01-eda-city-listings/README.md",
    },
    {
        "id": "02",
        "slug": "house-prices",
        "nav": "🏠  02 · House Prices",
        "eyebrow": "Regression",
        "title": "House Price Regression",
        "subtitle": "Can regularised regression beat OLS on Ames housing?",
        "icon": "🏠",
        "tags": ["Feature engineering", "Overfitting", "Ridge", "Lasso"],
        "card_result": "Engineered OLS reaches holdout R² 0.913; regularisation buys stability, not a holdout win.",
        "metrics": [
            ("Holdout R²", "0.913", "full OLS"),
            ("RMSE", "$22,788", "holdout"),
            ("MAE", "$15,195", "holdout"),
            ("Lasso features", "80 / 297", "alpha = 0.001"),
        ],
        "findings": [
            r"Engineered OLS cuts holdout RMSE from \$35,978 (3-feature baseline) to \$22,788.",
            r"Training R² 0.945 vs holdout 0.913 shows the overfitting gap; a degree-10 polynomial on 200 houses drives holdout RMSE to \$188k.",
            "Ridge/Lasso cut CV log-RMSE from 0.163 to 0.140/0.138, but the single 292-house holdout slightly prefers OLS (0.913 vs 0.901/0.899).",
            "Lasso keeps only 80 of 297 encoded features, mostly size and quality.",
        ],
        "method": (
            "Ames Housing: 1,460 sales, 79 predictors. Log target; ordinal quality mapping; engineered "
            "TotalSF, TotalBath, HouseAge, RemodAge, TotalPorch, HasPool, HasGarage; median imputation "
            "and one-hot encoding inside the pipeline; 80/20 split and 5-fold CV alpha selection."
        ),
        "caveat": "1,460 rows, one market; CV and holdout disagree; log back-transform estimates a median.",
        "chart_title": "Overfitting in one picture — polynomial degree vs RMSE",
        "chart2_title": "Holdout RMSE by model",
        "context": [
            ("Dataset", "Ames Housing", "1,460 sales"),
            ("Predictors", "79 → 297 encoded", "after engineering"),
            ("Validation", "80/20 + 5-fold CV", "alpha selected by CV"),
        ],
        "table_title": "Model comparison",
        "table": pd.DataFrame(
            {
                "Model": ["Baseline (3 features)", "Full OLS", "Ridge (alpha 30)", "Lasso (alpha 0.001)"],
                "Holdout R²": [0.812, 0.913, 0.901, 0.899],
                "RMSE": ["$35,978", "$22,788", "$25,704", "$25,521"],
                "MAE": ["$23,609", "$15,195", "$16,254", "$16,211"],
            }
        ),
        "notebook": f"{BLOB}/02-regression-house-prices/notebook.ipynb",
        "readme": f"{BLOB}/02-regression-house-prices/README.md",
    },
    {
        "id": "03",
        "slug": "air-quality",
        "nav": "🌫️  03 · Air Quality",
        "eyebrow": "Time series",
        "title": "Air Quality Forecasting",
        "subtitle": "Can I forecast NYC PM2.5, and for how long?",
        "icon": "🌫️",
        "tags": ["SARIMA", "Lag features", "Recursive forecasting"],
        "card_result": "Ridge lag model beats a seasonal baseline at 90 days; skill fades with horizon.",
        "metrics": [
            ("90-day RMSE", "6.45 µg/m³", "Ridge lag model"),
            ("One-step RMSE", "5.42 µg/m³", "Ridge"),
            ("Seasonal baseline", "7.08 µg/m³", "static 90-day"),
            ("Hours modelled", "17,544", "2023–2024"),
        ],
        "findings": [
            "Static 90-day RMSE: Ridge 6.45 vs SARIMA 6.79 vs seasonal naive 7.08 µg/m³.",
            "One-step RMSE: Ridge 5.42 vs SARIMA 5.96, random walk 6.18, seasonal naive 7.76.",
            "Skill is horizon-dependent: Ridge is lowest from 30 days onward, but every model misses the December spike.",
            "The weekly cycle is weak; the random walk beats seasonal naive at one step.",
        ],
        "method": (
            "Open-Meteo hourly PM2.5 for NYC (17,544 hours, 2023–2024), aggregated to daily means. "
            "Last 90 days held out chronologically. Baselines: random walk and seasonal naive, in both "
            "one-step and static regimes. Models: SARIMA(2,0,1)(0,0,1,7) on log PM2.5; Ridge on 14 lags, "
            "rolling means, day-of-week, and annual Fourier terms."
        ),
        "caveat": "One city, two years, no weather inputs; point forecasts only; modelled/reanalysis data.",
        "chart_title": "Forecast error by horizon",
        "chart2_title": "Static 90-day RMSE by model",
        "context": [
            ("Dataset", "Open-Meteo NYC PM2.5", "hourly"),
            ("Sample", "17,544 hours", "2023–2024"),
            ("Validation", "last 90 days", "chronological"),
        ],
        "table_title": "Cumulative RMSE over the first h days",
        "table": pd.DataFrame(
            {
                "Horizon (days)": [1, 7, 14, 30, 60, 90],
                "Seasonal naive": [2.50, 1.59, 2.69, 4.41, 4.58, 7.08],
                "SARIMA": [2.27, 2.92, 4.26, 4.10, 4.49, 6.79],
                "Ridge": [1.95, 2.33, 3.50, 3.62, 4.09, 6.45],
            }
        ),
        "notebook": f"{BLOB}/03-time-series-air-quality/notebook.ipynb",
        "readme": f"{BLOB}/03-time-series-air-quality/README.md",
    },
    {
        "id": "04",
        "slug": "readmission",
        "nav": "🏥  04 · Readmission",
        "eyebrow": "Classification",
        "title": "Hospital Readmission",
        "subtitle": "Can administrative data predict 30-day readmission?",
        "icon": "🏥",
        "tags": ["Classification", "Class imbalance", "Leakage-aware splits"],
        "card_result": "88.8% accuracy hides 2.5% recall. Balanced logistic recall: 54.3%.",
        "metrics": [
            ("Accuracy", "88.8%", "unweighted logistic"),
            ("Recall", "54.3%", "balanced, threshold 0.5"),
            ("Precision", "18.2%", "balanced, threshold 0.5"),
            ("ROC-AUC", "0.667", "holdout"),
        ],
        "findings": [
            "The unweighted logistic model is 88.8% accurate but catches only 2.5% of readmissions — the accuracy trap.",
            "Balanced logistic reaches 54.3% recall at 18.2% precision (F1 0.273); a depth-5 tree is similar (recall 56.6%, F1 0.268).",
            "Prior inpatient visits dominate (odds ratio 1.44 per prior admission), followed by diagnoses, emergency visits, and age.",
            "Threshold 0.5 flags 33% of patients; 0.3 catches 98.7% but flags 95%.",
        ],
        "method": (
            "UCI Diabetes 130-US Hospitals: 101,766 encounters, 99,343 after removing death/hospice "
            "discharges. GroupShuffleSplit by patient removes leakage. Logistic regression and a depth-5 "
            "tree; class weights; threshold analysis on the 19,802-encounter holdout."
        ),
        "caveat": "Administrative data, 1999–2008; weak signal; no calibration or fairness audit yet.",
        "chart_title": "Precision/recall trade-off — balanced logistic",
        "chart2_title": "Precision, recall, and F1 by model",
        "context": [
            ("Dataset", "UCI Diabetes 130", "1999–2008"),
            ("Sample", "99,343 encounters", "71,518 patients"),
            ("Validation", "patient-grouped 80/20", "no patient overlap"),
        ],
        "table_title": "Model comparison",
        "table": pd.DataFrame(
            {
                "Model": ["Logistic (unweighted)", "Logistic (balanced)", "Decision tree (depth 5)"],
                "Accuracy": [0.888, 0.676, 0.654],
                "Precision": [0.491, 0.182, 0.176],
                "Recall": [0.025, 0.543, 0.566],
                "F1": [0.047, 0.273, 0.268],
                "ROC-AUC": [0.665, 0.667, 0.652],
            }
        ),
        "notebook": f"{BLOB}/04-classification-hospital-readmission/notebook.ipynb",
        "readme": f"{BLOB}/04-classification-hospital-readmission/README.md",
    },
    {
        "id": "05",
        "slug": "fraud",
        "nav": "🕵️  05 · Fraud Detection",
        "eyebrow": "Ensembles & imbalance",
        "title": "Fraud Detection",
        "subtitle": "What happens when only 0.17% of transactions are fraudulent?",
        "icon": "🕵️",
        "tags": ["Random Forest", "PR-AUC", "Cost-sensitive thresholds"],
        "card_result": "Random Forest PR-AUC 0.782; a cost-aware threshold catches 77% of frauds.",
        "metrics": [
            ("PR-AUC", "0.782", "Random Forest"),
            ("ROC-AUC", "0.935", "Random Forest"),
            ("Precision @0.5", "97.3%", "36 TP, 1 FP"),
            ("Recall @0.5", "69.2%", "36 of 52 frauds"),
        ],
        "findings": [
            "Random Forest PR-AUC 0.782 vs logistic 0.723, but RF ROC-AUC 0.935 vs logistic 0.977 — PR is the honest metric here.",
            "At 0.5, the Random Forest catches 36 of 52 frauds with 1 false alarm (97.3% precision, 69.2% recall).",
            r"A cost-optimal threshold of 0.055 catches 40 of 52 frauds (76.9% recall, 47.6% precision) under \$150/\$5 costs.",
            "Class weighting lifts PR-AUC from 0.743 to 0.782 while lowering ROC-AUC from 0.951 to 0.935.",
        ],
        "method": (
            "ULB credit-card data: 284,807 transactions, 492 frauds; 1,081 duplicates removed. "
            "Chronological 70/15/15 split; class-weighted logistic, Random Forest, and histogram gradient "
            "boosting; PR-AUC, threshold trade-offs, and cost-based selection."
        ),
        "caveat": "Two days of anonymised data; costs are illustrative; drift and calibration not modelled.",
        "chart_title": "Random Forest — precision/recall by threshold",
        "chart2_title": "PR-AUC vs ROC-AUC by model",
        "context": [
            ("Dataset", "ULB credit-card fraud", "48 hours"),
            ("Sample", "283,726 transactions", "492 frauds"),
            ("Validation", "70/15/15 chronological", "threshold on validation"),
        ],
        "table_title": "Model comparison",
        "table": pd.DataFrame(
            {
                "Model": ["Logistic (balanced)", "Random Forest", "Hist. gradient boosting"],
                "PR-AUC": [0.723, 0.782, 0.725],
                "ROC-AUC": [0.977, 0.935, 0.926],
                "Precision @0.5": [0.021, 0.973, 0.312],
                "Recall @0.5": [0.885, 0.692, 0.769],
            }
        ),
        "notebook": f"{BLOB}/05-ensembles-fraud-detection/notebook.ipynb",
        "readme": f"{BLOB}/05-ensembles-fraud-detection/README.md",
    },
    {
        "id": "06",
        "slug": "segmentation",
        "nav": "👥  06 · Segmentation",
        "eyebrow": "Clustering",
        "title": "Customer Segmentation",
        "subtitle": "What customer segments exist, and which ones pay the bills?",
        "icon": "👥",
        "tags": ["RFM", "K-Means", "Silhouette"],
        "card_result": "Champions are 7.8% of customers but 52.9% of revenue.",
        "metrics": [
            ("Customers", "4,338", "RFM profiles"),
            ("Segments", "5", "K-Means, k = 5"),
            ("Champions", "7.8%", "of customers"),
            ("Revenue share", "52.9%", "generated by Champions"),
        ],
        "findings": [
            "Champions: 7.8% of customers, 52.9% of revenue. Hibernating: 27.9% of customers, only 3.8% of revenue.",
            "Raw RFM silhouette 0.617 is an outlier artefact (clusters of 6 and 8); log-RFM k=5 gives 0.316 and usable segments.",
            "At-risk segment: 1,018 customers, 16.6% of revenue, 104 days since last purchase — the retention target.",
            "Each segment gets a different action: retain, grow, win back, convert, or suppress.",
        ],
        "method": (
            "UCI Online Retail: 541,909 line items, 392,692 after removing guest checkouts, returns, "
            "zero prices, and duplicates; 4,338 customers. RFM with a 2011-12-10 snapshot; log1p + "
            "standardise; K-Means k=5 chosen for interpretability; silhouette, revenue share, and ARI stability."
        ),
        "caveat": "Guest customers excluded; gross spend, not net of returns; k and segment names are judgement calls.",
        "chart_title": "Customer share vs revenue share",
        "chart2_title": "Average monetary value by segment",
        "context": [
            ("Dataset", "UCI Online Retail", "Dec 2010–Dec 2011"),
            ("Sample", "4,338 customers", "392,692 line items"),
            ("Validation", "k = 5, ARI 0.92", "silhouette 0.316"),
        ],
        "table_title": "Segment profiles",
        "table": pd.DataFrame(
            {
                "Segment": ["Champions", "Loyal", "At risk", "New / promising", "Hibernating"],
                "Customers": [339, 938, 1018, 834, 1209],
                "Share": ["7.8%", "21.6%", "23.5%", "19.2%", "27.9%"],
                "Avg recency": ["12 d", "19 d", "104 d", "27 d", "208 d"],
                "Avg monetary": ["£13,877", "£2,179", "£1,452", "£390", "£277"],
                "Revenue share": ["52.9%", "23.0%", "16.6%", "3.7%", "3.8%"],
            }
        ),
        "notebook": f"{BLOB}/06-clustering-customer-segmentation/notebook.ipynb",
        "readme": f"{BLOB}/06-clustering-customer-segmentation/README.md",
    },
    {
        "id": "07",
        "slug": "ab-testing",
        "nav": "🐱  07 · A/B Testing",
        "eyebrow": "Experimentation",
        "title": "Cookie Cats A/B Test",
        "subtitle": "Does moving the gate from level 30 to 40 hurt retention?",
        "icon": "🐱",
        "tags": ["Chi-square", "Power", "SRM", "SQLite + Streamlit"],
        "card_result": "Gate 30 keeps 7-day retention 0.82 pp higher (p = 0.0016).",
        "metrics": [
            ("Players", "90,189", "two arms"),
            ("7-day lift", "+0.82 pp", "gate 30 vs 40"),
            ("p-value", "0.0016", "chi-square"),
            ("SRM p-value", "0.0086", "sample-ratio check"),
        ],
        "findings": [
            "7-day retention 19.02% vs 18.20% (+0.82 pp, p = 0.0016); 1-day retention 44.82% vs 44.23% (p = 0.074).",
            "The effect survives Bonferroni correction for two metrics and removing a 49,854-round outlier.",
            "A sample-ratio mismatch (p = 0.0086) is flagged, but the 1.75% imbalance does not explain the gap.",
            "The minimum detectable effect is 0.73 pp at 80% power; the observed 0.82 pp is just above it.",
        ],
        "method": (
            "Cookie Cats experiment: 90,189 players, gate_30 control vs gate_40 treatment. Two-sided "
            "chi-square, Wilson intervals, effect sizes, Bonferroni and BH corrections, power/MDE, SRM, "
            "outlier sensitivity, SQLite ETL, and a Streamlit dashboard."
        ),
        "caveat": "One game, one experiment; no revenue; SRM; post-treatment engagement is not a covariate.",
        "chart_title": "Retention by arm",
        "chart2_title": "Lift with 95% confidence interval",
        "context": [
            ("Dataset", "Cookie Cats A/B test", "mobile game"),
            ("Sample", "90,189 players", "44,700 vs 45,489"),
            ("Validation", "chi-square + power + SRM", "Bonferroni α = 0.025"),
        ],
        "table_title": "Experiment results",
        "table": pd.DataFrame(
            {
                "Metric": ["1-day retention", "7-day retention"],
                "gate_30": ["44.82%", "19.02%"],
                "gate_40": ["44.23%", "18.20%"],
                "Difference": ["+0.59 pp", "+0.82 pp"],
                "p-value": [0.074, 0.0016],
            }
        ),
        "notebook": f"{BLOB}/07-experimentation-ab-testing/notebook.ipynb",
        "readme": f"{BLOB}/07-experimentation-ab-testing/README.md",
    },
]

PROJECT_BY_NAV = {p["nav"]: p for p in PROJECTS}
NAV_OPTIONS = ["Overview"] + [p["nav"] for p in PROJECTS]


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
def chart_01() -> None:
    df = pd.DataFrame(
        {
            "model": ["Median", "Size", "Location", "Size + location", "Full"],
            "r2": [0.000, 0.234, 0.265, 0.469, 0.495],
        }
    )
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("model:N", sort=list(df["model"]), axis=alt.Axis(title=None, labelAngle=0)),
            y=alt.Y("r2:Q", axis=alt.Axis(title="5-fold CV R²", format=".2f")),
            color=alt.condition(
                alt.datum.model == "Full", alt.value(ORANGE), alt.value(NAVY)
            ),
            tooltip=[
                alt.Tooltip("model:N", title="Model"),
                alt.Tooltip("r2:Q", title="CV R²", format=".3f"),
            ],
        )
    )
    show_chart(chart)


def chart_02() -> None:
    df = pd.DataFrame(
        {
            "degree": list(range(1, 11)),
            "Train": [55183, 51555, 51528, 51166, 50712, 50195, 49944, 50219, 51022, 52177],
            "Holdout": [57951, 67654, 68360, 71675, 71993, 72339, 75477, 86262, 115373, 187985],
        }
    ).melt(id_vars="degree", var_name="split", value_name="rmse")

    chart = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(size=55, filled=True), strokeWidth=2.5)
        .encode(
            x=alt.X("degree:O", axis=alt.Axis(title="Polynomial degree", labelAngle=0)),
            y=alt.Y(
                "rmse:Q",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(title="RMSE ($, log scale)", format="~s", tickCount=5),
            ),
            color=alt.Color(
                "split:N",
                scale=alt.Scale(domain=["Train", "Holdout"], range=[TEAL, ORANGE]),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("degree:O", title="Degree"),
                alt.Tooltip("split:N", title="Split"),
                alt.Tooltip("rmse:Q", title="RMSE", format="$,.0f"),
            ],
        )
    )
    show_chart(chart)


def chart_03() -> None:
    df = pd.DataFrame(
        {
            "horizon": [1, 7, 14, 30, 60, 90],
            "Seasonal naive": [2.50, 1.59, 2.69, 4.41, 4.58, 7.08],
            "SARIMA": [2.27, 2.92, 4.26, 4.10, 4.49, 6.79],
            "Ridge lag model": [1.95, 2.33, 3.50, 3.62, 4.09, 6.45],
        }
    ).melt(id_vars="horizon", var_name="model", value_name="rmse")

    chart = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(size=55, filled=True), strokeWidth=2.5)
        .encode(
            x=alt.X("horizon:O", axis=alt.Axis(title="Forecast horizon (days)", labelAngle=0)),
            y=alt.Y("rmse:Q", axis=alt.Axis(title="Cumulative RMSE (µg/m³)", format=".1f")),
            color=alt.Color(
                "model:N",
                scale=alt.Scale(
                    domain=["Seasonal naive", "SARIMA", "Ridge lag model"],
                    range=["#98A2B3", ORANGE, TEAL],
                ),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("horizon:O", title="Horizon (days)"),
                alt.Tooltip("model:N", title="Model"),
                alt.Tooltip("rmse:Q", title="RMSE", format=".2f"),
            ],
        )
    )
    show_chart(chart)


def chart_04() -> None:
    df = pd.DataFrame(
        {
            "threshold": [0.3, 0.4, 0.5, 0.6, 0.7],
            "Precision": [0.116, 0.140, 0.182, 0.232, 0.301],
            "Recall": [0.987, 0.813, 0.543, 0.311, 0.172],
            "F1": [0.208, 0.239, 0.273, 0.266, 0.219],
        }
    ).melt(id_vars="threshold", var_name="metric", value_name="score")

    chart = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(size=55, filled=True), strokeWidth=2.5)
        .encode(
            x=alt.X("threshold:Q", axis=alt.Axis(title="Decision threshold", format=".1f")),
            y=alt.Y(
                "score:Q",
                scale=alt.Scale(domain=[0, 1]),
                axis=alt.Axis(title="Score", format=".1f"),
            ),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(domain=["Precision", "Recall", "F1"], range=[NAVY, ORANGE, TEAL]),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("threshold:Q", title="Threshold", format=".2f"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("score:Q", title="Score", format=".3f"),
            ],
        )
    )
    show_chart(chart)


def chart_05() -> None:
    df = pd.DataFrame(
        {
            "threshold": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            "Precision": [0.736, 0.848, 0.886, 0.950, 0.973, 0.971, 1.000, 1.000, 1.000],
            "Recall": [0.750, 0.750, 0.750, 0.731, 0.692, 0.635, 0.596, 0.481, 0.327],
        }
    ).melt(id_vars="threshold", var_name="metric", value_name="score")

    rule = (
        alt.Chart(pd.DataFrame({"x": [0.055]}))
        .mark_rule(color=TEAL, strokeDash=[4, 4], strokeWidth=1.5)
        .encode(x=alt.X("x:Q"))
    )
    label = (
        alt.Chart(pd.DataFrame({"x": [0.18], "y": [0.06], "text": ["cost-optimal ≈ 0.055"]}))
        .mark_text(align="left", color=TEAL, fontSize=10)
        .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="text:N")
    )
    chart = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(size=55, filled=True), strokeWidth=2.5)
        .encode(
            x=alt.X(
                "threshold:Q",
                scale=alt.Scale(domain=[0, 1]),
                axis=alt.Axis(title="Decision threshold", format=".2f"),
            ),
            y=alt.Y(
                "score:Q",
                scale=alt.Scale(domain=[0, 1]),
                axis=alt.Axis(title="Score", format=".1f"),
            ),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(domain=["Precision", "Recall"], range=[NAVY, ORANGE]),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("threshold:Q", title="Threshold", format=".2f"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("score:Q", title="Score", format=".3f"),
            ],
        )
        + rule
        + label
    )
    show_chart(chart)


def chart_06() -> None:
    segments = ["Champions", "Loyal", "At risk", "New / promising", "Hibernating"]
    df = pd.DataFrame(
        {
            "segment": segments,
            "Customers": [7.8, 21.6, 23.5, 19.2, 27.9],
            "Revenue": [52.9, 23.0, 16.6, 3.7, 3.8],
        }
    ).melt(id_vars="segment", var_name="metric", value_name="share")

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(
                "segment:N",
                sort=segments,
                axis=alt.Axis(title=None, labelAngle=-22, labelLimit=110),
            ),
            xOffset=alt.XOffset("metric:N", sort=["Customers", "Revenue"]),
            y=alt.Y("share:Q", axis=alt.Axis(title="Share (%)", format=".0f")),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(domain=["Customers", "Revenue"], range=[NAVY, TEAL]),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("segment:N", title="Segment"),
                alt.Tooltip("metric:N", title="Share of"),
                alt.Tooltip("share:Q", title="%", format=".1f"),
            ],
        )
    )
    show_chart(chart)


def chart_07() -> None:
    df = pd.DataFrame(
        {
            "arm": ["Control · gate 30", "Treatment · gate 40"],
            "1-day retention": [44.82, 44.23],
            "7-day retention": [19.02, 18.20],
        }
    ).melt(id_vars="arm", var_name="metric", value_name="rate")

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("arm:N", axis=alt.Axis(title=None, labelAngle=0)),
            xOffset=alt.XOffset("metric:N", sort=["1-day retention", "7-day retention"]),
            y=alt.Y(
                "rate:Q",
                scale=alt.Scale(domain=[0, 50]),
                axis=alt.Axis(title="Retention (%)", format=".0f"),
            ),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(
                    domain=["1-day retention", "7-day retention"], range=[NAVY, ORANGE]
                ),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("arm:N", title="Arm"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("rate:Q", title="Rate (%)", format=".2f"),
            ],
        )
    )
    show_chart(chart)



def chart2_01() -> None:
    df = pd.DataFrame(
        {
            "borough": ["Bronx", "Staten Island", "Queens", "Brooklyn", "Manhattan"],
            "median": [106.6, 107.8, 120.2, 151.5, 234.8],
        }
    )
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("borough:N", sort=list(df["borough"]), axis=alt.Axis(title=None, labelAngle=0)),
            y=alt.Y("median:Q", axis=alt.Axis(title="Median nightly price ($)", format="$,.0f")),
            color=alt.condition(
                alt.datum.borough == "Manhattan", alt.value(ORANGE), alt.value(NAVY)
            ),
            tooltip=[
                alt.Tooltip("borough:N", title="Borough"),
                alt.Tooltip("median:Q", title="Median price", format="$,.0f"),
            ],
        )
    )
    show_chart(chart, height=300)


def chart2_02() -> None:
    df = pd.DataFrame(
        {
            "model": ["Baseline", "Full OLS", "Ridge", "Lasso"],
            "rmse": [35978, 22788, 25704, 25521],
        }
    )
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("model:N", sort=list(df["model"]), axis=alt.Axis(title=None, labelAngle=0)),
            y=alt.Y("rmse:Q", axis=alt.Axis(title="Holdout RMSE ($)", format="$,.0f")),
            color=alt.condition(
                alt.datum.model == "Full OLS", alt.value(ORANGE), alt.value(NAVY)
            ),
            tooltip=[
                alt.Tooltip("model:N", title="Model"),
                alt.Tooltip("rmse:Q", title="Holdout RMSE", format="$,.0f"),
            ],
        )
    )
    show_chart(chart, height=300)


def chart2_03() -> None:
    df = pd.DataFrame(
        {
            "model": ["Random walk", "Seasonal naive", "SARIMA", "Ridge"],
            "rmse": [7.31, 7.08, 6.79, 6.45],
        }
    )
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("model:N", sort=list(df["model"]), axis=alt.Axis(title=None, labelAngle=0)),
            y=alt.Y("rmse:Q", axis=alt.Axis(title="Static 90-day RMSE (µg/m³)", format=".2f")),
            color=alt.condition(
                alt.datum.model == "Ridge", alt.value(ORANGE), alt.value(NAVY)
            ),
            tooltip=[
                alt.Tooltip("model:N", title="Model"),
                alt.Tooltip("rmse:Q", title="RMSE", format=".2f"),
            ],
        )
    )
    show_chart(chart, height=300)


def chart2_04() -> None:
    df = pd.DataFrame(
        {
            "model": ["Unweighted", "Balanced", "Tree (depth 5)"],
            "Precision": [0.491, 0.182, 0.176],
            "Recall": [0.025, 0.543, 0.566],
            "F1": [0.047, 0.273, 0.268],
        }
    ).melt(id_vars="model", var_name="metric", value_name="score")

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("model:N", sort=["Unweighted", "Balanced", "Tree (depth 5)"],
                    axis=alt.Axis(title=None, labelAngle=0)),
            xOffset=alt.XOffset("metric:N", sort=["Precision", "Recall", "F1"]),
            y=alt.Y("score:Q", scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(title="Score", format=".1f")),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(domain=["Precision", "Recall", "F1"], range=[NAVY, ORANGE, TEAL]),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("model:N", title="Model"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("score:Q", title="Score", format=".3f"),
            ],
        )
    )
    show_chart(chart, height=300)


def chart2_05() -> None:
    df = pd.DataFrame(
        {
            "model": ["Logistic", "Random Forest", "Hist. GBM"],
            "PR-AUC": [0.723, 0.782, 0.725],
            "ROC-AUC": [0.977, 0.935, 0.926],
        }
    ).melt(id_vars="model", var_name="metric", value_name="score")

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("model:N", sort=["Logistic", "Random Forest", "Hist. GBM"],
                    axis=alt.Axis(title=None, labelAngle=0)),
            xOffset=alt.XOffset("metric:N", sort=["PR-AUC", "ROC-AUC"]),
            y=alt.Y("score:Q", scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(title="Score", format=".1f")),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(domain=["PR-AUC", "ROC-AUC"], range=[NAVY, ORANGE]),
                legend=alt.Legend(title=None, orient="bottom", direction="horizontal"),
            ),
            tooltip=[
                alt.Tooltip("model:N", title="Model"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("score:Q", title="Score", format=".3f"),
            ],
        )
    )
    show_chart(chart, height=300)


def chart2_06() -> None:
    segments = ["Champions", "Loyal", "At risk", "New / promising", "Hibernating"]
    df = pd.DataFrame(
        {
            "segment": segments,
            "avg_value": [13877, 2179, 1452, 390, 277],
        }
    )
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("segment:N", sort=segments, axis=alt.Axis(title=None, labelAngle=0)),
            y=alt.Y("avg_value:Q", axis=alt.Axis(title="Average monetary value (£)", format=",.0f")),
            color=alt.condition(
                alt.datum.segment == "Champions", alt.value(ORANGE), alt.value(NAVY)
            ),
            tooltip=[
                alt.Tooltip("segment:N", title="Segment"),
                alt.Tooltip("avg_value:Q", title="Average monetary", format=",.0f"),
            ],
        )
    )
    show_chart(chart, height=300)


def chart2_07() -> None:
    df = pd.DataFrame(
        {
            "metric": ["7-day lift", "1-day lift"],
            "diff": [0.82, 0.59],
            "low": [0.31, -0.06],
            "high": [1.33, 1.24],
        }
    )
    order = ["1-day lift", "7-day lift"]
    base = alt.Chart(df)
    rule = base.mark_rule(color=ORANGE, size=3).encode(
        y=alt.Y("metric:N", sort=order, axis=alt.Axis(title=None)),
        x=alt.X(
            "low:Q",
            scale=alt.Scale(domain=[-0.3, 1.6]),
            axis=alt.Axis(title="Difference (percentage points)", format=".2f", tickCount=8),
        ),
        x2="high:Q",
    )
    point = base.mark_point(filled=True, size=130, color=NAVY).encode(
        y=alt.Y("metric:N", sort=order),
        x=alt.X("diff:Q"),
        tooltip=[
            alt.Tooltip("metric:N", title="Metric"),
            alt.Tooltip("diff:Q", title="Difference", format="+.2f"),
            alt.Tooltip("low:Q", title="95% CI low", format="+.2f"),
            alt.Tooltip("high:Q", title="95% CI high", format="+.2f"),
        ],
    )
    zero = (
        alt.Chart(pd.DataFrame({"x": [0]}))
        .mark_rule(color="#98A2B3", strokeDash=[4, 4])
        .encode(x=alt.X("x:Q"))
    )
    show_chart(rule + point + zero, height=240)


CHARTS = {
    "city-listings": chart_01,
    "house-prices": chart_02,
    "air-quality": chart_03,
    "readmission": chart_04,
    "fraud": chart_05,
    "segmentation": chart_06,
    "ab-testing": chart_07,
}

SECOND_CHARTS = {
    "city-listings": chart2_01,
    "house-prices": chart2_02,
    "air-quality": chart2_03,
    "readmission": chart2_04,
    "fraud": chart2_05,
    "segmentation": chart2_06,
    "ab-testing": chart2_07,
}


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def render_home() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Portfolio · 2026</div>
          <h1>Data science, from<br>question to decision.</h1>
          <p>
            Seven end-to-end projects across EDA, regression, forecasting, classification, ensembles,
            clustering, and experimentation. Each one starts from a real question, takes a baseline
            seriously, and ends with the limitation that matters.
          </p>
          <p>
            The through-line is evaluation discipline: baseline-first comparisons, validation that
            respects the data, metrics reported in units that matter, and caveats specific to each
            dataset. The dashboard is a visual index; each notebook holds the full analysis.
          </p>
          <div class="tag-row">
            <span class="tag">EDA</span>
            <span class="tag">Regression</span>
            <span class="tag">Time series</span>
            <span class="tag">Classification</span>
            <span class="tag">Ensembles</span>
            <span class="tag">Clustering</span>
            <span class="tag">Experimentation</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.markdown("### Pick a project")
        st.caption(
            "Every page has headline metrics, two charts, what I found, and the caveat. "
            "The sidebar works too."
        )
    with right:
        st.markdown(
            f"""
            <div class="kpi">
              <div class="kpi-label">Repository</div>
              <div class="kpi-value" style="font-size:1.05rem;">7 executed notebooks</div>
              <div class="kpi-note">7 public datasets · outputs saved · no raw data committed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    columns = st.columns(2, gap="large")
    for index, project in enumerate(PROJECTS):
        with columns[index % 2]:
            with st.container(border=True):
                tags = "".join(f'<span class="tag">{tag}</span>' for tag in project["tags"])
                st.markdown(
                    f"""
                    <div class="card-kicker">{project['id']} · {project['eyebrow']}</div>
                    <div class="card-title">{project['icon']} {project['title']}</div>
                    <div class="card-result">{project['card_result']}</div>
                    <div class="card-tags">{tags}</div>
                    """,
                    unsafe_allow_html=True,
                )
                st.button(
                    "Open project  →",
                    key=f"open_{project['slug']}",
                    on_click=navigate,
                    args=(project["nav"],),
                    width="stretch",
                )

    if len(PROJECTS) % 2 == 1:
        with columns[-1]:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="card-kicker">How to read this</div>
                    <div class="card-title">Start anywhere.</div>
                    <div class="card-result">
                      Every page has headline metrics, two charts, what I found, the method, and
                      the caveat. The notebook has the full analysis and diagnostics.
                    </div>
                    <div class="card-tags">
                      <span class="tag">7 notebooks</span>
                      <span class="tag">7 datasets</span>
                      <span class="tag">Outputs saved</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("View source on GitHub", GITHUB, width="stretch")

    st.markdown(
        """
        <div class="footer">
          Metrics are transcribed from the executed notebooks in this repository. The notebooks
          contain the full method, data provenance, diagnostics, and limitations. Datasets are not
          redistributed; each project README has the download steps.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project(project: dict) -> None:
    page_header(project)
    kpi_row(project["metrics"])

    left, right = st.columns([1.45, 1], gap="large")

    with left:
        st.markdown(f'<div class="chart-title">{project["chart_title"]}</div>', unsafe_allow_html=True)
        CHARTS[project["slug"]]()
        with st.expander(project["table_title"]):
            st.dataframe(project["table"], hide_index=True, width="stretch")

    with right:
        st.markdown("#### What I found")
        st.markdown("\n".join(f"- {finding}" for finding in project["findings"]))
        st.markdown(
            f'<div class="takeaway">{project["card_result"]}</div>',
            unsafe_allow_html=True,
        )
        link_row(project)

    st.markdown(
        f'<div class="chart-title" style="margin-top:1.5rem;">Supporting view · {project["chart2_title"]}</div>',
        unsafe_allow_html=True,
    )
    SECOND_CHARTS[project["slug"]]()

    st.markdown(
        '<div class="chart-title" style="margin-top:1.3rem;">Data snapshot</div>',
        unsafe_allow_html=True,
    )
    context_row(project["context"])

    with st.expander("Method and data"):
        st.markdown(project["method"])
        st.caption(f"Caveat: {project['caveat']}")

    st.divider()

    current = PROJECTS.index(project)
    next_project = PROJECTS[(current + 1) % len(PROJECTS)]
    nav_left, nav_right = st.columns(2, gap="medium")
    nav_left.button(
        "←  Overview",
        on_click=navigate,
        args=("Overview",),
        width="stretch",
    )
    nav_right.button(
        f"Next: {next_project['title']}  →",
        on_click=navigate,
        args=(next_project["nav"],),
        width="stretch",
    )


# ---------------------------------------------------------------------------
# Sidebar + routing
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="brand-mark">RC</div>', unsafe_allow_html=True)
    st.markdown("### Raymond Cancino")
    st.caption("Data Science Portfolio")
    st.divider()
    selected = st.radio(
        "Navigate",
        NAV_OPTIONS,
        key="nav",
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("7 projects · 7 public datasets · executed notebooks")
    st.markdown(
        f"[GitHub]({GITHUB}) · [Portfolio](https://cancinoray.netlify.app/) · "
        f"[Resume](https://drive.google.com/file/d/10nixZnwbBtAYzB-wXK0ZibS3YzUrPl-D/view)"
    )

if selected == "Overview":
    render_home()
else:
    render_project(PROJECT_BY_NAV[selected])
