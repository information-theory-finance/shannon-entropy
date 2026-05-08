.. _finance:

Finance Application
===================

Shannon entropy translates naturally into a market-microstructure diagnostic.
This page explains how the project applies entropy to NIFTY 50 return
distributions and synthetic order books, and how a threshold signal is derived.

----

Why This Applies to Financial Data
-----------------------------------

A return series is a sequence of realisations from an unknown distribution.
When that distribution is approximately uniform (all return bins equally
likely), entropy is high — consistent with an efficient, unpredictable market.
When the distribution becomes concentrated (e.g. persistent drift or
volatility clustering), entropy drops — signalling structure that a trader
might exploit.

Similarly, the order book's volume distribution carries information about
liquidity and informed trading.  A flat (high-entropy) book suggests balanced
supply and demand; a concentrated (low-entropy) book may reveal directional
pressure or thin liquidity.

----

Tickers and Data
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Ticker
     - Description
   * - ``^NSEI``
     - NIFTY 50 Index, fetched via ``yfinance``, cached in DuckDB,
       daily OHLCV from 2018-01-01 to present.  Auto-refreshed every
       24 hours on Streamlit Cloud.

----

Methodology
-----------

**Step 1 — Log-return computation**

.. math::

   r_t = \log\!\left(\frac{P_t}{P_{t-1}}\right)

Log-returns are used rather than percent changes for their additive
time-aggregation property.

**Step 2 — Discretisation**

The return series is binned into :math:`n` equal-width intervals using
``pandas.cut``.  The resulting histogram is normalised to a PMF.

**Step 3 — Rolling entropy**

At each date :math:`t`, the entropy of the empirical PMF constructed from the
prior :math:`w` returns is computed:

.. math::

   H_t = -\sum_{k=1}^{n} \hat{p}_{t,k}\,\log_2\,\hat{p}_{t,k}

where :math:`\hat{p}_{t,k}` is the fraction of the :math:`w` returns falling
in bin :math:`k`.

**Step 4 — Order-book entropy**

Bid and ask volume vectors :math:`\mathbf{v}^{\text{bid}},
\mathbf{v}^{\text{ask}} \in \mathbb{R}^L_+` (one entry per price level) are
normalised and passed through the entropy formula.  Three regimes are
simulated: liquid (exponentially decaying volumes), illiquid (thin, noisy),
and one-sided (imbalanced book).

**Step 5 — Trading signal**

A long position is entered when :math:`H_t` falls below the
:math:`q`-th percentile of the observed entropy distribution (default
:math:`q = 0.25`).  The position is held for :math:`h` days (default
:math:`h = 5`) and then closed, regardless of subsequent entropy readings.

----

Interpreting Results
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Observation
     - Interpretation
   * - Entropy rising
     - Return distribution spreading out; market becoming more random
   * - Entropy falling below threshold
     - Increased predictability / structure in recent returns
   * - High entropy + high volatility
     - Chaotic, noisy market; both measures elevated in stress periods
   * - Low book entropy (bid side)
     - Volume concentrated at best bid; potential support level
   * - Large OBI with low ask entropy
     - Sellers concentrated; directional pressure downward

----

Example Output
--------------

A typical run on NIFTY 50 data (2018–2025) with a 60-day window and 20 bins
produces rolling entropy values in the range [3.0, 4.3] bits, with a mean
around 3.8 bits and dips below 3.5 bits during sustained trend episodes
(e.g. the 2020 COVID crash and the 2022 rate-hike drawdown).

----

Limitations and Caveats
-----------------------

.. important::

   The backtest is purely illustrative.  The following biases and limitations
   apply:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Limitation
     - Detail
   * - In-sample threshold
     - The percentile threshold is computed on the full history; in live
       trading it must be computed on a rolling expanding window.
   * - No transaction costs
     - Bid-ask spread, brokerage, and STT are not modelled.
   * - Discretisation sensitivity
     - Entropy values depend on the number of bins; more bins → higher
       entropy, but noisier estimates for small windows.
   * - EOD data only
     - Order-book entropy uses simulated, not real, Level-2 data.
   * - Single asset
     - No portfolio construction or position sizing is performed.
