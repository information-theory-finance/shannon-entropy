.. _overview:

Overview
========

Shannon entropy — introduced by Claude E. Shannon in *A Mathematical Theory
of Communication* (1948) — quantifies the average information content, or
irreducible uncertainty, of a probability distribution. This project applies
the concept directly to NSE equity return distributions and simulated order
books, treating market microstructure as an information-theoretic system.

----

Why This Concept
----------------

Financial markets encode information about future prices through the
distribution of past returns and the depth of the order book. Shannon entropy
provides a single scalar that summarises how spread out (uncertain) or
concentrated (predictable) that distribution is. Unlike variance, entropy is
sensitive to the *shape* of the distribution, not just its second moment —
making it a richer signal for regime detection and liquidity measurement.

----

Formula
-------

.. math::

   H(X) = -\sum_{x \in \mathcal{X}} p(x)\,\log_2 p(x) \quad [\text{bits}]

where :math:`p(x)` is the probability mass function of the discrete random
variable :math:`X` over alphabet :math:`\mathcal{X}`.  The convention
:math:`0 \cdot \log_2 0 := 0` handles zero-probability outcomes.

----

Technology Stack
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Layer
     - Library
     - Role
   * - Core math
     - NumPy
     - Entropy computation, PMF discretisation, rolling statistics
   * - Data
     - yfinance + DuckDB
     - Fetch and cache OHLCV data; incremental update pattern
   * - Data wrangling
     - pandas
     - Time-series alignment, rolling windows, backtest P&L
   * - UI
     - Streamlit 1.30+
     - Interactive pages with sliders, tabs, and metrics
   * - Visualisation
     - Plotly
     - All charts; themed via ``utils/theme.py``
   * - Docs
     - Sphinx + RTD theme
     - This documentation site

----

Feature Summary
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - Description
   * - Shannon entropy (from scratch)
     - Pure NumPy implementation with configurable log base
   * - Binary entropy curve
     - Interactive :math:`H_b(p)` vs :math:`p` with slider and base selector
   * - Uniform distribution explorer
     - :math:`H = \log_2 n` visualised for :math:`n \in [1, 100]`
   * - Custom PMF builder
     - Drag sliders to define any PMF; entropy updates live
   * - Rolling return entropy
     - NIFTY 50 log-returns discretised and passed through rolling window
   * - Entropy vs volatility
     - Scatter with year-coloured markers and Pearson correlation
   * - Order-book simulator
     - Synthetic Level-2 book with liquid / illiquid / one-sided regimes
   * - Entropy backtest
     - Long signal triggered when entropy falls below a percentile threshold

----

Scope
-----

Will
~~~~

- Compute and visualise Shannon entropy for discrete PMFs.
- Apply rolling entropy to NIFTY 50 daily log-returns.
- Simulate order-book entropy across three liquidity regimes.
- Run a simple entropy-threshold backtest and report summary statistics.

Will Not
~~~~~~~~

- Use true tick-level or real Level-2 order-book data (requires exchange
  subscription; simulated data is used instead).
- Compute continuous (differential) entropy — this project restricts itself
  to discrete distributions.
- Implement joint or conditional entropy, mutual information, or
  transfer entropy (covered in separate ITF projects).

----

Tickers Used
------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - yfinance symbol
     - Name
     - Rationale
   * - ``^NSEI``
     - NIFTY 50 Index
     - Broad-market benchmark; high liquidity, clean data, ideal for
       single-asset entropy analysis per the ITF ticker selection rules.
