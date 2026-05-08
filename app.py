# app.py
# Information Theory × Finance — Shannon Entropy
# Landing page.
# Author: Pranava BA

import streamlit as st

st.set_page_config(
    page_title="Shannon Entropy — ITF",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Injected CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #0f1629 0%, #1c2640 60%, #0f1629 100%);
    border: 1px solid #2a3548;
    border-left: 4px solid #f5a623;
    border-radius: 10px;
    padding: 2.4rem 2.6rem 2rem;
    margin-bottom: 1.8rem;
}
.hero-title {
    font-size: 2.1rem; font-weight: 700; color: #e8edf5;
    letter-spacing: -0.01em; margin: 0 0 0.3rem;
}
.hero-sub {
    font-size: 0.9rem; color: #f5a623; letter-spacing: 0.12em;
    text-transform: uppercase; font-weight: 600; margin: 0 0 1.1rem;
}
.hero-body {
    color: #b0bccc; font-size: 0.97rem; line-height: 1.75;
    max-width: 820px; margin: 0;
}
.formula-label {
    font-size: 0.72rem; color: #5a6e8a; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.6rem;
}
.prop-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 0.9rem; margin-bottom: 1.8rem;
}
.prop-card {
    background: #0f1629; border: 1px solid #2a3548;
    border-radius: 8px; padding: 1rem 1.1rem;
}
.prop-title {
    font-size: 0.72rem; color: #f5a623; letter-spacing: 0.1em;
    text-transform: uppercase; font-weight: 700; margin-bottom: 0.35rem;
}
.prop-body  { color: #b0bccc; font-size: 0.875rem; line-height: 1.55; margin: 0; }
.prop-math  { color: #fbbf45; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }
.nav-card {
    background: #0f1629; border: 1px solid #2a3548; border-radius: 10px;
    padding: 1.5rem 1.6rem; height: 100%; transition: border-color 0.2s;
}
.nav-card:hover { border-color: #f5a623; }
.nav-icon  { font-size: 1.8rem; margin-bottom: 0.5rem; }
.nav-title { font-size: 1.05rem; font-weight: 700; color: #e8edf5; margin-bottom: 0.4rem; }
.nav-desc  { color: #8a9ab8; font-size: 0.875rem; line-height: 1.6; margin: 0; }
.nav-pills { margin-top: 0.8rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
.pill {
    background: #151d33; border: 1px solid #2a3548; border-radius: 20px;
    padding: 2px 10px; font-size: 0.72rem; color: #5a6e8a;
    font-family: 'JetBrains Mono', monospace;
}
.sb-label { font-size: 0.65rem; color: #5a6e8a; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.3rem; }
.sb-value { font-size: 0.88rem; color: #e8edf5; margin-bottom: 0.9rem; }
.sb-link  { color: #f5a623 !important; text-decoration: none; font-size: 0.88rem; }
.sb-link:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.2rem 0 1rem'>
        <div style='font-size:1rem;font-weight:700;color:#e8edf5;'>Shannon Entropy</div>
        <div style='font-size:0.72rem;color:#f5a623;letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;'>
            Information Theory × Finance
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div class='sb-label'>Navigate</div>
    <div class='sb-value'>Use the pages below to explore the Theory and Finance modules.</div>
    <div class='sb-label'>Ticker</div>
    <div class='sb-value' style='font-family:monospace;color:#fbbf45;'>^NSEI (NIFTY 50)</div>
    <div class='sb-label'>Stack</div>
    <div class='sb-value'>Python · NumPy · Streamlit · Plotly · DuckDB</div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div class='sb-label'>Author</div>
    <a class='sb-link' href='https://github.com/pranava-ba' target='_blank'>Pranava BA</a>
    <br/><br/>
    <div class='sb-label'>Series</div>
    <a class='sb-link' href='https://github.com/information-theory-finance' target='_blank'>
        information-theory-finance
    </a>
    """, unsafe_allow_html=True)
    st.caption("v0.1.0 · MIT License")


# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'>Shannon Entropy</div>
    <div class='hero-sub'>Information Theory × NSE Finance</div>
    <p class='hero-body'>
        Shannon entropy is the foundational scalar of information theory —
        the average number of bits required to encode the outcome of a random
        variable. Applied to financial markets it quantifies the
        <em>uncertainty</em> embedded in a return distribution: high entropy
        indicates randomness and market efficiency; low entropy signals
        predictability, thin liquidity, or directional structure.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Formula + worked example ───────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    st.markdown("<div class='formula-label'>Core Formula</div>", unsafe_allow_html=True)
    st.latex(r"H(X) \;=\; -\sum_{x \,\in\, \mathcal{X}} p(x)\,\log_2\,p(x)")
    st.markdown(
        "<p style='color:#5a6e8a;font-size:0.82rem;margin-top:0.3rem;'>"
        "p(x) is the PMF over alphabet 𝒳. Convention: 0 · log 0 := 0. Unit: bits."
        "</p>",
        unsafe_allow_html=True,
    )

with right:
    st.markdown("<div class='formula-label'>Worked Example — Fair 4-sided Die</div>", unsafe_allow_html=True)
    st.latex(r"H = -4 \times 0.25\,\log_2(0.25) = 2\ \text{bits}")
    st.markdown(
        "<p style='color:#5a6e8a;font-size:0.82rem;margin-top:0.3rem;'>"
        "Uniform over 4 outcomes. Exactly 2 binary questions suffice on average."
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
        Zero iff X is deterministic — all mass on one outcome.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Maximum</div>
        <p class='prop-body'><span class='prop-math'>H(X) ≤ log₂|𝒳|</span><br/>
        Achieved uniquely by the uniform distribution.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Concavity</div>
        <p class='prop-body'>H is strictly concave in p — mixing distributions always increases entropy.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Chain Rule</div>
        <p class='prop-body'><span class='prop-math'>H(X,Y) = H(X) + H(Y|X)</span><br/>
        Joint entropy decomposes additively over the conditioning.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Data Processing</div>
        <p class='prop-body'><span class='prop-math'>H(f(X)) ≤ H(X)</span><br/>
        Deterministic functions cannot create new uncertainty.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Continuity</div>
        <p class='prop-body'>H is continuous in p — small perturbations in probability cause small changes in entropy.</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Navigation cards ───────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='font-size:0.72rem;color:#5a6e8a;letter-spacing:0.1em;"
    "text-transform:uppercase;margin-bottom:0.8rem;'>Modules</p>",
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="medium")

with c1:
    st.markdown("""
    <div class='nav-card'>
        <div class='nav-icon'>📐</div>
        <div class='nav-title'>Theory</div>
        <p class='nav-desc'>
            Interactive derivation of H(X). Reshape a PMF with sliders and watch
            entropy update live. Covers the binary entropy curve H_b(p), uniform
            distribution scaling, and a fully configurable custom PMF builder — all
            rendered with Plotly and st.latex().
        </p>
        <div class='nav-pills'>
            <span class='pill'>Binary entropy</span>
            <span class='pill'>Uniform H = log n</span>
            <span class='pill'>Custom PMF</span>
            <span class='pill'>H / H_max</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='nav-card'>
        <div class='nav-icon'>📈</div>
        <div class='nav-title'>Finance</div>
        <p class='nav-desc'>
            Rolling Shannon entropy on NIFTY 50 log-returns alongside annualised
            volatility. Includes a synthetic Level-2 order-book entropy simulator
            across three liquidity regimes and an entropy-threshold backtest
            with full P&amp;L statistics.
        </p>
        <div class='nav-pills'>
            <span class='pill'>^NSEI</span>
            <span class='pill'>Rolling H(X)</span>
            <span class='pill'>Order-book sim</span>
            <span class='pill'>Backtest</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
