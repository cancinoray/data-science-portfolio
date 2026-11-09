# 07 - A/B Testing: Does Moving the Cookie Cats Gate from 30 to 40 Hurt Retention?

90,189 players were randomised to hit the first gate at level 30 or level 40. **7-day retention is
19.02% at gate 30 vs 18.20% at gate 40** — a difference of **0.82 percentage points** (relative lift
4.5%, 95% CI 0.31–1.33 pp, chi-square p = 0.0016). **1-day retention is 44.82% vs 44.23%** (0.59 pp,
p = 0.074), not significant. The effect is small but it points the same way in both metrics, survives
a Bonferroni correction for two tests, and is robust to removing an extreme whale. The decision:
**keep the gate at level 30**; moving it to 40 costs early retention with no evidence of a
compensating benefit.

## Dataset

- Source: *Mobile Games A/B Testing — Cookie Cats* on Kaggle
  ([dataset page](https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing))
- Size: 90,189 players × 5 columns (`userid`, `version`, `sum_gamerounds`, `retention_1`,
  `retention_7`)
- Arms: `gate_30` (44,700 players) and `gate_40` (45,489 players)
- Licence: check the Kaggle dataset page. The CSV is **not committed**; `data/` is git-ignored.
- How to download:

```bash
# Kaggle CLI
kaggle datasets download -d yufengsui/mobile-games-ab-testing -p data/
unzip data/mobile-games-ab-testing.zip -d data/

# Mirror used in this project
curl -L "https://raw.githubusercontent.com/yfsui/Mobile-Games-AB-Testing-Project/HEAD/cookie_cats.csv" \
  -o data/cookie_cats.csv
```

The notebook expects `data/cookie_cats.csv`; it also builds `data/cookie_cats.db` for the dashboard.

Notes:

- One row is one player; the randomisation unit is the player.
- There are no dates, acquisition channels, devices, countries, or revenue in the extract.
- `sum_gamerounds` is a **post-treatment** variable. It is used descriptively and for sensitivity, not
  as a covariate in the retention comparison.
- One player has 49,854 rounds (far above the 99.9th percentile); removing them does not change the
  conclusion.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb      # analysis + SQLite ETL
streamlit run app.py                 # dashboard
```

## Key results

| Metric | gate_30 | gate_40 | Difference | 95% CI | p-value |
|---|---|---|---|---|---|
| 1-day retention | 44.82% | 44.23% | +0.59 pp | −0.06 to +1.24 pp | 0.074 |
| 7-day retention | **19.02%** | **18.20%** | **+0.82 pp** | **+0.31 to +1.33 pp** | **0.0016** |

- **7-day retention is significantly better at gate 30.** The effect survives Bonferroni correction
  for two metrics (α = 0.025) and Benjamini–Hochberg FDR control.
- **1-day retention is directionally the same but not significant.** The confidence interval includes
  zero.
- **Sample ratio mismatch:** 44,700 vs 45,489, expected 45,094.5 each; chi-square p = 0.0086. The
  imbalance is 1.75% relative and does not explain the retention difference, but it is flagged.
- **Power:** with ~45k players per arm, the minimum detectable effect at 80% power is **0.73 pp**.
  The observed 0.82 pp is just above it, so the estimate is imprecise.
- **Sensitivity:** excluding the extreme player or all players above 2,000 rounds leaves the 7-day
  result at p ≈ 0.0016 and the rates essentially unchanged.
- **Practical impact:** 0.82 pp corresponds to about **8,200 additional 7-day retained players per
  1 million** exposed, at gate 30. The 4.5% relative lift is meaningful; the absolute effect is small.
- **Decision:** keep the gate at level 30. Moving it to 40 costs 7-day retention with no metric on
  which it is better.

## Dashboard

`app.py` is a Streamlit dashboard that reads the SQLite table built by the notebook:

- player counts, retention rates, and the chi-square result;
- a 1-day / 7-day metric switch;
- Wilson confidence intervals and a retention bar chart;
- the distribution of rounds played by arm;
- method notes, including the SRM and the multiple-testing correction.

The app falls back to the raw CSV if the database has not been built. It is a communication tool;
the notebook is the source of truth for the method and caveats.

## What the notebook covers

- Data sanity checks: duplicates, missing values, arm sizes, and sample ratio mismatch.
- Hypotheses, two-sided chi-square tests, and the meaning of a p-value.
- Effect sizes, relative lift, and confidence intervals for the difference.
- Power, minimum detectable effect, and the distinction between statistical and practical
  significance.
- Multiple-testing corrections (Bonferroni and BH).
- Outlier sensitivity and why `sum_gamerounds` is not a covariate.
- SQLite ETL with indexed queries for the dashboard.
- Limitations: one game, short windows, no revenue, SRM, no pre-registration, no subgroups.

## Skills shown

- Experiment design and sanity checks (SRM, randomisation unit)
- Chi-square testing, confidence intervals, effect sizes
- Power analysis and minimum detectable effect
- Multiple-testing correction
- Sensitivity analysis and practical significance
- SQLite ETL and a Streamlit dashboard
