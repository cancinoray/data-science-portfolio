# 02 - House Price Regression: OLS, Overfitting, Ridge, and Lasso

I predict Ames, Iowa house sale prices from 79 predictors and use the problem to study overfitting and
regularization. A three-feature OLS baseline reaches a holdout R² of **0.812** and an RMSE of
**$35,978**. Adding engineered features and one-hot encoding lifts that to **R² 0.913 / RMSE $22,788
/ MAE $15,195**. Cross-validated Ridge and Lasso **do not beat OLS on this particular 292-house
holdout** (R² 0.901 and 0.899), but they cut 5-fold CV log-RMSE from **0.163 to 0.140 / 0.138**,
shrink unstable coefficients, and let Lasso keep only **80 of 297** encoded features. The honest
lesson: with 1,460 rows and a strong signal, regularization buys stability and simplicity more than
raw accuracy.

## Dataset

- Source: Ames Housing, Kaggle
  [House Prices — Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)
- Mirror: OpenML dataset `42165` (`house_prices`), which is how I fetched it
- Size: 1,460 rows × 81 columns (79 predictors + `Id` + `SalePrice`)
- Licence: check the Kaggle competition rules and the Ames data documentation. The CSV is **not
  committed**; `data/` is git-ignored.
- How to download:

```bash
# Option A: OpenML (no Kaggle account)
python - <<'PY'
from sklearn.datasets import fetch_openml
d = fetch_openml(data_id=42165, as_frame=True, parser="auto", data_home=".cache/openml")
d.frame.to_csv("data/ames.csv", index=False)
PY

# Option B: Kaggle CLI (needs an account with the competition rules accepted)
kaggle competitions download -c house-prices-advanced-regression-techniques -p data/
unzip data/house-prices-advanced-regression-techniques.zip -d data/
```

The notebook expects `data/ames.csv`.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

| Model | Train R² | Holdout R² | Holdout RMSE | Holdout MAE | Median APE |
|---|---|---|---|---|---|
| Baseline (3 features) | 0.77 | 0.81 | $35,978 | $23,609 | 10.1% |
| Full OLS (engineered + one-hot) | 0.94 | **0.91** | **$22,788** | **$15,195** | **5.7%** |
| Ridge (CV alpha = 30) | 0.91 | 0.90 | $25,704 | $16,254 | 6.5% |
| Lasso (CV alpha = 0.001) | 0.91 | 0.90 | $25,521 | $16,211 | 6.8% |

- **Overfitting is visible in the train/holdout gap:** full OLS fits 0.945 on training but 0.913 on
  the holdout. A controlled polynomial demo (200 training houses, degree 1→10) shows training RMSE
  staying flat around $50k while holdout RMSE rises from $58k to $188k.
- **Cross-validation prefers the regularized models:** CV log-RMSE is 0.163 for OLS, 0.140 for Ridge,
  and 0.138 for Lasso. The single holdout disagrees, which is a useful lesson about the variance of a
  292-row test set. I trust CV for selection and report both.
- **Lasso selects a smaller model:** 80 of 297 encoded features survive at alpha = 0.001. The kept
  features are plausible: living area, overall quality, pool/garage variables, and a handful of
  neighbourhood dummies.
- **Engineering matters:** `TotalSF`, `TotalBath`, `HouseAge`, `RemodAge`, `TotalPorch`, `HasPool`,
  and `HasGarage`, plus ordinal encoding of quality ratings, take the holdout R² from 0.812 to 0.913.

## What the notebook covers

- The right-skewed target and why `log1p(SalePrice)` is used.
- Missing values that mean "this feature does not exist" (pool, alley, garage) vs genuine gaps
  (`LotFrontage`).
- Ordinal quality mapping, absence-missing numeric fixes, engineered features, and pseudo-numeric
  categoricals.
- A controlled overfitting demonstration with polynomial degrees.
- Ridge coefficient paths and Lasso feature selection.
- Cross-validated alpha selection (`GridSearchCV`), holdout evaluation, and a candid discussion of
  CV-vs-holdout disagreement.
- Residual diagnostics, dollar-error interpretation, and back-transform bias.
- Limitations: small single-market sample, linearity, outliers, no spatial coordinates, no time split.

## Skills shown

- Linear regression, feature engineering, one-hot and ordinal encoding
- Overfitting diagnostics and train/test discipline
- Ridge and Lasso regularization, alpha tuning, coefficient paths
- Cross-validation, model comparison, error metrics in dollars
- Explaining a model's limitations honestly
