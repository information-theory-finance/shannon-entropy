<div align="center">

<pre>
 ____  _   _    _    _   _ _   _  ___  _   _
/ ___|| | | |  / \  | \ | | \ | |/ _ \| \ | |
\___ \| |_| | / _ \ |  \| |  \| | | | |  \| |
 ___) |  _  |/ ___ \| |\  | |\  | |_| | |\  |
|____/|_| |_/_/ \___|_|_\_|_|_\_|\___/|_| \_|

 ___ _   _ _____ ____   ___  ____  __   __
|_ _| \ | |_   _|  _ \ / _ \|  _ \ \ \ / /
 | ||  \| | | | | |_) | | | | |_) | \ V /
 | || |\  | | | |  _ <| |_| |  __/   | |
|___|_| \_| |_| |_| \_\\___/|_|      |_|
</pre>

**Shannon Entropy — Information Theory × NSE Finance**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![DuckDB](https://img.shields.io/badge/DuckDB-Latest-FFF000?style=flat-square)](https://duckdb.org)
[![NSE](https://img.shields.io/badge/Data-NSE%20India-0055A5?style=flat-square)](https://nseindia.com)
[![License](https://img.shields.io/badge/License-MIT-8B949E?style=flat-square)](LICENSE.md)

[![Docs](https://img.shields.io/badge/📖%20Documentation-shannon--entropy.readthedocs.io-1ABC9C?style=for-the-badge&logo=readthedocs&logoColor=white)](https://shannon-entropy.readthedocs.io)
[![Live Demo](https://img.shields.io/badge/▶%20Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://shannon-entropy.streamlit.app)

<br/>

*Measuring market uncertainty one bit at a time — from the binary entropy curve to NIFTY 50 rolling entropy and order-book liquidity analysis.*

</div>

<br/>

---

## Run Locally

<details>
<summary><strong>🐍 Run from Source</strong></summary>
<br/>

```bash
git clone https://github.com/information-theory-finance/shannon-entropy.git
cd shannon-entropy
pip install -r requirements.txt
streamlit run app.py
```

Data is fetched automatically from Yahoo Finance on first run and cached in `data/nse.duckdb`.

</details>

---

## What This App Shows

| Page | Content |
|------|---------|
| **Theory** | Interactive binary entropy curve, uniform distribution explorer, and custom PMF builder with live H(X) readout — all with configurable log base |
| **Finance** | Rolling Shannon entropy of NIFTY 50 log-returns, entropy vs volatility scatter, synthetic order-book entropy simulation, and an entropy-threshold backtest P&L curve |

---

## Screenshots

<div align="center">

<table>
  <tr>
    <td><img src="images/i1.png" width="100%" /></td>
    <td><img src="images/i2.png" width="100%" /></td>
  </tr>
  <tr>
    <td><img src="images/i3.png" width="100%" /></td>
    <td><img src="images/i4.png" width="100%" /></td>
  </tr>
</table>

</div>

---

## Core Formula

$$H(X) = -\sum_{x \in \mathcal{X}} p(x)\,\log_2 p(x) \quad [\text{bits}]$$

---

## Features

<details>
<summary><strong>📐 Theory Page</strong></summary>
<br/>

- **Binary entropy curve** — plot $H_b(p)$ vs $p$ with a draggable slider; switch between bits, nats, and hartleys
- **Uniform distribution** — visualise $H = \log_2 n$ as alphabet size grows from 1 to 100
- **Custom PMF builder** — define up to 8 outcomes with weight sliders; entropy, H_max, and normalised entropy update live
- **Distribution comparison** — bar chart comparing entropy across Bernoulli, uniform, and skewed PMFs
- All formulas rendered via `st.latex()`; implementation shown with `st.code()`

</details>

<details>
<summary><strong>📈 Finance Page</strong></summary>
<br/>

- **Rolling entropy** — configurable window (20–120 days) and bin count (5–40) applied to NIFTY 50 log-returns
- **Three-panel chart** — closing price / rolling entropy / rolling annualised volatility on a shared time axis
- **Entropy vs volatility scatter** — year-coloured markers with Pearson correlation readout
- **Empirical PMF** — bar chart of the return distribution in the most recent window
- **Order-book simulator** — synthetic Level-2 book with liquid / illiquid / one-sided regimes; bid and ask entropy displayed separately
- **Entropy-threshold backtest** — cumulative return curve for the signal vs buy-and-hold, plus a summary stats table (total return, Sharpe, max drawdown, win rate, days in market)

</details>

<details>
<summary><strong>🔄 Data</strong></summary>
<br/>

- **Source:** Yahoo Finance via `yfinance` (adjusted closes, `auto_adjust=True`)
- **Ticker:** `^NSEI` (NIFTY 50 Index)
- **Cache:** DuckDB at `data/nse.duckdb`; incremental update on each run, full refresh every 24 h on Streamlit Cloud
- **Start date:** 2018-01-01 (≈ 1,800 trading sessions)

</details>

---

## Data Notes

> OHLCV data for `^NSEI` is sourced from Yahoo Finance via `yfinance` with automatic split and dividend adjustment. Data is cached locally in a DuckDB database (`data/nse.duckdb`) and refreshed incrementally — only the gap between the last stored date and today is re-fetched on each run. The `data/` directory is excluded from version control. Volume is always zero for index symbols in yfinance and is not used in any calculation. Historical coverage begins 2018-01-01.

---

## Part of

> This project is part of the **Information Theory × Finance** series by
> [Pranava BA](https://github.com/pranava-ba).
> [View all projects →](https://github.com/information-theory-finance)

---

<div align="center">

**Pranava BA** · Chennai, India · © 2025–2026

</div>
