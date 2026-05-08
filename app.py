# app.py — Landing page with working navigation
# Author: Pranava BA

import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Shannon Entropy — ITF",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.theme import PAGE_CSS
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# Extra hero-only CSS
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #0f1629 0%, #1c2640 60%, #0f1629 100%);
    border: 1px solid #2a3548;
    border-left: 4px solid #f5a623;
    border-radius: 10px;
    padding: 2.4rem 2.6rem 2rem;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    font-size: 0.72rem; color: #f5a623; letter-spacing: 0.14em;
    text-transform: uppercase; font-weight: 700; margin-bottom: 0.4rem;
}
.hero-title {
    font-size: 2.2rem; font-weight: 700; color: #e8edf5;
    letter-spacing: -0.02em; margin: 0 0 0.4rem;
}
.hero-body {
    color: #8a9ab8; font-size: 0.97rem; line-height: 1.78;
    max-width: 800px; margin: 0;
}
.formula-eyebrow {
    font-size: 0.68rem; color: #5a6e8a; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 0.5rem;
}
.nav-card {
    background: #0f1629; border: 1px solid #2a3548;
    border-radius: 10px; padding: 1.5rem 1.6rem;
}
.nav-card-eyebrow {
    font-size: 0.68rem; color: #f5a623; letter-spacing: 0.12em;
    text-transform: uppercase; font-weight: 700; margin-bottom: 0.3rem;
}
.nav-card-title {
    font-size: 1.1rem; font-weight: 700; color: #e8edf5; margin-bottom: 0.5rem;
}
.nav-card-body {
    color: #8a9ab8; font-size: 0.875rem; line-height: 1.65; margin: 0 0 0.9rem;
}
.pill-row { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.pill {
    background: #151d33; border: 1px solid #2a3548; border-radius: 20px;
    padding: 3px 10px; font-size: 0.7rem; color: #5a6e8a;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.4rem 0 0.8rem'>
        <div style='font-size:1rem;font-weight:700;color:#e8edf5;'>Shannon Entropy</div>
        <div style='font-size:0.7rem;color:#f5a623;letter-spacing:0.1em;text-transform:uppercase;margin-top:3px;'>
            Information Theory × Finance
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div class='sb-eyebrow'>Ticker</div>
    <div class='sb-value' style='font-family:monospace;color:#fbbf45;'>^NSEI — NIFTY 50</div>
    <div class='sb-eyebrow'>Stack</div>
    <div class='sb-value'>Python · NumPy · Streamlit · Plotly · DuckDB</div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div class='sb-eyebrow'>Author</div>
    <a class='sb-link' href='https://github.com/pranava-ba' target='_blank'>Pranava BA</a><br/><br/>
    <div class='sb-eyebrow'>Series</div>
    <a class='sb-link' href='https://github.com/information-theory-finance' target='_blank'>information-theory-finance</a>
    """, unsafe_allow_html=True)
    st.caption("v0.1.0 · MIT License")

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-eyebrow'>Information Theory × NSE Finance</div>
    <div class='hero-title'>Shannon Entropy</div>
    <p class='hero-body'>
        Shannon entropy H(X) is the expected information content of a random variable —
        the average number of bits needed to encode its outcome. In financial markets,
        it translates directly into a market-state diagnostic: a high-entropy return
        distribution looks uniform and unpredictable (efficient market); a low-entropy
        one is concentrated, signalling structure, drift, or thin liquidity that a
        quantitative strategy can act on.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Core formula ───────────────────────────────────────────────────────────
fcol, ecol = st.columns([1, 1], gap="large")

with fcol:
    st.markdown("<div class='formula-eyebrow'>Definition</div>", unsafe_allow_html=True)
    st.latex(r"H(X) \;=\; -\sum_{x \,\in\, \mathcal{X}} p(x)\,\log_2\,p(x)")
    st.markdown(
        "<p style='color:#5a6e8a;font-size:0.82rem;line-height:1.6;margin-top:0.5rem;'>"
        "p(x) is the PMF over alphabet 𝒳 &nbsp;·&nbsp; Unit: bits (base 2) "
        "&nbsp;·&nbsp; Convention: 0·log 0 := 0"
        "</p>",
        unsafe_allow_html=True,
    )

with ecol:
    st.markdown("<div class='formula-eyebrow'>Derivation from Surprise</div>", unsafe_allow_html=True)
    st.latex(r"\underbrace{-\log_2 p(x)}_{\text{surprise } I(x)} \;\Rightarrow\; H(X) = \mathbb{E}[\,I(X)\,]")
    st.markdown(
        "<p style='color:#5a6e8a;font-size:0.82rem;line-height:1.6;margin-top:0.5rem;'>"
        "Entropy is simply the expected surprise. Rare events carry more information; "
        "H(X) averages this over the whole distribution."
        "</p>",
        unsafe_allow_html=True,
    )

st.markdown("<br/>", unsafe_allow_html=True)

# ── Properties grid ────────────────────────────────────────────────────────
st.markdown("""
<div class='prop-grid'>
    <div class='prop-card'>
        <div class='prop-title'>Non-negativity</div>
        <p class='prop-body'><span class='prop-math'>H(X) ≥ 0</span><br/>
        Zero iff X is deterministic. No uncertainty = no information.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Maximum Entropy</div>
        <p class='prop-body'><span class='prop-math'>H(X) ≤ log₂|𝒳|</span><br/>
        Achieved by the uniform PMF — maximum ignorance.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Concavity</div>
        <p class='prop-body'>H is strictly concave in p. Mixing two distributions
        always produces higher entropy than either alone.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Chain Rule</div>
        <p class='prop-body'><span class='prop-math'>H(X,Y) = H(X) + H(Y|X)</span><br/>
        Joint entropy decomposes into marginal + conditional.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Data Processing</div>
        <p class='prop-body'><span class='prop-math'>H(f(X)) ≤ H(X)</span><br/>
        Processing information can only lose it, never create it.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Additivity</div>
        <p class='prop-body'>For independent X, Y:<br/>
        <span class='prop-math'>H(X,Y) = H(X) + H(Y)</span></p>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Navigation cards with working page links ───────────────────────────────
st.markdown(
    "<p style='font-size:0.68rem;color:#5a6e8a;letter-spacing:0.12em;"
    "text-transform:uppercase;margin-bottom:1rem;'>Explore</p>",
    unsafe_allow_html=True,
)

nc1, nc2 = st.columns(2, gap="medium")

with nc1:
    st.markdown("""
    <div class='nav-card'>
        <div class='nav-card-eyebrow'>Module 1</div>
        <div class='nav-card-title'>📐 Theory</div>
        <p class='nav-card-body'>
            Build intuition for H(X) from the ground up. Explore the binary
            entropy curve H<sub>b</sub>(p), see how entropy scales with
            alphabet size, and construct arbitrary PMFs with live entropy readout.
            Every formula is derived, not just stated.
        </p>
        <div class='pill-row'>
            <span class='pill'>H_b(p) curve</span>
            <span class='pill'>Uniform H = log n</span>
            <span class='pill'>Custom PMF</span>
            <span class='pill'>H / H_max</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Theory.py", label="Open Theory →", use_container_width=True)

with nc2:
    st.markdown("""
    <div class='nav-card'>
        <div class='nav-card-eyebrow'>Module 2</div>
        <div class='nav-card-title'>📈 Finance</div>
        <p class='nav-card-body'>
            Apply rolling Shannon entropy to NIFTY 50 log-returns as a
            market-state signal. Simulate Level-2 order-book entropy across
            three liquidity regimes and backtest a simple entropy-threshold
            long strategy with full P&amp;L statistics.
        </p>
        <div class='pill-row'>
            <span class='pill'>^NSEI rolling H</span>
            <span class='pill'>Order-book sim</span>
            <span class='pill'>H vs volatility</span>
            <span class='pill'>Backtest</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Finance.py", label="Open Finance →", use_container_width=True)
