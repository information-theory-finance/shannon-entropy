"""
Shannon Entropy — Finance Page
Rolling entropy of log returns for NSE tickers.

Tickers used: ^NSEI (NIFTY 50), GOLDBEES.NS (Nippon Gold ETF)
Reason: NIFTY 50 gives the broad market baseline; GOLDBEES has a distinct entropy
profile driven by macro/currency factors rather than equity sentiment.
Comparing them illustrates how entropy differs across asset classes.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.fetch import get_log_returns, get_ohlcv
from utils.math_core import entropy_from_data, rolling_entropy
from utils.theme import AMBER, AMBER_LIGHT, BLUE_ACCENT, GREEN_UP, RED_DOWN, SILVER_LIGHT, plotly_layout

st.set_page_config(
    page_title="Finance · Shannon Entropy · ITF",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Shannon Entropy — NSE Application")
st.caption("Rolling entropy of log returns · NSE data via yfinance · Auto-updated daily")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Data Controls")
    ticker = st.selectbox(
        "Ticker",
        ["^NSEI", "GOLDBEES.NS"],
        format_func=lambda t: {"^NSEI": "NIFTY 50 (^NSEI)", "GOLDBEES.NS": "Nippon Gold ETF (GOLDBEES.NS)"}[t],
    )
    start_date = st.date_input("Start date", value=pd.Timestamp("2018-01-01"))
    st.divider()
    st.header("Entropy Parameters")
    window = st.slider("Rolling window (trading days)", 20, 120, 60, step=5)
    bins = st.slider("Histogram bins", 10, 60, 25, step=5)
    log_base = st.selectbox("Entropy units", ["bits (base 2)", "nats (base e)"], index=0)
    base = {"bits (base 2)": 2.0, "nats (base e)": np.e}[log_base]
    unit = {"bits (base 2)": "bits", "nats (base e)": "nats"}[log_base]
    st.divider()
    st.caption("Data fetches on first load and auto-refreshes every 24 h.")


@st.cache_data(ttl=86400)
def load_data(ticker: str, start: str) -> tuple[pd.DataFrame, pd.Series]:
    ohlcv = get_ohlcv(ticker, start=start)
    returns = get_log_returns(ticker, start=start)
    return ohlcv, returns


with st.spinner(f"Fetching {ticker} data…"):
    ohlcv, returns = load_data(ticker, str(start_date))

if ohlcv.empty:
    st.error("No data returned. Check your internet connection and try again.")
    st.stop()

ohlcv["date"] = pd.to_datetime(ohlcv["date"])
ohlcv = ohlcv.sort_values("date")

# ── Rolling entropy ───────────────────────────────────────────────────────────
ret_arr = returns.values
roll_ent = rolling_entropy(ret_arr, window=window, bins=bins, base=base)
ent_series = pd.Series(roll_ent, index=returns.index, name="rolling_entropy")

# ── KPI row ───────────────────────────────────────────────────────────────────
valid_ent = ent_series.dropna()
current_H  = valid_ent.iloc[-1]  if len(valid_ent) else float("nan")
mean_H     = valid_ent.mean()    if len(valid_ent) else float("nan")
max_H      = valid_ent.max()     if len(valid_ent) else float("nan")
min_H      = valid_ent.min()     if len(valid_ent) else float("nan")
current_ret = returns.iloc[-1]  if len(returns) else float("nan")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Current Entropy", f"{current_H:.3f} {unit}", delta=f"{current_H - mean_H:+.3f} vs avg")
k2.metric("Mean Entropy", f"{mean_H:.3f} {unit}")
k3.metric("Max Entropy", f"{max_H:.3f} {unit}")
k4.metric("Min Entropy", f"{min_H:.3f} {unit}")
k5.metric("Latest Return", f"{current_ret*100:.3f}%", delta=None)

st.divider()

# ── Main chart: Price + Rolling Entropy ──────────────────────────────────────
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.55, 0.45],
    vertical_spacing=0.06,
    subplot_titles=["Close Price", f"Rolling Entropy ({window}-day window, {bins} bins)"],
)

fig.add_trace(
    go.Scatter(
        x=ohlcv["date"], y=ohlcv["close"],
        mode="lines", line=dict(color=AMBER, width=1.5), name="Close",
    ),
    row=1, col=1,
)

# Colour entropy line by high/low relative to mean
ent_colours = [GREEN_UP if v >= mean_H else RED_DOWN for v in ent_series.fillna(mean_H)]
fig.add_trace(
    go.Scatter(
        x=ent_series.index, y=ent_series.values,
        mode="lines", line=dict(color=BLUE_ACCENT, width=1.5), name=f"H(X) [{unit}]",
    ),
    row=2, col=1,
)
fig.add_hline(
    y=mean_H, line=dict(color=AMBER_LIGHT, dash="dot", width=1),
    annotation_text=f"mean {mean_H:.3f}", annotation_font_color=AMBER_LIGHT,
    row=2, col=1,
)

layout = plotly_layout(title=f"{ticker} — Price & Rolling Shannon Entropy")
layout.update({"height": 600, "showlegend": True})
fig.update_layout(**layout)
fig.update_xaxes(gridcolor="#2a3a5c", zerolinecolor="#2a3a5c", color=SILVER_LIGHT)
fig.update_yaxes(gridcolor="#2a3a5c", zerolinecolor="#2a3a5c", color=SILVER_LIGHT)

st.plotly_chart(fig, use_container_width=True)

# ── Return distribution ───────────────────────────────────────────────────────
st.subheader("Return Distribution")
col_hist, col_stats = st.columns([2, 1])

with col_hist:
    counts, bin_edges = np.histogram(ret_arr, bins=60)
    bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    pmf = counts / counts.sum()
    H_full = entropy_from_data(ret_arr, bins=60, base=base)

    fig_hist = go.Figure()
    fig_hist.add_trace(
        go.Bar(
            x=bin_centres, y=pmf,
            marker_color=AMBER, marker_line_color="#0f1629", marker_line_width=0.4,
            name="PMF",
        )
    )
    fig_hist.update_layout(
        **plotly_layout(
            title=f"Log Return Distribution — H(X) = {H_full:.3f} {unit}",
            x_title="Log Return", y_title="p(x)",
        )
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_stats:
    st.markdown("**Return statistics**")
    st.dataframe(
        pd.DataFrame({
            "Statistic": ["Count", "Mean", "Std Dev", "Skew", "Kurtosis", "Min", "Max"],
            "Value": [
                len(ret_arr),
                f"{ret_arr.mean():.6f}",
                f"{ret_arr.std():.6f}",
                f"{pd.Series(ret_arr).skew():.4f}",
                f"{pd.Series(ret_arr).kurtosis():.4f}",
                f"{ret_arr.min():.6f}",
                f"{ret_arr.max():.6f}",
            ],
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.metric("Full-sample H(X)", f"{H_full:.4f} {unit}")

st.divider()
st.caption(
    f"Data: {ticker} · Source: NSE via yfinance · "
    f"Stored in DuckDB at data/nse.duckdb · Window: {window} days · Bins: {bins}"
)
