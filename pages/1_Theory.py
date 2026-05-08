# pages/1_Theory.py — Theory: Shannon Entropy from first principles
# Author: Pranava BA

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.math_core import (
    shannon_entropy, max_entropy, normalised_entropy,
    bernoulli_entropy, bernoulli_entropy_curve, uniform_entropy,
)
from utils.theme import (
    PAGE_CSS, AMBER, AMBER_LIGHT, BLUE_ACCENT, GREEN_UP, RED_DOWN,
    TEXT_PRIMARY, NAVY_DARKEST, NAVY_DARK, NAVY_MID, BORDER,
    SLATE_LIGHT, SLATE_MID, plotly_layout,
)

st.set_page_config(page_title="Theory — Shannon Entropy", layout="wide")
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.4rem 0 0.8rem'>
        <div style='font-size:1rem;font-weight:700;color:#e8edf5;'>Shannon Entropy</div>
        <div style='font-size:0.7rem;color:#f5a623;letter-spacing:0.1em;text-transform:uppercase;margin-top:3px;'>
            Theory
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='sb-eyebrow'>Log base</div>", unsafe_allow_html=True)
    log_base = st.selectbox(
        "", options=[2, float(np.e), 10],
        format_func=lambda b: {2: "2  →  bits", float(np.e): "e  →  nats", 10: "10 →  hartleys"}[b],
        label_visibility="collapsed",
    )
    unit = {2: "bits", float(np.e): "nats", 10: "hartleys"}[log_base]
    st.divider()
    st.page_link("app.py", label="← Back to Home", use_container_width=True)
    st.page_link("pages/2_Finance.py", label="Finance →", use_container_width=True)

# ── Page header ────────────────────────────────────────────────────────────
st.markdown("""
<div class='page-hero'>
    <div class='page-hero-eyebrow'>Module 1 · Mathematics</div>
    <div class='page-hero-title'>Theory of Shannon Entropy</div>
    <p class='page-hero-body'>
        A derivation of H(X) from first principles, starting from the notion of
        surprise, through the binary entropy function, to the key properties that
        make entropy the right measure of uncertainty in both coding theory and
        financial markets.
    </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — From Surprise to Entropy
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 1</div>
<div class='section-title'>From Surprise to Entropy</div>
""", unsafe_allow_html=True)

col_math, col_chart = st.columns([1, 1], gap="large")

with col_math:
    st.markdown("""
    <div class='info-card'>
        <p>
            The <em>surprise</em> (or self-information) of observing outcome x is defined as:<br/><br/>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"I(x) \;=\; -\log_2\,p(x) \quad [\text{bits}]")
    st.markdown("""
    <div class='info-card' style='margin-top:0.8rem;'>
        <p>
            Three axioms pin down this definition uniquely:<br/>
            <em>1.</em> Certain events carry zero surprise: I(1) = 0.<br/>
            <em>2.</em> Rarer events are more surprising: p↓ ⟹ I↑.<br/>
            <em>3.</em> Independent events add: I(p·q) = I(p) + I(q), forcing log.
            <br/><br/>
            <em>Shannon entropy</em> is simply the expected surprise over the
            entire distribution:
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"H(X) \;=\; \mathbb{E}[\,I(X)\,] \;=\; -\sum_{x \in \mathcal{X}} p(x)\log_2 p(x)")
    st.markdown("""
    <div class='info-card' style='margin-top:0.8rem;'>
        <p>
            <em>Coding interpretation:</em> H(X) is the minimum average
            code-length (in bits) achievable by any uniquely decodable code
            for X — Shannon's source coding theorem.
            A fair coin gives H = 1 bit. A fair die gives H = log₂ 6 ≈ 2.585 bits.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    # Self-information curve
    ps = np.linspace(1e-4, 1 - 1e-4, 400)
    surprise = -np.log(ps) / np.log(log_base)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ps, y=surprise, mode="lines",
        line=dict(color=AMBER, width=2.5),
        name=f"I(x) = −log_{int(log_base) if log_base != np.e else 'e'} p",
    ))
    fig.update_layout(
        **plotly_layout(
            title=f"Surprise I(x) = −log p  [{unit}]",
            x_title="p(x)",
            y_title=f"I(x)  [{unit}]",
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "<p style='color:#5a6e8a;font-size:0.8rem;text-align:center;margin-top:-0.5rem;'>"
        "Surprise diverges as p→0 (very rare event = enormous information content)."
        "</p>", unsafe_allow_html=True,
    )

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — Binary Entropy Function
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 2</div>
<div class='section-title'>The Binary Entropy Function H<sub>b</sub>(p)</div>
""", unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown("""
    <div class='info-card'>
        <p>
            For a Bernoulli(p) variable — a biased coin — the alphabet is {0,1}
            and entropy collapses to:
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"H_b(p) \;=\; -p\log_2 p \;-\; (1-p)\log_2(1-p)")
    st.markdown("""
    <div class='info-card' style='margin-top:0.8rem;'>
        <p>
            <em>p = 0 or 1:</em> certain outcome, H_b = 0 bits.<br/>
            <em>p = 0.5:</em> maximum uncertainty, H_b = 1 bit — exactly
            one question suffices on average.<br/><br/>
            The curve is symmetric around p = 0.5 and strictly concave —
            any mixture of two distributions has higher entropy than either alone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    p_sel = st.slider("Highlight p =", 0.01, 0.99, 0.50, 0.01)
    h_sel = bernoulli_entropy(p_sel, base=log_base)
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H_b({p_sel:.2f})</div>
            <div class='stat-pill-val'>{h_sel:.4f} {unit}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H_max (p=0.5)</div>
            <div class='stat-pill-val'>{bernoulli_entropy(0.5, log_base):.4f} {unit}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H / H_max</div>
            <div class='stat-pill-val'>{h_sel / bernoulli_entropy(0.5, log_base):.3f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    ps_curve, hs_curve = bernoulli_entropy_curve(n_points=400, base=log_base)
    h_at_sel = bernoulli_entropy(p_sel, base=log_base)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=ps_curve, y=hs_curve, mode="lines",
        line=dict(color=AMBER, width=2.5), name="H_b(p)",
    ))
    fig2.add_vline(x=p_sel, line=dict(color=BLUE_ACCENT, dash="dot", width=1.2))
    fig2.add_hline(y=h_at_sel, line=dict(color=BLUE_ACCENT, dash="dot", width=1.2))
    fig2.add_trace(go.Scatter(
        x=[p_sel], y=[h_at_sel], mode="markers",
        marker=dict(color=BLUE_ACCENT, size=11, symbol="circle"),
        name=f"p = {p_sel:.2f}",
    ))
    fig2.update_layout(**plotly_layout(
        title=f"Binary Entropy H_b(p)  [{unit}]",
        x_title="p",
        y_title=f"H_b(p)  [{unit}]",
    ))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 — Uniform Distribution & Scaling
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 3</div>
<div class='section-title'>Uniform Distribution — H = log n</div>
""", unsafe_allow_html=True)

col_u1, col_u2 = st.columns([1, 1], gap="large")

with col_u1:
    st.markdown("""
    <div class='info-card'>
        <p>
            When all n outcomes are equally likely p(x) = 1/n, the entropy
            formula simplifies to:
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"H(\text{Uniform}(n)) \;=\; \log_2\,n")
    st.markdown("""
    <div class='info-card' style='margin-top:0.8rem;'>
        <p>
            This is also the <em>maximum entropy</em> for any distribution
            over n outcomes — no distribution over n symbols can exceed log n
            bits. The uniform distribution achieves this bound exactly because
            it spreads mass as evenly as possible.<br/><br/>
            <em>Practical interpretation:</em> a NIFTY 50 return distribution
            with entropy near log(n_bins) bits is close to uniform — returns
            are nearly unpredictable. A lower value signals concentration in
            a few return bins.
        </p>
    </div>
    """, unsafe_allow_html=True)

    n_sel = st.slider("Select n", 1, 50, 8, 1, key="unif_n")
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H(Uniform({n_sel}))</div>
            <div class='stat-pill-val'>{uniform_entropy(n_sel, log_base):.4f} {unit}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>Each p(x)</div>
            <div class='stat-pill-val'>{1/max(n_sel,1):.4f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_u2:
    ns = np.arange(1, 51)
    h_uniform = [uniform_entropy(int(n), log_base) for n in ns]

    fig3 = go.Figure()
    # Theoretical log₂n line
    log_line = np.log(ns) / np.log(log_base)
    fig3.add_trace(go.Scatter(
        x=ns, y=log_line, mode="lines",
        line=dict(color=SLATE_MID, dash="dot", width=1.5),
        name=f"log_{int(log_base) if log_base != np.e else 'e'}(n)",
    ))
    fig3.add_trace(go.Bar(
        x=ns, y=h_uniform,
        marker_color=[AMBER if int(n) == n_sel else "#1c2640" for n in ns],
        name="H (uniform)",
    ))
    fig3.add_trace(go.Scatter(
        x=[n_sel], y=[uniform_entropy(n_sel, log_base)],
        mode="markers", marker=dict(color=BLUE_ACCENT, size=10),
        name=f"n = {n_sel}", showlegend=False,
    ))
    fig3.update_layout(**plotly_layout(
        title="Entropy of Uniform(n) vs Alphabet Size",
        x_title="n",
        y_title=f"H  [{unit}]",
    ))
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4 — Custom PMF
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 4</div>
<div class='section-title'>Custom PMF Builder</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='info-card' style='margin-bottom:1rem;'>
    <p>
        Drag the weight sliders below to define any distribution over 2–8 outcomes.
        Weights are normalised automatically. Watch how concentrating mass on fewer
        outcomes drives entropy toward zero, while spreading it uniformly drives entropy
        toward the maximum log₂(n).
    </p>
</div>
""", unsafe_allow_html=True)

c_ctrl, c_chart = st.columns([1, 1], gap="large")

with c_ctrl:
    n_out = st.slider("Number of outcomes", 2, 8, 4, key="pmf_n")
    ws = []
    for i in range(n_out):
        default = 1.0 if i < 2 else (0.5 if i < 4 else 0.2)
        ws.append(st.slider(f"w_{i+1}", 0.0, 10.0, default, 0.1, key=f"pmf_w{i}"))

    ws = np.array(ws, dtype=float)
    if ws.sum() == 0:
        ws = np.ones(n_out)
    pmf = ws / ws.sum()

    h_custom = shannon_entropy(pmf, base=log_base)
    h_max_c  = max_entropy(n_out, log_base)
    h_norm_c = normalised_entropy(pmf, log_base)

    st.markdown(f"""
    <div class='stat-row' style='margin-top:0.8rem;'>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H(X)</div>
            <div class='stat-pill-val'>{h_custom:.4f} {unit}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H_max</div>
            <div class='stat-pill-val'>{h_max_c:.4f} {unit}</div>
        </div>
        <div class='stat-pill'>
            <div class='stat-pill-label'>H / H_max</div>
            <div class='stat-pill-val'>{h_norm_c:.3f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_chart:
    outcome_labels = [f"x{i+1}" for i in range(n_out)]
    uniform_ref    = [1 / n_out] * n_out

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=outcome_labels, y=pmf,
        marker_color=AMBER, name="p(x)",
        text=[f"{v:.3f}" for v in pmf],
        textposition="outside",
        textfont=dict(color=TEXT_PRIMARY, size=10),
    ))
    fig4.add_trace(go.Scatter(
        x=outcome_labels, y=uniform_ref,
        mode="lines+markers",
        line=dict(color=BLUE_ACCENT, dash="dash", width=1.5),
        marker=dict(size=6),
        name=f"Uniform (1/{n_out} = {1/n_out:.3f})",
    ))
    fig4.update_layout(
        **plotly_layout(title="Custom PMF  vs  Uniform Reference", x_title="Outcome", y_title="Probability"),
    )
    fig4.update_yaxes(range=[0, max(max(pmf) * 1.25, 1.0 / n_out * 1.5)])
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5 — Properties
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-eyebrow'>Section 5</div>
<div class='section-title'>Key Properties</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='prop-grid'>
    <div class='prop-card'>
        <div class='prop-title'>Non-negativity</div>
        <p class='prop-body'><span class='prop-math'>H(X) ≥ 0</span><br/>
        Equality iff X is deterministic. You cannot have negative average information.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Maximum</div>
        <p class='prop-body'><span class='prop-math'>H(X) ≤ log₂|𝒳|</span><br/>
        Tight bound achieved by the uniform distribution over all outcomes.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Concavity</div>
        <p class='prop-body'>H(λp + (1−λ)q) ≥ λH(p) + (1−λ)H(q)<br/>
        Averaging/mixing probability distributions increases entropy.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Chain Rule</div>
        <p class='prop-body'><span class='prop-math'>H(X,Y) = H(X) + H(Y|X)</span><br/>
        Joint entropy equals the marginal plus the average conditional.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Data Processing</div>
        <p class='prop-body'><span class='prop-math'>H(f(X)) ≤ H(X)</span><br/>
        Deterministic functions can only reduce or preserve entropy, never increase it.</p>
    </div>
    <div class='prop-card'>
        <div class='prop-title'>Subadditivity</div>
        <p class='prop-body'><span class='prop-math'>H(X,Y) ≤ H(X) + H(Y)</span><br/>
        With equality iff X and Y are independent — dependence reduces joint entropy.</p>
    </div>
</div>
""", unsafe_allow_html=True)
