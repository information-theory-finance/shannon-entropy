"""
Shannon Entropy — Theory Page
Interactive exploration of H(X) = -∑ p(x) log₂ p(x) on synthetic data.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.math_core import (
    entropy_from_data,
    max_entropy,
    shannon_entropy,
    synthetic_entropy_curve,
)
from utils.theme import (
    AMBER,
    AMBER_LIGHT,
    BLUE_ACCENT,
    BORDER,
    GREEN_UP,
    NAVY_DARK,
    NAVY_MID,
    RED_DOWN,
    SILVER_LIGHT,
    plotly_layout,
)

st.set_page_config(
    page_title="Theory · Shannon Entropy · ITF",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Shannon Entropy — Theory")
st.caption("Interactive exploration on synthetic data")

# ── Sidebar controls ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Parameters")
    distribution = st.selectbox(
        "Distribution",
        ["Normal", "Uniform", "Exponential", "Laplace"],
        index=0,
    )
    param_label = {
        "Normal": "Standard deviation σ",
        "Uniform": "Half-width a (Uniform[−a, a])",
        "Exponential": "Scale λ",
        "Laplace": "Scale b",
    }[distribution]
    param_value = st.slider(param_label, min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    bins = st.slider("Histogram bins (PMF resolution)", 10, 100, 50, step=5)
    n_samples = st.select_slider("Monte Carlo samples", [1_000, 5_000, 10_000, 50_000], value=10_000)
    log_base = st.selectbox("Entropy units", ["bits (base 2)", "nats (base e)", "hartleys (base 10)"], index=0)
    base = {"bits (base 2)": 2.0, "nats (base e)": np.e, "hartleys (base 10)": 10.0}[log_base]
    st.divider()
    st.caption("Changes apply immediately.")

# ── Generate synthetic data ───────────────────────────────────────────────────
rng = np.random.default_rng(42)
dist_map = {
    "Normal": rng.normal(0, param_value, n_samples),
    "Uniform": rng.uniform(-param_value, param_value, n_samples),
    "Exponential": rng.exponential(param_value, n_samples),
    "Laplace": rng.laplace(0, param_value, n_samples),
}
data = dist_map[distribution]
H = entropy_from_data(data, bins=bins, base=base)
H_max = max_entropy(bins, base=base)
unit = {"bits (base 2)": "bits", "nats (base e)": "nats", "hartleys (base 10)": "hartleys"}[log_base]

# ── Layout ───────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Definition")
    st.latex(r"H(X) = -\sum_{i=1}^{n} p(x_i) \, \log_b \, p(x_i)")
    st.markdown(
        f"""
**Key properties:**
- $H(X) \\geq 0$ always (entropy is non-negative)
- $H(X) = 0$ if and only if $X$ is deterministic (one outcome has $p = 1$)
- $H(X) \\leq \\log_b(n)$ — the uniform distribution maximises entropy
- Measured in **{unit}** when using base {base:.4g}

**Current configuration:**

| Quantity | Value |
|----------|-------|
| Distribution | {distribution}(param={param_value}) |
| Estimated H(X) | **{H:.4f} {unit}** |
| Maximum H(n={bins} bins) | {H_max:.4f} {unit} |
| Relative entropy | {H/H_max*100:.1f}% of maximum |
"""
    )

    st.subheader("Entropy vs. Spread")
    st.markdown("How entropy changes as the distribution parameter grows:")
    param_range = np.linspace(0.1, 5.0, 40)
    ent_curve = synthetic_entropy_curve(
        distribution.lower(), param_range, bins=bins, n_samples=5_000, base=base
    )
    fig_curve = go.Figure()
    fig_curve.add_trace(
        go.Scatter(
            x=param_range,
            y=ent_curve,
            mode="lines",
            line=dict(color=AMBER, width=2),
            name="H(X)",
        )
    )
    fig_curve.add_vline(
        x=param_value,
        line=dict(color=BLUE_ACCENT, dash="dash", width=1.5),
        annotation_text=f"current ({param_value})",
        annotation_font_color=BLUE_ACCENT,
    )
    fig_curve.update_layout(
        **plotly_layout(
            title=f"Entropy vs. {param_label}",
            x_title=param_label,
            y_title=f"H(X) [{unit}]",
        )
    )
    st.plotly_chart(fig_curve, use_container_width=True)

with right:
    st.subheader("Distribution & PMF")

    counts, bin_edges = np.histogram(data, bins=bins)
    bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    pmf = counts / counts.sum()

    fig_pmf = go.Figure()
    fig_pmf.add_trace(
        go.Bar(
            x=bin_centres,
            y=pmf,
            marker_color=AMBER,
            marker_line_color=NAVY_DARK,
            marker_line_width=0.5,
            name="PMF estimate",
        )
    )
    fig_pmf.update_layout(
        **plotly_layout(
            title=f"{distribution}(param={param_value}) — PMF estimate ({bins} bins)",
            x_title="x",
            y_title="p(x)",
        )
    )
    st.plotly_chart(fig_pmf, use_container_width=True)

    # Entropy gauge
    st.subheader("Entropy Gauge")
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=H,
            delta={"reference": H_max, "suffix": f" {unit}", "valueformat": ".3f"},
            number={"suffix": f" {unit}", "valueformat": ".3f", "font": {"color": AMBER}},
            gauge={
                "axis": {"range": [0, H_max], "tickcolor": SILVER_LIGHT},
                "bar": {"color": AMBER},
                "bgcolor": NAVY_MID,
                "bordercolor": BORDER,
                "steps": [
                    {"range": [0, H_max * 0.33], "color": NAVY_DARK},
                    {"range": [H_max * 0.33, H_max * 0.66], "color": NAVY_MID},
                    {"range": [H_max * 0.66, H_max], "color": "#1e3a5f"},
                ],
                "threshold": {
                    "line": {"color": GREEN_UP, "width": 2},
                    "thickness": 0.75,
                    "value": H_max,
                },
            },
            title={"text": f"H(X) vs Maximum ({H_max:.3f} {unit})", "font": {"color": SILVER_LIGHT}},
        )
    )
    fig_gauge.update_layout(paper_bgcolor=NAVY_DARK, font=dict(color=SILVER_LIGHT), height=280)
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()
st.caption("Entropy is estimated from the empirical PMF via histogram binning. Increase samples or bins for a more accurate estimate.")
