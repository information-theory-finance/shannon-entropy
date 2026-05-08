.. _changelog:

Changelog
=========

----

v0.1.0
------

*Initial release — May 2026*

Changes
~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - ID
     - Description
   * - C-001
     - Implemented ``shannon_entropy``, ``bernoulli_entropy``,
       ``uniform_entropy``, ``normalised_entropy`` in ``utils/math_core.py``.
   * - C-002
     - Implemented ``rolling_entropy``, ``rolling_volatility``,
       ``discretise_returns`` for financial time-series analysis.
   * - C-003
     - Implemented ``simulate_order_book`` and ``order_book_entropy``
       for Level-2 book simulation across three liquidity regimes.
   * - C-004
     - Implemented ``entropy_signal`` backtest with percentile threshold
       entry and fixed hold-period exit.
   * - C-005
     - Built ``utils/fetch.py`` with DuckDB caching and incremental
       yfinance update pattern.
   * - C-006
     - Theory page: binary entropy curve, uniform distribution explorer,
       custom PMF builder with live entropy readout.
   * - C-007
     - Finance page: rolling entropy + price + volatility subplot,
       entropy vs volatility scatter, PMF bar chart, order-book simulator,
       and backtest P&L curve with summary statistics table.
   * - C-008
     - Full Sphinx documentation site with RTD theme and custom dark CSS.
   * - C-009
     - README with ASCII banner, badges, screenshots table, feature
       dropdowns, and data notes block.

Bug Fixes
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - ID
     - Description
   * - B-001
     - No bugs recorded in initial release.
