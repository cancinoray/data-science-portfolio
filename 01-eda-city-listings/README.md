# 01 - City Listings EDA: Does Size or Location Drive Price?

[ONE-PARAGRAPH SUMMARY TODO: I explore Inside Airbnb listings for New York City to ask whether size or location explains nightly price.]

## Dataset

- City: New York City
- Source: Inside Airbnb (https://insideairbnb.com/get-the-data/), snapshot `2026-06-14`: https://data.insideairbnb.com/united-states/ny/new-york-city/2026-06-14/data/listings.csv.gz
- License: check terms at https://insideairbnb.com/data-policies/ before committing anything; data not committed
- How to download: already downloaded to `data/listings.csv.gz` (54,270 listings, gzip-compressed CSV; `pandas.read_csv("data/listings.csv.gz")` reads it directly). To refresh or switch cities, grab a new file from the link above and overwrite it; `data/` is git-ignored

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

- [TODO: result 1]
- [TODO: result 2]

## Skills shown

- wrangling, EDA, correlation: does size or location drive price?
