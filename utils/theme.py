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
