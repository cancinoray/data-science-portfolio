# 05 - Fraud Detection with Ensembles: Learning from 0.17% Positives

The ULB credit-card dataset has **284,807 transactions and only 492 frauds (0.173%)**. Using a
chronological 70/15/15 split, a balanced logistic regression gets a **PR-AUC of 0.723** but a
**ROC-AUC of 0.977**; a Random Forest gets **PR-AUC 0.782** but a **lower ROC-AUC of 0.935**. That
inversion is the point of the project: with extreme imbalance, ROC looks reassuring while
precision-recall tells you what actually happens to alerts. At a 0.5 threshold the Random Forest
catches **69% of frauds with 97% precision** (36 of 52 frauds, 1 false alarm). Lowering the threshold
to the cost-optimal point raises recall to **77%** at 48% precision, which is better if a missed
fraud costs far more than a manual review.

## Dataset

- Source: *Credit Card Fraud Detection*, ULB Machine Learning Group
  ([Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud))
- Size: 284,807 transactions × 31 columns; 492 frauds (0.173%); 1,081 exact duplicates
- Columns: `Time`, `V1`–`V28` (anonymised PCA components), `Amount`, `Class`
- Licence: check the Kaggle/ULB terms. The CSV is **not committed**; `data/` is git-ignored.
- How to download:

```bash
# Kaggle CLI
kaggle datasets download -d mlg-ulb/creditcardfraud -p data/
unzip data/creditcardfraud.zip -d data/

# Mirror used in this project (same 31 columns, includes Time)
curl -L "https://raw.githubusercontent.com/nsethi31/Kaggle-Data-Credit-Card-Fraud-Detection/master/creditcard.csv" \
  -o data/creditcard.csv
```

The notebook expects `data/creditcard.csv`.

Notes:

- The dataset covers about 48 hours and has no missing values.
- `V1`–`V28` are PCA components; the original business features are not available. That limits
  interpretability.
- I drop exact duplicates before splitting (283,726 rows remain) so the same transaction cannot appear
  in both train and test.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

Chronological split: train = first 70% (198,608 rows, 366 frauds), validation = next 15% (42,559,
55 frauds), test = last 15% (42,559, 52 frauds). Models are fit on train; thresholds are chosen on
validation; test is touched once.

| Model | PR-AUC | ROC-AUC | Precision @0.5 | Recall @0.5 |
|---|---|---|---|---|
| Logistic (balanced) | 0.723 | **0.977** | 0.021 | 0.885 |
| Random Forest | **0.782** | 0.935 | **0.973** | 0.692 |
| Hist. gradient boosting | 0.725 | 0.926 | 0.312 | 0.769 |

- **ROC vs PR:** logistic regression wins ROC-AUC but flags 2,095 false positives to catch 46 frauds;
  Random Forest wins PR-AUC and flags 1 false positive to catch 36. PR-AUC is the metric that matches
  the review team's experience.
- **Cost-sensitive threshold:** with an illustrative missed-fraud cost of $150 and a false-alarm cost
  of $5, the validation-optimal threshold is **0.055**. On test it flags 84 transactions (40 TP,
  44 FP, 12 FN): precision **47.6%**, recall **76.9%**, expected cost **$0.047 per transaction** vs
  **$0.057** at 0.5.
- **Class weighting ablation:** RF without weights has PR-AUC 0.743 and ROC-AUC 0.951; with
  `balanced_subsample` it has PR-AUC 0.782 and ROC-AUC 0.935. Better PR, worse ROC — the same
  trade-off.
- **Top features:** `V14`, `V12`, `V10`, `V4`, `V17`. They are anonymised, so the model can rank but
  cannot explain a fraud in business terms.

## What the notebook covers

- The 578:1 imbalance and why an all-negative classifier is 99.83% accurate and useless.
- Deduplication, hour-of-day sin/cos encoding, `log1p(Amount)`, and dropping raw `Time`.
- Why a chronological split is the right evaluation for fraud.
- Class weighting vs resampling; why I chose weights.
- Logistic regression, Random Forest, and histogram gradient boosting.
- PR-AUC vs ROC-AUC, precision/recall curves, confusion matrices.
- Threshold selection with an explicit cost model.
- Feature importance and its interpretability limits.
- Limitations: two days of data, anonymised features, drift, label noise, calibration, single model.

## Skills shown

- Imbalanced classification and class weighting
- Random Forest and histogram gradient boosting
- PR-AUC / average precision vs ROC-AUC
- Temporal validation and threshold selection
- Cost-sensitive decision analysis
- Explaining a high-stakes model's limits
