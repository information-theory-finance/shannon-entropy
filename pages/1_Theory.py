# pages/1_Theory.py
# Information Theory × Finance — Shannon Entropy
# Theory page: math + interactive visualisations using synthetic data.
# Author: Pranava BA

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.math_core import (
    shannon_entropy,
    max_entropy,
    normalised_entropy,
    bernoulli_entropy,
    bernoulli_entropy_curve,
    uniform_entropy,
    entropy_of_custom_pmf,
)
from utils.theme import (
    AMBER, BLUE_ACCENT, GREEN_UP, RED_DOWN,
    TEXT_PRIMARY, NAVY_DARKEST, NAVY_DARK, NAVY_MID, BORDER, SLATE_LIGHT,
    plotly_layout,
)

st.set_page_config(page_title="Theory — Shannon Entropy", layout="wide")

st.title("📐 Shannon Entropy — Theory")
st.markdown("---")

# ── Two-column layout ──────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# ══════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Math explanation
# ══════════════════════════════════════════════════════════════════════════
with left:
    st.markdown("### Definition")
    st.markdown(
        "For a discrete random variable $X$ taking values in $\\mathcal{X}$ "
        "with PMF $p$, Shannon entropy is:"
    )
    st.latex(r"H(X) = -\sum_{x \in \mathcal{X}} p(x)\,\log_b\,p(x)")
    st.markdown(
        "The choice of base $b$ fixes the unit: $b=2$ gives **bits**, "
        "$b=e$ gives **nats**, $b=10$ gives **hartleys**."
    )

    st.markdown("### Binary Entropy Function")
    st.markdown(
        "For a Bernoulli($p$) variable (coin flip), the formula collapses to:"
    )
    st.latex(r"H_b(p) = -p\log_2 p - (1-p)\log_2(1-p)")
    st.markdown(
        "This is maximised at $p = 0.5$ (1 bit) and equals 0 at $p \\in \\{0,1\\}$ "
        "(certainty)."
    )

    st.markdown("### Key Properties")
    st.markdown(
        "**Non-negativity:** $H(X) \\geq 0$, with equality iff $X$ is deterministic.  \n"
        "**Maximum:** $H(X) \\leq \\log_b |\\mathcal{X}|$, achieved by the uniform PMF.  \n"
        "**Concavity:** $H$ is a concave function of the PMF.  \n"
        "**Chain rule:** $H(X,Y) = H(X) + H(Y|X)$.  \n"
        "**Data processing:** $H(f(X)) \\leq H(X)$ for any function $f$."
    )

    st.markdown("### Uniform Distribution")
    st.markdown(
        "When all $n$ outcomes are equally likely, $p(x) = 1/n$ and:"
    )
    st.latex(r"H(X) = \log_b\,n")

    st.markdown("### Implementation (from scratch)")
    st.code(
        "import numpy as np\n\n"
        "def shannon_entropy(probs, base=2.0):\n"
        "    probs = np.asarray(probs, dtype=float)\n"
        "    probs = probs[probs > 0]          # drop zeros\n"
        "    probs /= probs.sum()              # normalise\n"
        "    return -np.sum(probs * np.log(probs) / np.log(base))",
        language="python",
    )

    st.markdown("### Worked Example")
    st.markdown(
        "Roll a fair four-sided die: $p = [0.25, 0.25, 0.25, 0.25]$."
    )
    st.latex(r"H = -4 \times 0.25\log_2(0.25) = -4 \times 0.25 \times (-2) = 2\text{ bits}")
    h_example = uniform_entropy(4)
    st.metric("Computed H (4-sided die)", f"{h_example:.4f} bits")

# ══════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Interactive visualisations
# ══════════════════════════════════════════════════════════════════════════
with right:
    tab1, tab2, tab3 = st.tabs(
        ["🎲 Binary Entropy Curve", "🎯 Uniform Distribution", "🛠 Custom PMF"]
    )

    # ── Tab 1: Binary entropy curve ──────────────────────────────────────
    with tab1:
        st.markdown("#### H_b(p) vs p — Bernoulli Variable")
        log_base = st.selectbox(
            "Logarithm base", options=[2, np.e, 10],
            format_func=lambda b: {2: "2 (bits)", np.e: "e (nats)", 10: "10 (hartleys)"}[b],
            key="tab1_base",
        )
        p_highlight = st.slider(
            "Highlight p =", 0.01, 0.99, 0.5, 0.01, key="tab1_p"
        )

        ps, hs = bernoulli_entropy_curve(n_points=400, base=log_base)
        h_at_p = bernoulli_entropy(p_highlight, base=log_base)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ps, y=hs, mode="lines",
            line=dict(color=AMBER, width=2.5),
            name="H_b(p)",
        ))
        fig.add_trace(go.Scatter(
            x=[p_highlight], y=[h_at_p],
            mode="markers",
            marker=dict(color=BLUE_ACCENT, size=12, symbol="circle"),
            name=f"p = {p_highlight:.2f}",
        ))
        fig.add_vline(x=p_highlight, line=dict(color=BLUE_ACCENT, dash="dot", width=1))
        fig.add_hline(y=h_at_p, line=dict(color=BLUE_ACCENT, dash="dot", width=1))

        unit = {2: "bits", np.e: "nats", 10: "hartleys"}[log_base]
        fig.update_layout(
            **plotly_layout(
                title=f"Binary Entropy Curve (base = {log_base if log_base != np.e else 'e'})",
                x_title="p",
                y_title=f"H_b(p)  [{unit}]",
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.metric(f"H_b({p_highlight:.2f})", f"{h_at_p:.4f} {unit}")

    # ── Tab 2: Uniform distribution entropy ──────────────────────────────
    with tab2:
        st.markdown("#### H(X) = log₂(n) for Uniform Distribution")
        n_max = st.slider("Maximum n (outcomes)", 2, 100, 20, key="tab2_n")

        ns = np.arange(1, n_max + 1)
        hs_uniform = [uniform_entropy(int(n)) for n in ns]

        n_sel = st.slider("Selected n", 1, n_max, min(n_max, 8), key="tab2_sel")

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=ns, y=hs_uniform,
            marker_color=[AMBER if n == n_sel else SLATE_LIGHT for n in ns],
            name="H (uniform)",
        ))
        fig2.update_layout(
            **plotly_layout(
                title="Entropy of Uniform Distribution vs Alphabet Size",
                x_title="n (number of outcomes)",
                y_title="H(X)  [bits]",
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.metric(f"H(Uniform({n_sel}))", f"{uniform_entropy(n_sel):.4f} bits")

    # ── Tab 3: Custom PMF ─────────────────────────────────────────────────
    with tab3:
        st.markdown("#### Custom Probability Mass Function")
        st.markdown(
            "Adjust the unnormalised weights below. The app normalises them "
            "automatically and computes H(X)."
        )
        n_outcomes = st.slider("Number of outcomes", 2, 8, 4, key="tab3_n")

        weights = []
        cols = st.columns(n_outcomes)
        for i, col in enumerate(cols):
            w = col.slider(f"w_{i+1}", 0.0, 10.0, 1.0, 0.1, key=f"tab3_w{i}")
            weights.append(w)

        weights = np.array(weights, dtype=float)
        total = weights.sum()
        if total == 0:
            st.warning("All weights are zero — assigning uniform distribution.")
            weights = np.ones(n_outcomes)
        pmf = weights / weights.sum()

        h_custom = entropy_of_custom_pmf(weights.tolist())
        h_max_custom = max_entropy(n_outcomes)
        h_norm = normalised_entropy(pmf)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=[f"x_{i+1}" for i in range(n_outcomes)],
            y=pmf,
            marker_color=AMBER,
            name="p(x)",
        ))
        # Overlay uniform reference
        fig3.add_trace(go.Scatter(
            x=[f"x_{i+1}" for i in range(n_outcomes)],
            y=[1 / n_outcomes] * n_outcomes,
            mode="lines",
            line=dict(color=BLUE_ACCENT, dash="dash", width=1.5),
            name=f"Uniform (1/{n_outcomes})",
        ))
        fig3.update_layout(
            **plotly_layout(
                title="Custom PMF",
                x_title="Outcome",
                y_title="Probability",
            )
        )
        fig3.update_yaxes(range=[0, 1])
        st.plotly_chart(fig3, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("H(X)", f"{h_custom:.4f} bits")
        m2.metric("H_max", f"{h_max_custom:.4f} bits")
        m3.metric("H / H_max", f"{h_norm:.3f}")

st.divider()
st.markdown(
    "### Entropy Across Distributions — Summary Heatmap",
    help="Comparison of Shannon entropy for common PMFs.",
)

# ── Summary comparison chart ───────────────────────────────────────────────
dist_labels = ["Bernoulli(0.5)", "Bernoulli(0.1)", "Uniform(4)", "Uniform(8)",
               "Skewed(heavy)", "Uniform(16)", "Uniform(32)"]
dist_values = [
    bernoulli_entropy(0.5),
    bernoulli_entropy(0.1),
    uniform_entropy(4),
    uniform_entropy(8),
    shannon_entropy([0.5, 0.3, 0.15, 0.05]),
    uniform_entropy(16),
    uniform_entropy(32),
]

colors = [
    AMBER if v == max(dist_values) else (RED_DOWN if v == min(dist_values) else BLUE_ACCENT)
    for v in dist_values
]

fig_summary = go.Figure(go.Bar(
    x=dist_labels,
    y=dist_values,
    marker_color=colors,
    text=[f"{v:.3f} bits" for v in dist_values],
    textposition="outside",
    textfont=dict(color=TEXT_PRIMARY, size=11),
))
fig_summary.update_layout(
    **plotly_layout(
        title="Shannon Entropy Comparison Across Distributions",
        x_title="Distribution",
        y_title="H(X)  [bits]",
    )
)
fig_summary.update_yaxes(
    range=[0, max(dist_values) * 1.2],
    gridcolor=BORDER,
    zerolinecolor=BORDER,
    color=SLATE_LIGHT,
)
st.plotly_chart(fig_summary, use_container_width=True)
