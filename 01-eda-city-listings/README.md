# 01 - City Listings EDA: Does Size or Location Drive Price?

I explore 30,259 New York City Airbnb listings to ask whether nightly price is driven more by the
size of the listing or by where it is. After dropping listings without a visible price and filtering
to short-stay, mid-market listings, I compare size-only, location-only, and combined linear models
on log price. **Both matter, and they are complementary:** size alone reaches a 5-fold CV R² of
0.234, location alone 0.265, and the two together 0.469. Adding location to a size + room-type model
lifts R² by **+0.175**; adding size to a location + room-type model lifts it by **+0.115**. In plain
terms: size sets the baseline price, location sets the multiplier.

## Dataset

- City: New York City
- Source: Inside Airbnb, snapshot `2026-06-14`
  ([data page](https://insideairbnb.com/get-the-data/))
- File: `listings.csv.gz`, 30,259 rows × 90 columns
- Licence: Inside Airbnb's [data policies](https://insideairbnb.com/data-policies/) apply. The data
  is **not committed**; `data/` is git-ignored.
- How to download:

```bash
mkdir -p data
curl -L "https://data.insideairbnb.com/united-states/ny/new-york-city/2026-06-14/data/listings.csv.gz" \
  -o data/listings.csv.gz
```

Notes on the data:

- 28.9% of listings have no `price` (8,744 rows). Missingness varies by borough and room type, so the
  cleaned sample is not a random sample of the marketplace.
- `bedrooms`, `beds`, and `bathrooms` are missing for about a third of listings; the model imputes
  them inside the pipeline.
- `minimum_nights` has a median of 30 days, so I keep only listings with a minimum stay of 30 nights
  or less to focus on short-stay pricing.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

- Cleaned sample: **20,320 listings**; median nightly price **$171.83**, mean **$225.38**.
- Median price by borough: Manhattan **$234.78**, Brooklyn **$151.50**, Queens **$120.15**, Staten
  Island **$107.78**, Bronx **$106.57**.
- Median price by room type: entire home/apt **$221.27**, private room **$102.05**, shared room
  **$52.21**, hotel room **$399.00**.
- Model comparison (5-fold CV R² on log price):

  | Model | CV R² | Holdout R² | MAE |
  |---|---|---|---|
  | Median baseline | 0.000 | 0.000 | $126 |
  | Size only | 0.234 | 0.239 | $114 |
  | Location only | 0.265 | 0.252 | $108 |
  | Size + location | 0.469 | 0.468 | $94 |
  | Full (+ room type) | **0.495** | **0.498** | **$92** |

- Incremental value: adding location to size + room type gives **+0.175 R²**; adding size to location
  + room type gives **+0.115 R²**.
- The full model's median absolute percentage error is **36.6%**; only **34.4%** of predictions land
  within 25% of the actual price. It is a driver-analysis model, not a pricing oracle.
- One extra guest is associated with roughly a **11.9%** higher nightly price in the full model,
  holding the other features fixed; one extra bedroom with about **8.0%**. These are model weights,
  not causal effects, because the size variables are correlated.

## What the notebook covers

- Data provenance, licence, and the 29% missing-price problem.
- Cleaning as a sequence of explicit decisions, with the cost of each filter.
- Price distributions and the log transform.
- Price by borough and room type; size vs price; a spatial price map; neighbourhood rankings.
- Correlation matrix and multicollinearity caveats.
- Baseline → size-only → location-only → combined models, with 5-fold CV and a holdout.
- Coefficient interpretation, residual diagnostics, and error by borough.
- Limitations (asking price vs transaction price, selection bias, omitted amenities, one snapshot).

## Skills shown

- Data wrangling and missing-data judgement
- Exploratory data analysis and visualisation
- Correlation vs causation, confounding, multicollinearity
- Linear regression on a log target, one-hot encoding, cross-validation
- Communicating model results in dollars and in plain language
