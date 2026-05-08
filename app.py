# app.py
# Information Theory × Finance — Shannon Entropy
# Landing page: formula, description, sidebar controls.
# Author: Pranava BA

import streamlit as st

st.set_page_config(
    page_title="Shannon Entropy — ITF",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Title ──────────────────────────────────────────────────────────────────
st.title("🔢 Shannon Entropy")
st.subheader("Information Theory × NSE Finance")

st.markdown(
    """
    **Shannon entropy** is the foundational quantity of information theory: the
    average number of bits required to encode the outcome of a random variable.
    In financial markets, entropy measures the *uncertainty* embedded in a price
    process — high entropy signals randomness and efficient markets, while low
    entropy signals structure, predictability, or thin liquidity.
    """
)

# ── Core formula ───────────────────────────────────────────────────────────
st.markdown("### Core Formula")
st.latex(r"H(X) = -\sum_{x \in \mathcal{X}} p(x)\,\log_2 p(x) \quad [\text{bits}]")

st.markdown(
    """
    where $p(x)$ is the probability mass function of the discrete random
    variable $X$ over alphabet $\\mathcal{X}$.  The convention
    $0 \\cdot \\log_2 0 := 0$ handles zero-probability outcomes.
    """
)

# ── Navigation ─────────────────────────────────────────────────────────────
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📐 Theory Page")
    st.markdown(
        "Interactive exploration of the binary entropy function, uniform "
        "distributions, and the intuition behind H(X). Sliders let you "
        "adjust probabilities and watch entropy change in real time."
    )
with col2:
    st.markdown("#### 📈 Finance Page")
    st.markdown(
        "Rolling entropy computed on NIFTY 50 daily returns. Includes "
        "an order-book entropy simulator, intraday entropy vs volatility "
        "visualisation, and a simple entropy-threshold trading backtest."
    )

st.divider()

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Shannon Entropy")
    st.markdown("**Information Theory × Finance**")
    st.divider()
    st.markdown(
        "Use the pages in the sidebar to navigate between the **Theory** "
        "and **Finance** modules."
    )
    st.divider()
    st.markdown(
        "**Author:** [Pranava BA](https://github.com/pranava-ba)  \n"
        "**Series:** [information-theory-finance](https://github.com/information-theory-finance)"
    )
    st.caption("v0.1.0 · MIT License")
