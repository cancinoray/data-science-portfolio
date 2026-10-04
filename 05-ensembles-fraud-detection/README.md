# 05 - Fraud Detection with Ensembles (ULB Credit Card Fraud)

[ONE-PARAGRAPH SUMMARY TODO: heavily imbalanced classification, Random Forest vs gradient boosting.]

## Dataset

- Source: Credit Card Fraud Detection (ULB, Kaggle), heavily imbalanced (https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- License: check Kaggle dataset license before committing anything; data not committed
- How to download: needs a Kaggle account, so I could not fetch this one automatically. Once logged in: `pip install kaggle`, place your API token at `~/.kaggle/kaggle.json`, then run `kaggle datasets download -d mlg-ulb/creditcardfraud -p data/` and unzip into `data/`; `data/` is git-ignored

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

- [TODO: result 1]
- [TODO: result 2]

## Skills shown

- Random Forest, gradient boosting, class imbalance
