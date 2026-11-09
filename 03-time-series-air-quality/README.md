# 03 - Air Quality Time Series: Forecasting NYC PM2.5

I use two years of hourly PM2.5 data for New York City (17,544 hours, no missing values) and
forecast the daily average for the last 90 days. A **static seasonal naive** baseline — repeat the
last training week for the whole horizon — gets an RMSE of **7.08 µg/m³**. A SARIMA model on log
PM2.5 improves that to **6.79**, and a Ridge model with lag features and calendar terms does best at
**6.45**. For **one-day-ahead** forecasting, Ridge gets RMSE **5.42** vs 5.96 for SARIMA, 6.18 for a
random walk, and 7.76 for a one-step seasonal naive. Forecast skill is horizon-dependent: the models
have real information about tomorrow, much less about next month, and at 90 days they are only
modestly better than a seasonal baseline.

## Dataset

- Source: [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api), a free API
  that serves reanalysis and forecast fields without a key
- Location: New York City (40.7128, −74.0060), timezone `America/New_York`
- Period: 2023-01-01 to 2024-12-31, hourly
- File: `nyc_air_quality_hourly.csv`, 17,544 rows × 3 columns (`time`, `pm2_5`, `pm10`)
- Licence / terms: check [Open-Meteo's terms](https://open-meteo.com/en/terms). The CSV is **not
  committed**; `data/` is git-ignored.
- How to download:

```bash
mkdir -p data
python - <<'PY'
import json, urllib.request
import pandas as pd

url = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    "?latitude=40.7128&longitude=-74.0060"
    "&hourly=pm2_5,pm10&start_date=2023-01-01&end_date=2024-12-31"
    "&timezone=America%2FNew_York"
)
with urllib.request.urlopen(url) as r:
    payload = json.load(r)
pd.DataFrame(payload["hourly"]).to_csv("data/nyc_air_quality_hourly.csv", index=False)
PY
```

Notes:

- These are modelled/reanalysis values on a grid, not a single regulatory monitor. They smooth over
  street-level variation.
- The series contains two unusual episodes: the June 2023 Canadian wildfire smoke and a late-December
  2024 pollution event. Both are real and both matter for evaluation.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

I evaluate in two regimes because they answer different questions. **One-step** uses the actual
previous value(s) at each test day; **static 90-day** freezes the forecast at the end of training.

| Model | One-step RMSE | One-step MAE | Static 90-day RMSE | Static 90-day MAE |
|---|---|---|---|---|
| Random walk | 6.18 | 4.39 | 7.31 | 4.60 |
| Seasonal naive | 7.76 | 5.29 | 7.08 | 4.97 |
| SARIMA(2,0,1)(0,0,1,7) on log PM2.5 | 5.96 | 3.90 | 6.79 | 4.65 |
| Ridge lag features | **5.42** | **3.67** | **6.45** | **4.45** |

- **Ridge wins both regimes:** 5.42 one-step, 6.45 static 90-day. The margin is much larger at one
  step (30% vs the seasonal naive one-step) than at 90 days (9% vs the static seasonal naive).
- **The static seasonal naive is a strong long-horizon baseline** (7.08), because it preserves the
  weekly pattern. The one-step seasonal naive is worse (7.76) because the weekly cycle is weak; the
  recent level dominates at short range.
- **Horizon skill is not monotonic.** Cumulative RMSE at h = 1 is best for Ridge (1.95 vs 2.50 for
  seasonal naive and 2.27 for SARIMA). At h = 7 the seasonal naive dips to 1.59 because that
  particular week was stable; by h = 30 Ridge is lowest, and at h = 90 it is 6.45 vs 6.79 and 7.08.
- **The December spike is missed by every model.** An extreme pollution episode driven by weather and
  wildfire smoke is not predictable from PM2.5 history alone.
- **Diagnostics:** ADF p ≈ 0.002 on the levels (no differencing needed); ACF decays slowly with a small
  weekly bump; residual ACF is much smaller than the raw series but not zero.

## What the notebook covers

- Hourly vs daily aggregation and the trade-off (diurnal cycle vs noise).
- Annual, weekly, and diurnal seasonality; wildfire and winter episodes.
- Stationarity (ADF), ACF/PACF, and what they imply for AR/MA orders.
- Chronological train/test split and why shuffling is wrong.
- Two evaluation regimes: one-step rolling and static 90-day forecasts.
- Seasonal naive and random-walk baselines in both regimes.
- SARIMA on log PM2.5, with an explanation of AR, MA, ARIMA, and SARIMA terms, plus a walk-forward
  one-step evaluation.
- Lag features, rolling means, Fourier calendar terms, and a recursive 90-day Ridge forecast.
- Horizon-by-horizon error, residual diagnostics, and a plain-language interpretation.
- Limitations: one city, two years, no weather inputs, modelled data, point forecasts only.

## Skills shown

- Time-series EDA, stationarity testing, ACF/PACF interpretation
- Lag features and recursive forecasting
- SARIMA with statsmodels, including walk-forward refitting
- Chronological evaluation, RMSE/MAE, baseline discipline across forecast regimes
- Explaining forecast skill and its limits
