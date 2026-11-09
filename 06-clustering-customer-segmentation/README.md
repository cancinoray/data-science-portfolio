# 06 - Customer Segmentation: RFM, K-Means, and Naming the Segments

I turn 392,692 cleaned transactions from a UK online retailer into **4,338 customer RFM profiles**
(Recency, Frequency, Monetary). A K-Means baseline on raw, standardised RFM gets a silhouette of
**0.617** — but it does so by isolating **6 and 8 customers** into their own clusters, which is
outlier detection, not segmentation. Log-transforming the heavily skewed RFM values and re-running
K-Means with **k = 5** gives a lower silhouette (**0.316**) but five usable segments:
**Champions** (7.8% of customers, **52.9% of revenue**), **Loyal** (21.6%, 23.0%), **At risk**
(23.5%, 16.6%), **New / promising** (19.2%, 3.7%), and **Hibernating** (27.9%, 3.8%). The lesson:
silhouette measures separation, not usefulness; a segmentation has to be interpretable to be worth
acting on.

## Dataset

- Source: UCI Machine Learning Repository, *Online Retail*
  ([dataset page](https://archive.ics.uci.edu/dataset/352/online+retail))
- File: `Online Retail.xlsx`, 541,909 line items × 8 columns
- Period: 2010-12-01 to 2011-12-09, UK-based online retailer
- Licence: check the UCI dataset page. The workbook is **not committed**; `data/` is git-ignored.
- How to download:

```bash
mkdir -p data
curl -L "https://archive.ics.uci.edu/static/public/352/online+retail.zip" -o data/online_retail.zip
unzip data/online_retail.zip -d data/
# rename if needed so the notebook finds data/Online Retail.xlsx
```

Reading the Excel file needs `openpyxl` (in `requirements.txt`).

Notes:

- 135,080 rows (25%) have no `CustomerID` and are excluded; they are guest checkouts and cannot be
  attributed to a customer.
- 10,624 rows have negative `Quantity` (returns/cancellations) and are removed, so `Monetary` is gross
  spend, not net of returns.
- 2,517 rows have zero/negative price; 5,268 exact duplicates. After cleaning: **392,692 line items**
  and **4,338 customers**.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

Clean table: 4,338 customers. Snapshot date: 2011-12-10.

| Segment | Customers | Share | Avg recency | Avg frequency | Avg monetary | Revenue share |
|---|---|---|---|---|---|---|
| Champions | 339 | 7.8% | 12.2 days | 20.7 | £13,877 | **52.9%** |
| Loyal | 938 | 21.6% | 18.5 days | 5.8 | £2,179 | 23.0% |
| At risk | 1,018 | 23.5% | 103.7 days | 3.1 | £1,452 | 16.6% |
| New / promising | 834 | 19.2% | 27.0 days | 1.6 | £390 | 3.7% |
| Hibernating | 1,209 | 27.9% | 208.4 days | 1.2 | £277 | 3.8% |

- **Raw RFM baseline:** silhouette **0.617** with k = 5, but cluster sizes `[3048, 1063, 8, 213, 6]`.
  Two clusters are extreme monetary outliers; the high silhouette is an artefact of separating them.
- **Log-transformed RFM:** silhouette 0.433 at k = 2, 0.337 at k = 3, 0.338 at k = 4, **0.316 at
  k = 5**, 0.303 at k = 8. I choose k = 5 for business interpretability: k = 2 is too coarse and k = 4
  merges the At-risk and Loyal groups.
- **Revenue concentration:** the top 7.8% of customers generate 52.9% of revenue; the largest segment
  (Hibernating, 27.9%) generates only 3.8%.
- **Stability:** adjusted Rand index across K-Means seeds averages **0.918**, so the partition is
  stable but not identical — boundary customers move.
- **Silhouette by segment:** Hibernating is the most compact (0.43); the other four sit in a narrow
  0.26–0.29 band, which matches the overlap visible in the recency-vs-monetary scatter.

## What the notebook covers

- RFM construction and the snapshot-date choice.
- Cleaning decisions and their costs: guest customers, returns, zero prices, duplicates.
- Heavy-tailed distributions and why raw K-Means fails.
- Elbow and silhouette plots, and the k = 2 vs k = 5 trade-off.
- Segment profiling, naming by average monetary value, and revenue-share analysis.
- A z-score heatmap and a two-dimensional recency/monetary scatter.
- Silhouette by segment and a stability check across seeds.
- Plain-language segment actions: retain Champions, grow Loyal, win back At risk, convert New,
  suppress or cheaply reactivate Hibernating.
- Limitations: guest customers excluded, gross spend, one year, no margin, hard assignments, and the
  subjectivity of k and names.

## Skills shown

- RFM feature engineering
- K-Means, log transformation, standardisation
- Elbow and silhouette analysis, choosing k with judgement
- Cluster profiling and segment naming
- Revenue concentration and business interpretation
- Communicating an unsupervised result without overclaiming
