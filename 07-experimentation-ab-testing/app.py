"""Cookie Cats A/B test dashboard.

A small Streamlit app that reads the cleaned experiment table from SQLite
(`data/cookie_cats.db`) and shows retention by arm, a chi-square test, and the
distribution of rounds played. Falls back to the raw CSV if the database has
not been built yet.

Run from this folder:
    streamlit run app.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportion_confint

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "cookie_cats.db"
CSV_PATH = DATA_DIR / "cookie_cats.csv"

NAVY, ORANGE, TEAL, GRAY = "#12355B", "#E07A5F", "#1B998B", "#6B7280"
ARM_COLORS = {"gate_30": NAVY, "gate_40": ORANGE}

st.set_page_config(
    page_title="Cookie Cats A/B Test",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_experiment() -> pd.DataFrame:
    """Load the experiment from SQLite, falling back to the raw CSV."""
    if DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query("SELECT * FROM experiment", conn)

    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)
        df["retention_1"] = df["retention_1"].astype(int)
        df["retention_7"] = df["retention_7"].astype(int)
        return df[["userid", "version", "sum_gamerounds", "retention_1", "retention_7"]]

    st.error(
        "No experiment data found. Add `data/cookie_cats.csv` (or build "
        "`data/cookie_cats.db` by running the notebook) and reload."
    )
    st.stop()


def wilson_interval(successes: int, n: int) -> tuple[float, float]:
    low, high = proportion_confint(successes, n, method="wilson")
    return float(low), float(high)


def arm_stats(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    rows = []
    for arm in ["gate_30", "gate_40"]:
        subset = df.loc[df["version"] == arm, metric]
        if subset.empty:
            continue
        n = len(subset)
        successes = int(subset.sum())
        rate = successes / n
        low, high = wilson_interval(successes, n)
        rows.append(
            {
                "arm": arm,
                "players": n,
                "retained": successes,
                "rate": rate,
                "ci_low": low,
                "ci_high": high,
            }
        )
    return pd.DataFrame(rows)


def difference_test(df: pd.DataFrame, metric: str) -> dict:
    table = pd.crosstab(df["version"], df[metric])
    chi2, p_value, dof, expected = chi2_contingency(table, correction=False)
    rates = df.groupby("version")[metric].mean()
    diff = float(rates.get("gate_30", np.nan) - rates.get("gate_40", np.nan))
    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "dof": int(dof),
        "min_expected": float(expected.min()),
        "difference": diff,
        "relative_lift": diff / float(rates.get("gate_40", np.nan)),
    }


df = load_experiment()

st.title("🐱 Cookie Cats: gate placement A/B test")
st.caption(
    "Does moving the first gate from level 30 to level 40 change player retention? "
    "90,189 players, two arms, one experiment."
)

with st.sidebar:
    st.header("Controls")
    selected_arms = st.multiselect(
        "Arms to show",
        options=["gate_30", "gate_40"],
        default=["gate_30", "gate_40"],
        help="gate_30 is the control; gate_40 is the treatment.",
    )
    metric_label = st.radio(
        "Retention metric",
        options=["7-day retention", "1-day retention"],
        index=0,
    )
    metric = "retention_7" if metric_label.startswith("7") else "retention_1"

    st.divider()
    st.caption(
        "This dashboard is descriptive. The notebook contains the full method, "
        "power analysis, multiple-testing correction, and limitations."
    )

if not selected_arms:
    st.warning("Select at least one arm to see results.")
    st.stop()

filtered = df[df["version"].isin(selected_arms)].copy()
stats = arm_stats(filtered, metric)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
top = st.columns(4)

gate_30 = stats.loc[stats["arm"] == "gate_30"]
gate_40 = stats.loc[stats["arm"] == "gate_40"]

if not gate_30.empty:
    top[1].metric("gate_30 retention", f"{gate_30['rate'].iloc[0]:.2%}",
                  help=f"{int(gate_30['retained'].iloc[0]):,} of {int(gate_30['players'].iloc[0]):,} players")
if not gate_40.empty:
    top[2].metric("gate_40 retention", f"{gate_40['rate'].iloc[0]:.2%}",
                  help=f"{int(gate_40['retained'].iloc[0]):,} of {int(gate_40['players'].iloc[0]):,} players")

top[0].metric("Players shown", f"{len(filtered):,}")

if len(stats) == 2:
    test = difference_test(filtered, metric)
    lift_pp = test["difference"] * 100
    top[3].metric(
        "gate_30 − gate_40",
        f"{lift_pp:+.2f} pp",
        delta=f"p = {test['p_value']:.4f}",
        delta_color="off",
        help="Positive means gate_30 has higher retention. Two-sided chi-square test.",
    )
else:
    test = None
    top[3].metric("Difference", "—", help="Select both arms to run the test.")

st.divider()

# ---------------------------------------------------------------------------
# Retention chart
# ---------------------------------------------------------------------------
left, right = st.columns([1.15, 1])

with left:
    st.subheader(f"{metric_label} by arm")
    fig, ax = plt.subplots(figsize=(7, 4.4))
    for i, row in stats.iterrows():
        color = ARM_COLORS.get(row["arm"], GRAY)
        error = np.array([[(row["rate"] - row["ci_low"]) * 100,
                           (row["ci_high"] - row["rate"]) * 100]]).T
        ax.bar(row["arm"], row["rate"] * 100, color=color, alpha=0.9,
               yerr=error, capsize=5)
        ax.text(row["arm"], row["rate"] * 100 + 1.2, f"{row['rate']:.2%}",
                ha="center", fontsize=10)
    ax.set_ylabel("Retention (%)")
    ax.set_ylim(0, max(55, stats["ci_high"].max() * 100 + 8))
    ax.set_title("Point estimate with 95% Wilson interval")
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    st.pyplot(fig)

with right:
    st.subheader("The test")
    if test is not None:
        st.write(
            f"Difference: **{test['difference'] * 100:+.2f} percentage points** "
            f"({test['relative_lift']:+.1%} relative to gate_40)."
        )
        st.write(
            f"Chi-square = **{test['chi2']:.2f}**, df = {test['dof']}, "
            f"p = **{test['p_value']:.4f}**."
        )
        if test["p_value"] < 0.05:
            st.success("Statistically significant at α = 0.05 (two-sided).")
        else:
            st.info("Not statistically significant at α = 0.05 (two-sided).")
        st.caption(
            "With two primary metrics, the notebook applies a Bonferroni correction "
            "(α = 0.025). The 7-day result survives; the 1-day result does not."
        )
    else:
        st.info("Select both arms to run the difference test.")

    st.subheader("Counts")
    display = stats.copy()
    display["rate"] = display["rate"].map(lambda x: f"{x:.2%}")
    display["95% CI"] = display.apply(
        lambda row: f"{row['ci_low']:.2%} – {row['ci_high']:.2%}", axis=1
    )
    st.dataframe(
        display[["arm", "players", "retained", "rate", "95% CI"]],
        hide_index=True,
        width="stretch",
    )

st.divider()

# ---------------------------------------------------------------------------
# Engagement distribution
# ---------------------------------------------------------------------------
st.subheader("Rounds played in the first 14 days")
st.caption(
    "Descriptive only: `sum_gamerounds` is measured after the gate, so it is a "
    "post-treatment variable. Do not adjust the retention comparison for it."
)

fig, ax = plt.subplots(figsize=(10, 4.2))
bins = np.logspace(0, np.log10(df["sum_gamerounds"].max() + 2), 45)
for arm in selected_arms:
    values = df.loc[df["version"] == arm, "sum_gamerounds"] + 1
    ax.hist(values, bins=bins, alpha=0.55, density=True,
            color=ARM_COLORS.get(arm, GRAY), label=arm)
ax.set_xscale("log")
ax.set_xlabel("Rounds played + 1 (log scale)")
ax.set_ylabel("Density")
ax.set_title("Most players play fewer than 100 rounds")
ax.legend(frameon=False)
fig.tight_layout()
st.pyplot(fig)

with st.expander("Method notes and caveats"):
    st.markdown(
        """
        - **Unit of randomisation:** the player (`userid`). One row per player.
        - **Metrics:** `retention_1` and `retention_7` are binary; rates are means.
        - **Test:** two-sided chi-square test of independence, no Yates correction
          (expected counts are in the thousands).
        - **Effect size:** absolute difference in percentage points, plus a 95%
          Wald interval for the difference.
        - **Sample ratio mismatch:** 44,700 vs 45,489, p ≈ 0.009. The imbalance is
          small and does not explain the retention difference, but it is flagged.
        - **Multiple metrics:** two tests; Bonferroni α = 0.025 and BH FDR both
          leave the 7-day result significant and the 1-day result not significant.
        - **Power:** with ~45k players per arm, the minimum detectable effect is
          about 0.73 pp at 80% power. The observed 0.82 pp effect is close to that
          threshold, so the estimate is imprecise.
        - **Outlier:** one player has 49,854 rounds; removing them does not change
          the conclusion.
        """
    )

st.caption(
    "Data: Cookie Cats mobile game A/B test (Kaggle). Dashboard code: `app.py`. "
    "Full analysis and caveats: `notebook.ipynb`."
)
