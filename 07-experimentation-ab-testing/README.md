# 07 - A/B Testing: Cookie Cats Retention Experiment

[ONE-PARAGRAPH SUMMARY TODO: retention experiment, chi-square test, ETL into SQLite, small Streamlit dashboard.]

## Dataset

- Source: Cookie Cats mobile game A/B test (retention experiment) (https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing)
- License: check Kaggle dataset license before committing anything; data not committed
- How to download: needs a Kaggle account, so I could not fetch this one automatically. Once logged in: `pip install kaggle`, place your API token at `~/.kaggle/kaggle.json`, then run `kaggle datasets download -d yufengsui/mobile-games-ab-testing -p data/` and unzip into `data/`; `data/` is git-ignored

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
# TODO: streamlit app entry point (e.g. streamlit run app.py), to be added with analysis
```

## Key results

- [TODO: result 1]
- [TODO: result 2]

## Skills shown

- hypothesis testing (chi-square), ETL into SQLite, small Streamlit dashboard
