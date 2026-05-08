# pages/2_Finance.py — Finance: rolling entropy on NIFTY 50
# Ticker: ^NSEI (single-asset entropy, broad-market benchmark)
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
    rolling_entropy, rolling_volatility, discretise_returns,
    shannon_entropy as _h,
    order_book_entropy, simulate_order_book, entropy_signal,
)
from utils.theme import (
    PAGE_CSS, AMBER, AMBER_LIGHT, BLUE_ACCENT, GREEN_UP, RED_DOWN,
    TEXT_PRIMARY, NAVY_DARKEST, NAVY_DARK, NAVY_MID, NAVY_LIGHT,
    BORDER, SLATE_LIGHT, SLATE_MID, plotly_layout,
)

st.set_page_config(page_title="Finance — Shannon Entropy", layout="wide")
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.4rem 0 0.8rem'>
        <div style='font-size:1rem;font-weight:700;color:#e8edf5;'>Shannon Entropy</div>
        <div style='font-size:0.7rem;color:#f5a623;letter-spacing:0.1em;text-transform:uppercase;margin-top:3px;'>
            Finance
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<div class='sb-eyebrow'>Rolling Window</div>", unsafe_allow_html=True)
    window = st.slider("", 20, 120, 60, 5, label_visibility="collapsed", key="fin_win")

    st.markdown("<div class='sb-eyebrow'>Discretisation Bins</div>", unsafe_allow_html=True)
    n_bins = st.slider("", 5, 40, 20, 5, label_visibility="collapsed", key="fin_bins")

    st.markdown("<div class='sb-eyebrow'>Log Base</div>", unsafe_allow_html=True)
    base = st.selectbox("", [2, 10], label_visibility="collapsed",
                        format_func=lambda b: {2: "2 → bits", 10: "10 → hartleys"}[b])
    unit = {2: "bits", 10: "hartleys"}[base]

    st.divider()
    st.markdown("<div class='sb-eyebrow'>Backtest</div>", unsafe_allow_html=True)
    threshold_pct = st.slider("Entry percentile", 0.10, 0.50, 0.25, 0.05)
    hold_days     = st.slider("Hold period (days)", 1, 20, 5, 1)

    st.divider()
    st.markdown("<div class='sb-eyebrow'>Order-Book Simulator</div>", unsafe_allow_html=True)
    ob_regime = st.selectbox("Regime", ["liquid", "illiquid", "one_sided"],
                             format_func=lambda x: x.replace("_", "-").title())
    ob_levels = st.slider("Price levels", 5, 20, 10, 1)

    st.divider()
    st.page_link("app.py", label="← Back to Home", use_container_width=True)
    st.page_link("pages/1_Theory.py", label="Theory →", use_container_width=True)

# ── Data ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def load(tkr):
    return get_ohlcv(tkr)

with st.spinner("Fetching NIFTY 50 data …"):
    try:
        df = load("^NSEI")
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

entropy_ts = rolling_entropy(df["log_return"], window=window, n_bins=n_bins, base=base)
vol_ts     = rolling_volatility(df["log_return"], window=window)
valid_ent  = entropy_ts.dropna()
valid_vol  = vol_ts.dropna()
threshold_val = valid_ent.quantile(threshold_pct)

# ── Page header ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='page-hero'>
    <div class='page-hero-eyebrow'>Module 2 · NSE Application</div>
    <div class='page-hero-title'>Entropy as a Market-State Signal</div>
    <p class='page-hero-body'>
        We compute rolling Shannon entropy of NIFTY 50 log-returns as a
        single scalar summarising how predictable (or random) the return
        distribution has been over the past {window} trading sessions.
        Low entropy ≠ low volatility: entropy measures distributional
        <em>shape</em>, not spread — it drops when returns cluster in a
        few bins, regardless of their magnitude.
    </p>
</div>
""", unsafe_allow_html=True)

# Data summary pills
latest_close  = df["close"].iloc[-1]
latest_ret    = df["log_return"].iloc[-1]
latest_ent    = valid_ent.iloc[-1]
latest_vol    = valid_vol.iloc[-1]
corr_hv       = valid_ent.corr(valid_vol.reindex(valid_ent.index))
st.markdown(f"""
<div class='stat-row'>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Ticker</div>
        <div class='stat-pill-val'>^NSEI</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Trading Days</div>
        <div class='stat-pill-val'>{len(df):,}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Latest Close</div>
        <div class='stat-pill-val'>₹{latest_close:,.0f}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Current Entropy</div>
        <div class='stat-pill-val'>{latest_ent:.3f} {unit}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Mean Entropy</div>
        <div class='stat-pill-val'>{valid_ent.mean():.3f} {unit}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Corr(H, Vol)</div>
        <div class='stat-pill-val'>{corr_hv:+.3f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — Three-panel chart
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 1</div>
<div class='section-title'>Price · Rolling Entropy · Volatility</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='info-card' style='margin-bottom:1rem;'>
    <p>
        The three panels share the same time axis. <em>Entropy</em> and
        <em>volatility</em> are both rolling statistics over the same window,
        but they measure different things: volatility measures the dispersion
        (std dev) of returns; entropy measures how evenly the returns are spread
        across all bins — a fat-tailed distribution can have lower entropy than
        a thin-tailed one with the same variance.
    </p>
</div>
""", unsafe_allow_html=True)

fig_main = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    row_heights=[0.45, 0.3, 0.25],
    vertical_spacing=0.04,
)
fig_main.add_trace(go.Scatter(
    x=df.index, y=df["close"], mode="lines",
    line=dict(color=AMBER, width=1.5), name="Close",
), row=1, col=1)
fig_main.add_trace(go.Scatter(
    x=valid_ent.index, y=valid_ent.values, mode="lines",
    line=dict(color=BLUE_ACCENT, width=1.5), name=f"H(X)  [{unit}]",
), row=2, col=1)
fig_main.add_hline(
    y=threshold_val, row=2, col=1,
    line=dict(color=RED_DOWN, dash="dash", width=1),
    annotation_text=f"Entry threshold ({int(threshold_pct*100)}th pct = {threshold_val:.3f})",
    annotation_font_color=RED_DOWN, annotation_font_size=10,
)
fig_main.add_trace(go.Scatter(
    x=valid_vol.index, y=valid_vol.values, mode="lines",
    line=dict(color=GREEN_UP, width=1.5), name="Ann. Vol",
), row=3, col=1)

fig_main.update_layout(
    **plotly_layout(title=f"NIFTY 50 — {window}-day Rolling Entropy & Volatility"),
    height=620, showlegend=True,
)
for i in range(1, 4):
    fig_main.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=i, col=1)
    fig_main.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=i, col=1)

st.plotly_chart(fig_main, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — Entropy vs Volatility
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 2</div>
<div class='section-title'>Entropy vs Annualised Volatility</div>
""", unsafe_allow_html=True)

col_s1, col_s2 = st.columns([2, 1], gap="large")

with col_s1:
    merged = pd.concat(
        [valid_ent.rename("H"), valid_vol.rename("vol")], axis=1
    ).dropna()
    yr = merged.index.year

    fig_sc = go.Figure(go.Scatter(
        x=merged["vol"], y=merged["H"], mode="markers",
        marker=dict(color=yr, colorscale="YlOrRd", size=4, opacity=0.7,
                    colorbar=dict(title="Year", tickfont=dict(color=TEXT_PRIMARY))),
        text=merged.index.strftime("%Y-%m-%d"),
        hovertemplate="<b>%{text}</b><br>Vol: %{x:.3f}<br>H: %{y:.4f}<extra></extra>",
    ))
    fig_sc.update_layout(**plotly_layout(
        title="H(X) vs Volatility — Each point = one trading day",
        x_title="Annualised Volatility",
        y_title=f"H(X)  [{unit}]",
    ))
    st.plotly_chart(fig_sc, use_container_width=True)

with col_s2:
    st.markdown("""
    <div class='info-card'>
        <p>
            <em>Why does this correlation exist?</em><br/><br/>
            In high-volatility regimes (e.g. COVID crash, 2022 drawdown),
            returns are spread across more bins — the distribution widens
            and flattens, driving entropy up.<br/><br/>
            In low-volatility trending markets, returns cluster in a few
            bins (small positive moves day after day), driving entropy down.
            This is the regime the backtest signal targets.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='stat-row' style='margin-top:0.8rem;flex-direction:column;'>
        <div class='stat-pill'>
            <div class='stat-pill-label'>Pearson ρ(H, Vol)</div>
            <div class='stat-pill-val'>{corr_hv:+.4f}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>Date range</div>
            <div class='stat-pill-val'>{df.index[0].date()} → {df.index[-1].date()}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>Entry threshold</div>
            <div class='stat-pill-val'>{threshold_val:.4f} {unit}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 — Order-book entropy
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 3</div>
<div class='section-title'>Order-Book Entropy Simulation</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='info-card' style='margin-bottom:1rem;'>
    <p>
        A real Level-2 order book is a list of (price, volume) pairs on each
        side. We treat the normalised volume vector as a PMF and compute
        H(bid) and H(ask) separately.<br/><br/>
        <em>High bid entropy:</em> volume spread evenly across price levels —
        deep, liquid book. No single level dominates.<br/>
        <em>Low bid entropy:</em> volume concentrated near the best bid —
        thin book, large volumes waiting at one price. This often precedes
        a large move once that wall is absorbed.
    </p>
</div>
""", unsafe_allow_html=True)

rng  = np.random.default_rng(7)
book = simulate_order_book(mid_price=df["close"].iloc[-1], n_levels=ob_levels,
                           regime=ob_regime, rng=rng)
obs  = order_book_entropy(book["bid_volumes"], book["ask_volumes"], base=base)

fig_ob = make_subplots(rows=1, cols=2,
                       subplot_titles=["Bid Side", "Ask Side"],
                       horizontal_spacing=0.1)
fig_ob.add_trace(go.Bar(
    x=[f"L{i+1}" for i in range(ob_levels)], y=book["bid_volumes"],
    marker_color=GREEN_UP, name="Bid",
), row=1, col=1)
fig_ob.add_trace(go.Bar(
    x=[f"L{i+1}" for i in range(ob_levels)], y=book["ask_volumes"],
    marker_color=RED_DOWN, name="Ask",
), row=1, col=2)
fig_ob.update_layout(
    **plotly_layout(title=f"Synthetic Order Book — {ob_regime.replace('_','-').title()} Regime"),
    height=340, showlegend=True,
)
for c in [1, 2]:
    fig_ob.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=1, col=c)
    fig_ob.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=SLATE_LIGHT, row=1, col=c)
st.plotly_chart(fig_ob, use_container_width=True)

st.markdown(f"""
<div class='stat-row'>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Bid Entropy</div>
        <div class='stat-pill-val'>{obs['bid_entropy']:.4f} {unit}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Ask Entropy</div>
        <div class='stat-pill-val'>{obs['ask_entropy']:.4f} {unit}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Book Entropy</div>
        <div class='stat-pill-val'>{obs['book_entropy']:.4f} {unit}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Order Imbalance</div>
        <div class='stat-pill-val'>{obs['imbalance']:+.3f}</div>
    </div>
    <div class='stat-pill'>
        <div class='stat-pill-label'>Spread</div>
        <div class='stat-pill-val'>₹{book['spread']:.2f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4 — Backtest
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 4</div>
<div class='section-title'>Entropy-Threshold Backtest</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='info-card' style='margin-bottom:1rem;'>
    <p>
        <em>Signal logic:</em> enter long NIFTY 50 when the rolling entropy
        falls below the {int(threshold_pct*100)}th percentile of its own history
        ({threshold_val:.4f} {unit}). Hold for {hold_days} trading days, then exit flat.
        No leverage, no transaction costs, no short selling.<br/><br/>
        <em>Rationale:</em> a drop in entropy means recent returns have become
        less uniformly distributed — they are clustering in a subset of bins.
        This often coincides with a directional market regime where a simple
        long position captures the move before the distribution widens again.
    </p>
</div>
""", unsafe_allow_html=True)

bt = entropy_signal(entropy_ts, df["close"],
                    threshold_pct=threshold_pct, hold_days=hold_days)

fig_bt = go.Figure()
fig_bt.add_trace(go.Scatter(
    x=bt.index, y=bt["cum_buyhold"],
    mode="lines", line=dict(color=SLATE_MID, width=1.5, dash="dot"),
    name="Buy & Hold",
))
fig_bt.add_trace(go.Scatter(
    x=bt.index, y=bt["cum_strategy"],
    mode="lines", line=dict(color=AMBER, width=2),
    name=f"Entropy Signal (thr={threshold_pct:.0%}, hold={hold_days}d)",
))
fig_bt.add_trace(go.Scatter(
    x=bt.index, y=bt["cum_strategy"].where(bt["signal"] == 1),
    mode="lines", line=dict(color=GREEN_UP, width=3),
    name="In Trade",
))
fig_bt.update_layout(**plotly_layout(
    title=f"Cumulative Return — Entropy Signal vs Buy & Hold  (^NSEI)",
    x_title="Date", y_title="Cumulative Return (×)",
))
st.plotly_chart(fig_bt, use_container_width=True)

# Stats table
def sharpe(r):
    return float(r.mean() / r.std() * np.sqrt(252)) if r.std() > 0 else 0.0

def mdd(cum):
    return float(((cum - cum.cummax()) / cum.cummax()).min())

def winrate(r):
    a = r[r != 0]
    return float((a > 0).sum() / len(a)) if len(a) > 0 else 0.0

sr, br = bt["strategy_return"].dropna(), bt["buy_hold_return"].dropna()
stats = pd.DataFrame({
    "Total Return":  [f"{(bt['cum_strategy'].iloc[-1]-1)*100:.2f}%", f"{(bt['cum_buyhold'].iloc[-1]-1)*100:.2f}%"],
    "Sharpe Ratio":  [f"{sharpe(sr):.3f}", f"{sharpe(br):.3f}"],
    "Max Drawdown":  [f"{mdd(bt['cum_strategy'])*100:.2f}%", f"{mdd(bt['cum_buyhold'])*100:.2f}%"],
    "Win Rate":      [f"{winrate(sr):.1%}", "—"],
    "Days in Market":[f"{int(bt['signal'].sum())} / {len(bt)}", f"{len(bt)} / {len(bt)}"],
}, index=["Entropy Signal", "Buy & Hold"]).T

st.dataframe(stats, use_container_width=True)
st.caption(
    "⚠ In-sample backtest only. No transaction costs, slippage, or look-ahead correction. "
    "Threshold is fitted on the full history — live deployment requires an expanding-window percentile."
)
