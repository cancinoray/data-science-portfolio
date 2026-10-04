# 03 - Air Quality Time Series (OpenAQ)

[ONE-PARAGRAPH SUMMARY TODO: hourly data for one location, lag features, AR vs ARMA forecast.]

## Dataset

- Source: OpenAQ air quality API, one location, hourly data (https://docs.openaq.org/about/about) [DATASET LINK: add location ID / query I used]
- License: check OpenAQ's terms before committing anything; data not committed
- How to download: OpenAQ's v3 API requires a free API key (register at https://explore.openaq.org, then generate a key under your account) sent as the `X-API-Key` header. I could not fetch this one automatically without a key. Once you have one: pick a `location_id` from `GET /v3/locations`, then pull hourly measurements from `GET /v3/locations/{id}/measurements` and save the result into `data/`; `data/` is git-ignored

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

- [TODO: result 1]
- [TODO: result 2]

## Skills shown

- lag features, AR and ARMA forecasting
