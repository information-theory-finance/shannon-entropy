"""
Shannon Entropy — Information Theory × NSE Finance
app.py: Landing / home page.
"""

import streamlit as st

st.set_page_config(
    page_title="Shannon Entropy · ITF",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Shannon Entropy")
st.caption("Information Theory × NSE Finance · [information-theory-finance](https://github.com/information-theory-finance)")

st.markdown(
    """
Shannon entropy quantifies the **average uncertainty** in a random variable.
Given a discrete distribution $p_1, p_2, \\ldots, p_n$, it measures how many
bits are needed on average to encode an outcome — or equivalently, how
unpredictable the variable is.
"""
)

st.latex(r"H(X) = -\sum_{i=1}^{n} p(x_i) \, \log_2 \, p(x_i)")

st.markdown(
    """
In finance, entropy applied to the distribution of asset returns captures
something correlation and variance cannot: the **shape** of uncertainty.
A highly leptokurtic distribution and a uniform distribution can have identical
variance but very different entropy.
"""
)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Theory.py", label="📐 Theory — interactive concept explorer", icon="📐")
    st.caption("PMF visualisation, entropy as a function of distribution spread, synthetic data.")
with col2:
    st.page_link("pages/2_Finance.py", label="📈 Finance — NSE application", icon="📈")
    st.caption("Rolling entropy of NSE log returns. NIFTY 50 and GOLDBEES daily data, self-updating.")

st.divider()
st.caption("Data: NSE India via yfinance · Stored locally in DuckDB · Auto-updated daily")
st.caption("Part of the [Information Theory × Finance](https://github.com/information-theory-finance) series · Pranava BA · Chennai")
