<div align="center">

<pre>
 _____ _   _ _   _ ___  _   _ _   _   _____  _   _ _____ ____   ___  ______   __
/ ____| | | | | | / _ \| \ | | \ | | | ____|| \ | |_   _|  _ \ / _ \|  _ \ \ / /
\___ \| |_| | |_| | | | |  \| |  \| | |  _|  |  \| | | | | |_) | | | | |_) \ V / 
 ___) |  _  |  _  | |_| | |\  | |\  | | |___ | |\  | | | |  _ <| |_| |  __/ | |  
|____/|_| |_|_| |_|\___/|_| \_|_| \_| |_____||_| \_| |_| |_| \_\\___/|_|    |_|  
</pre>

**Shannon Entropy — Information Theory × NSE Finance**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![DuckDB](https://img.shields.io/badge/DuckDB-Latest-FFF000?style=flat-square)](https://duckdb.org)
[![NSE](https://img.shields.io/badge/Data-NSE%20India-0055A5?style=flat-square)](https://nseindia.com)
[![License](https://img.shields.io/badge/License-MIT-8B949E?style=flat-square)](LICENSE.md)

[![Docs](https://img.shields.io/badge/📖%20Documentation-RTD-1ABC9C?style=for-the-badge&logo=readthedocs&logoColor=white)](#)
[![Live Demo](https://img.shields.io/badge/▶%20Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)

<br/>

*Measuring uncertainty in NSE return distributions — a model-free alternative to variance.*

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

Data is fetched automatically from NSE via yfinance on first run and stored in `data/nse.duckdb`.

</details>

---

## What This App Shows

| Page | Content |
|------|---------|
| **Theory** | Interactive PMF visualiser, entropy vs. spread curve, entropy gauge — on synthetic data |
| **Finance** | Rolling Shannon entropy of NIFTY 50 and GOLDBEES.NS log returns, self-updating daily |

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

$$H(X) = -\sum_{i=1}^{n} p(x_i) \, \log_2 \, p(x_i)$$

---

## Features

<details>
<summary><strong>📐 Theory Page</strong></summary>
<br/>

- Select from four distribution families: Normal, Uniform, Exponential, Laplace
- Adjust the distribution parameter with a live slider
- View the empirical PMF histogram (configurable bins)
- See entropy as a fraction of maximum entropy via an interactive gauge
- Entropy vs. parameter curve showing how spread drives uncertainty

</details>

<details>
<summary><strong>📈 Finance Page</strong></summary>
<br/>

- Switch between NIFTY 50 (`^NSEI`) and Nippon Gold ETF (`GOLDBEES.NS`)
- Configurable rolling window (20–120 trading days) and bin count
- Price series and rolling entropy plotted on shared x-axis
- Full-sample return distribution with entropy estimate
- KPI row: current entropy, mean, max, min, latest return

</details>

<details>
<summary><strong>🔄 Data</strong></summary>
<br/>

- Source: NSE India via yfinance (adjusted close, EOD)
- Stored in a local DuckDB file (`data/nse.duckdb`) — not committed to the repo
- Self-updating: missing trading days are fetched automatically on app load
- Streamlit cache TTL: 24 hours

</details>

---

## Data Notes

> EOD OHLCV data for `^NSEI` and `GOLDBEES.NS` sourced from NSE India via yfinance.
> Default date range: 2018-01-01 to present. Data is stored locally in DuckDB and
> refreshed automatically; no manual updates required.

---

## Part of

> This project is part of the **Information Theory × Finance** series by
> [Pranava BA](https://github.com/pranava-ba).  
> [View all projects →](https://github.com/information-theory-finance)

---

<div align="center">

**Pranava BA** · Chennai, India · © 2025–2026

</div>
