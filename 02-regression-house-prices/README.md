# 02 - House Price Regression (Ames Housing)

[ONE-PARAGRAPH SUMMARY TODO: predict sale price, compare linear regression baseline vs Ridge/Lasso, discuss overfitting.]

## Dataset

- Source: Ames Housing, Kaggle "House Prices - Advanced Regression Techniques" (https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques); needs a Kaggle account and accepting the competition rules
- License: check competition rules on Kaggle before committing anything; data not committed
- How to download: needs a Kaggle account with the competition rules accepted, so I could not fetch this one automatically. Once logged in: `pip install kaggle`, place your API token at `~/.kaggle/kaggle.json`, join the competition on its page above, then run `kaggle competitions download -c house-prices-advanced-regression-techniques -p data/` and unzip into `data/`; `data/` is git-ignored

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

- [TODO: result 1]
- [TODO: result 2]

## Skills shown

- linear regression, overfitting, Ridge and Lasso
