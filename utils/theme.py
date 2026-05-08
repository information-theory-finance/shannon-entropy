# utils/theme.py
# Single source of truth for all colors and Plotly layout.
# Part of the information-theory-finance series.
# Author: Pranava BA

# ── Palette (dark theme) ───────────────────────────────────────────────────
NAVY_DARKEST  = "#0a0e1a"
NAVY_DARK     = "#0f1629"
NAVY_MID      = "#151d33"
NAVY_LIGHT    = "#1c2640"
SLATE_DARK    = "#2a3548"
SLATE_MID     = "#3d4d66"
SLATE_LIGHT   = "#5a6e8a"
AMBER         = "#f5a623"
AMBER_LIGHT   = "#fbbf45"
GREEN_UP      = "#a3be8c"
RED_DOWN      = "#f08030"
BLUE_ACCENT   = "#88c0d0"
TEXT_PRIMARY  = "#e8edf5"
TEXT_MUTED    = "#5a6e8a"
BORDER        = "#1c2640"


# ── Plotly base layout ─────────────────────────────────────────────────────
def plotly_layout(title: str = "", x_title: str = "", y_title: str = "") -> dict:
    """Return a base Plotly layout dict consistent with the app theme."""
    return dict(
        title=dict(text=title, font=dict(color=TEXT_PRIMARY, size=16)),
        paper_bgcolor=NAVY_DARKEST,
        plot_bgcolor=NAVY_DARK,
        font=dict(color=TEXT_PRIMARY, family="JetBrains Mono, monospace", size=12),
        xaxis=dict(
            title=x_title,
            gridcolor=BORDER,
            zerolinecolor=BORDER,
            color=SLATE_LIGHT,
        ),
        yaxis=dict(
            title=y_title,
            gridcolor=BORDER,
            zerolinecolor=BORDER,
            color=SLATE_LIGHT,
        ),
        legend=dict(
            bgcolor=NAVY_MID,
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=SLATE_LIGHT),
        ),
        margin=dict(l=60, r=30, t=60, b=60),
    )


# ── Shared Streamlit CSS injected on every page via st.markdown() ──────────
PAGE_CSS = """
<style>
/* ── Page header card ── */
.page-hero {
    background: linear-gradient(135deg, #0f1629 0%, #1c2640 60%, #0f1629 100%);
    border: 1px solid #2a3548;
    border-left: 4px solid #f5a623;
    border-radius: 10px;
    padding: 1.8rem 2.2rem 1.5rem;
    margin-bottom: 2rem;
}
.page-hero-eyebrow {
    font-size: 0.7rem; color: #f5a623; letter-spacing: 0.14em;
    text-transform: uppercase; font-weight: 700; margin-bottom: 0.35rem;
}
.page-hero-title {
    font-size: 1.75rem; font-weight: 700; color: #e8edf5;
    letter-spacing: -0.01em; margin: 0 0 0.5rem;
}
.page-hero-body {
    color: #8a9ab8; font-size: 0.92rem; line-height: 1.7;
    max-width: 860px; margin: 0;
}

/* ── Section header ── */
.section-eyebrow {
    font-size: 0.68rem; color: #f5a623; letter-spacing: 0.14em;
    text-transform: uppercase; font-weight: 700;
    margin: 0 0 0.3rem;
}
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #e8edf5;
    margin: 0 0 0.9rem;
}

/* ── Info / callout card ── */
.info-card {
    background: #0f1629; border: 1px solid #2a3548;
    border-radius: 8px; padding: 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
}
.info-card p  { color: #b0bccc; font-size: 0.9rem; line-height: 1.7; margin: 0; }
.info-card em { color: #fbbf45; font-style: normal; }

/* ── Stat pills row ── */
.stat-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 1.4rem; }
.stat-pill {
    background: #0f1629; border: 1px solid #2a3548; border-radius: 6px;
    padding: 0.55rem 1rem;
}
.stat-pill-label {
    font-size: 0.62rem; color: #5a6e8a; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.15rem;
}
.stat-pill-val {
    font-size: 0.92rem; font-weight: 700; color: #fbbf45;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Property grid ── */
.prop-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 0.8rem; }
.prop-card {
    background: #0f1629; border: 1px solid #2a3548;
    border-radius: 8px; padding: 1rem 1.15rem;
}
.prop-title {
    font-size: 0.68rem; color: #f5a623; letter-spacing: 0.1em;
    text-transform: uppercase; font-weight: 700; margin-bottom: 0.35rem;
}
.prop-body { color: #b0bccc; font-size: 0.875rem; line-height: 1.55; margin: 0; }
.prop-math { color: #fbbf45; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }

/* ── Sidebar ── */
.sb-eyebrow {
    font-size: 0.62rem; color: #5a6e8a; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 0.2rem;
}
.sb-value { font-size: 0.88rem; color: #e8edf5; margin-bottom: 0.9rem; }
.sb-link  { color: #f5a623 !important; text-decoration: none; font-size: 0.88rem; }
.sb-link:hover { text-decoration: underline; }

/* ── Page-link button ── */
div[data-testid="stPageLink"] > a {
    display: block !important;
    background: transparent !important;
    border: 1px solid #f5a623 !important;
    border-radius: 6px !important;
    color: #f5a623 !important;
    text-align: center !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    padding: 0.45rem 1rem !important;
    margin-top: 0.9rem;
    transition: background 0.15s, color 0.15s;
}
div[data-testid="stPageLink"] > a:hover {
    background: #f5a623 !important;
    color: #0a0e1a !important;
}

/* ── Divider spacing ── */
hr { border-color: #2a3548 !important; margin: 1.8rem 0 !important; }
</style>
"""
