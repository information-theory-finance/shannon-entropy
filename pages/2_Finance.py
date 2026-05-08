# pages/2_Finance.py
# Information Theory × Finance — Shannon Entropy
#
# Ticker selection (per Section 6 of the project guide):
#   Concept type: Single-asset entropy / randomness
#   Selected ticker: ^NSEI (NIFTY 50 Index)
#   Reason: Index is clean, high liquidity, broad-market benchmark;
#           ideal for demonstrating rolling entropy as a market-state signal.
#
# Author: Pranava BA

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.fetch import get_ohlcv
from utils.math_core import (
    rolling_entropy,
    rolling_volatility,
    discretise_returns,
    order_book_entropy,
    simulate_order_book,
    entropy_signal,
)
from utils.theme import (
    AMBER, BLUE_ACCENT, GREEN_UP, RED_DOWN,
    TEXT_PRIMARY, NAVY_DARKEST, NAVY_DARK, NAVY_MID,
    NAVY_LIGHT, BORDER, SLATE_LIGHT, SLATE_MID,
    plotly_layout,
)

st.set_page_config(page_title="Finance — Shannon Entropy", layout="wide")

st.title("📈 Shannon Entropy — NSE Finance Application")
st.markdown(
    "Rolling Shannon entropy of NIFTY 50 daily returns, order-book entropy "
    "simulation, and an entropy-threshold trading backtest."
)
st.markdown("---")

# ── Sidebar controls ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Data Controls")
    ticker = st.selectbox("Ticker", ["^NSEI"], index=0)
    window = st.slider("Rolling window (days)", 20, 120, 60, 5)
    n_bins = st.slider("Discretisation bins", 5, 40, 20, 5)
    base = st.selectbox("Log base", [2, 10], index=0,
                        format_func=lambda b: {2: "2 (bits)", 10: "10 (hartleys)"}[b])
    st.divider()
    st.markdown("## Backtest Controls")
    threshold_pct = st.slider("Entry threshold (entropy percentile)", 0.10, 0.50, 0.25, 0.05)
    hold_days = st.slider("Hold period (days)", 1, 20, 5, 1)
    st.divider()
    st.markdown("## Order-Book Simulator")
    ob_regime = st.selectbox("Book regime", ["liquid", "illiquid", "one_sided"])
    ob_levels = st.slider("Price levels", 5, 20, 10, 1)


# ── Data load ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def load_data(tkr: str) -> pd.DataFrame:
    return get_ohlcv(tkr)


with st.spinner("Loading NIFTY 50 data …"):
    try:
        df = load_data(ticker)
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        df["log_return"] = np.log(df["close"] / df["close"].shift(1))
        df = df.dropna(subset=["log_return"])
        data_ok = True
    except Exception as e:
        st.error(f"Data fetch failed: {e}")
        data_ok = False

if not data_ok:
    st.stop()

# ── Compute metrics ────────────────────────────────────────────────────────
entropy_ts = rolling_entropy(df["log_return"], window=window, n_bins=n_bins, base=base)
volatility_ts = rolling_volatility(df["log_return"], window=window)

# ── Data summary ───────────────────────────────────────────────────────────
st.markdown("### Data Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ticker", ticker)
col2.metric("Trading Days", f"{len(df):,}")
col3.metric("Date Range", f"{df.index[0].date()} → {df.index[-1].date()}")
col4.metric(
    "Latest Close",
    f"₹{df['close'].iloc[-1]:,.2f}",
    delta=f"{df['log_return'].iloc[-1]*100:.2f}%",
)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — Rolling entropy + price
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("### Rolling Shannon Entropy of Log-Returns")

fig_main = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    row_heights=[0.45, 0.3, 0.25],
    subplot_titles=[
        f"NIFTY 50 Closing Price",
        f"Rolling Entropy (window={window}, bins={n_bins})",
        f"Rolling Annualised Volatility (window={window})",
    ],
    vertical_spacing=0.06,
)

# Price
fig_main.add_trace(go.Scatter(
    x=df.index, y=df["close"],
    mode="lines", line=dict(color=AMBER, width=1.5),
    name="Close",
), row=1, col=1)

# Entropy
valid_ent = entropy_ts.dropna()
fig_main.add_trace(go.Scatter(
    x=valid_ent.index, y=valid_ent.values,
    mode="lines", line=dict(color=BLUE_ACCENT, width=1.5),
    name="Entropy",
), row=2, col=1)

# Threshold line
threshold_val = valid_ent.quantile(threshold_pct)
fig_main.add_hline(
    y=threshold_val, row=2, col=1,
    line=dict(color=RED_DOWN, dash="dash", width=1.2),
    annotation_text=f"Entry threshold ({int(threshold_pct*100)}th pct)",
    annotation_font_color=RED_DOWN,
)

# Volatility
valid_vol = volatility_ts.dropna()
fig_main.add_trace(go.Scatter(
    x=valid_vol.index, y=valid_vol.values,
    mode="lines", line=dict(color=GREEN_UP, width=1.5),
    name="Ann. Volatility",
), row=3, col=1)

base_layout = plotly_layout(title="NIFTY 50 — Price · Entropy · Volatility")
fig_main.update_layout(
    **base_layout,
    height=680,
    showlegend=True,
)
for i in range(1, 4):
    fig_main.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=i, col=1)
    fig_main.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=i, col=1)

st.plotly_chart(fig_main, use_container_width=True)

# ─ Summary metrics ─────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Entropy", f"{valid_ent.iloc[-1]:.4f} bits")
m2.metric("Mean Entropy", f"{valid_ent.mean():.4f} bits")
m3.metric(f"{int(threshold_pct*100)}th Pct (entry)", f"{threshold_val:.4f} bits")
m4.metric("Corr(H, Vol)", f"{valid_ent.corr(valid_vol.reindex(valid_ent.index)):.3f}")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — Entropy vs Volatility scatter
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("### Entropy vs Volatility Scatter")

merged = pd.concat([valid_ent.rename("entropy"), valid_vol.rename("volatility")], axis=1).dropna()
year_color = merged.index.year

fig_scatter = go.Figure(go.Scatter(
    x=merged["volatility"],
    y=merged["entropy"],
    mode="markers",
    marker=dict(
        color=year_color,
        colorscale="YlOrRd",
        size=4,
        opacity=0.7,
        colorbar=dict(title="Year", tickfont=dict(color=TEXT_PRIMARY)),
        showscale=True,
    ),
    text=merged.index.strftime("%Y-%m-%d"),
    hovertemplate="<b>%{text}</b><br>Vol: %{x:.3f}<br>Entropy: %{y:.4f}<extra></extra>",
))

fig_scatter.update_layout(
    **plotly_layout(
        title="Rolling Entropy vs Rolling Annualised Volatility",
        x_title="Annualised Volatility",
        y_title=f"Shannon Entropy [bits]",
    )
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption(
    f"Pearson correlation: {merged['entropy'].corr(merged['volatility']):.4f}. "
    "High-volatility regimes tend to coincide with elevated entropy (more uncertainty)."
)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 — Return distribution & PMF
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("### Return Distribution (most recent window)")

recent_returns = df["log_return"].tail(window)
pmf = discretise_returns(recent_returns, n_bins=n_bins)
bin_labels = [f"b{i+1}" for i in range(len(pmf))]

fig_pmf = go.Figure(go.Bar(
    x=bin_labels,
    y=pmf,
    marker_color=AMBER,
    name="p(return bin)",
))
fig_pmf.update_layout(
    **plotly_layout(
        title=f"Empirical PMF — Last {window} NIFTY 50 Log-Returns",
        x_title="Return bin",
        y_title="Probability",
    )
)
st.plotly_chart(fig_pmf, use_container_width=True)
from utils.math_core import shannon_entropy as _h
_h_recent = _h(pmf, base=base)
st.metric("Entropy of this window", f"{_h_recent:.4f} bits")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4 — Order-book entropy simulator
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("### Order-Book Entropy Simulator")
st.markdown(
    "Simulates a synthetic Level-2 order book and computes Shannon entropy "
    "of the bid/ask volume distributions. High entropy → flat book (liquid). "
    "Low entropy → concentrated volume (thin market)."
)

rng = np.random.default_rng(7)
book = simulate_order_book(
    mid_price=df["close"].iloc[-1],
    n_levels=ob_levels,
    regime=ob_regime,
    rng=rng,
)
ob_stats = order_book_entropy(book["bid_volumes"], book["ask_volumes"], base=base)

fig_ob = make_subplots(
    rows=1, cols=2,
    subplot_titles=["Bid Side Volume", "Ask Side Volume"],
    horizontal_spacing=0.1,
)
fig_ob.add_trace(go.Bar(
    x=[f"L{i+1}" for i in range(ob_levels)],
    y=book["bid_volumes"],
    marker_color=GREEN_UP,
    name="Bid",
), row=1, col=1)
fig_ob.add_trace(go.Bar(
    x=[f"L{i+1}" for i in range(ob_levels)],
    y=book["ask_volumes"],
    marker_color=RED_DOWN,
    name="Ask",
), row=1, col=2)
base_ob = plotly_layout(title=f"Order Book — Regime: {ob_regime.title()}")
fig_ob.update_layout(**base_ob, height=350, showlegend=True)
for col in [1, 2]:
    fig_ob.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=1, col=col)
    fig_ob.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=1, col=col)
st.plotly_chart(fig_ob, use_container_width=True)

ob1, ob2, ob3, ob4 = st.columns(4)
ob1.metric("Bid Entropy", f"{ob_stats['bid_entropy']:.4f} bits")
ob2.metric("Ask Entropy", f"{ob_stats['ask_entropy']:.4f} bits")
ob3.metric("Book Entropy", f"{ob_stats['book_entropy']:.4f} bits")
ob4.metric("OBI", f"{ob_stats['imbalance']:+.3f}")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5 — Backtest
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("### Entropy-Threshold Backtest")
st.markdown(
    f"**Signal:** Enter long when rolling entropy < {int(threshold_pct*100)}th percentile "
    f"({threshold_val:.4f} bits). Hold for {hold_days} trading days. "
    "No leverage, no transaction costs."
)

bt = entropy_signal(
    entropy_ts,
    df["close"],
    threshold_pct=threshold_pct,
    hold_days=hold_days,
)

fig_bt = go.Figure()
fig_bt.add_trace(go.Scatter(
    x=bt.index, y=bt["cum_buyhold"],
    mode="lines", line=dict(color=SLATE_LIGHT, width=1.5, dash="dot"),
    name="Buy & Hold",
))
fig_bt.add_trace(go.Scatter(
    x=bt.index, y=bt["cum_strategy"],
    mode="lines", line=dict(color=AMBER, width=2),
    name=f"Entropy Signal (thr={threshold_pct:.0%}, hold={hold_days}d)",
))
# Shade entry zones
entry_dates = bt.index[bt["signal"] == 1]
if len(entry_dates) > 0:
    fig_bt.add_trace(go.Scatter(
        x=bt.index,
        y=bt["cum_strategy"].where(bt["signal"] == 1),
        mode="lines",
        line=dict(color=GREEN_UP, width=3),
        name="In trade",
    ))
fig_bt.update_layout(
    **plotly_layout(
        title="Cumulative Return — Entropy Signal vs Buy & Hold (NIFTY 50)",
        x_title="Date",
        y_title="Cumulative Return",
    )
)
st.plotly_chart(fig_bt, use_container_width=True)

# Backtest stats
strat_returns = bt["strategy_return"].dropna()
bh_returns = bt["buy_hold_return"].dropna()

def sharpe(r: pd.Series) -> float:
    if r.std() == 0:
        return 0.0
    return float(r.mean() / r.std() * np.sqrt(252))

def max_drawdown(cum: pd.Series) -> float:
    roll_max = cum.cummax()
    dd = (cum - roll_max) / roll_max
    return float(dd.min())

def win_rate(r: pd.Series) -> float:
    active = r[r != 0]
    if len(active) == 0:
        return 0.0
    return float((active > 0).sum() / len(active))

bt_stats = {
    "Total Return": [
        f"{(bt['cum_strategy'].iloc[-1] - 1)*100:.2f}%",
        f"{(bt['cum_buyhold'].iloc[-1] - 1)*100:.2f}%",
    ],
    "Sharpe Ratio": [
        f"{sharpe(strat_returns):.3f}",
        f"{sharpe(bh_returns):.3f}",
    ],
    "Max Drawdown": [
        f"{max_drawdown(bt['cum_strategy'])*100:.2f}%",
        f"{max_drawdown(bt['cum_buyhold'])*100:.2f}%",
    ],
    "Win Rate": [
        f"{win_rate(strat_returns):.1%}",
        "N/A",
    ],
    "Days in Market": [
        f"{int(bt['signal'].sum())} / {len(bt)}",
        f"{len(bt)} / {len(bt)}",
    ],
}
bt_df = pd.DataFrame(bt_stats, index=["Entropy Signal", "Buy & Hold"]).T
st.dataframe(bt_df, use_container_width=True)

st.caption(
    "⚠ Backtest is in-sample and does not account for transaction costs, "
    "slippage, or look-ahead bias. Results are illustrative only."
)
