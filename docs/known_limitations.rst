.. _known_limitations:

Known Limitations
=================

This page enumerates mathematical, data, and UI limitations of the current
release.

----

Mathematical Limitations
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Detail
   * - Discrete entropy only
     - Only the discrete Shannon entropy :math:`H(X) = -\sum p \log p`
       is implemented.  Differential (continuous) entropy and its estimators
       (KDE-based, k-nearest-neighbour) are out of scope.
   * - Bin-count sensitivity
     - The PMF is estimated by histogram binning.  The number of bins
       :math:`n` strongly affects the entropy value; there is no automatic
       bandwidth selection (e.g. Sturges, Scott, Freedman-Diaconis rule).
   * - Window length bias
     - Short rolling windows (:math:`w < 30`) produce highly variable PMF
       estimates.  The entropy is consistent but has high variance.
   * - Independence assumption
     - The rolling entropy treats each window as i.i.d. samples from a
       stationary distribution.  Serial correlation in returns violates this.
   * - No differential entropy
     - Gaussian return distributions have a closed-form differential entropy
       :math:`H = \frac{1}{2}\ln(2\pi e \sigma^2)`, but this is not computed
       or compared here.

----

Data Limitations
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Detail
   * - No real Level-2 data
     - Order-book entropy is computed on *simulated* synthetic books.  Real
       NSE Level-2 data requires an exchange data subscription.
   * - EOD resolution only
     - The finance page uses end-of-day prices.  Intraday entropy heatmaps
       would require minute-level or tick data, which is not fetched.
   * - Single ticker
     - Only ``^NSEI`` is analysed.  Multi-asset joint entropy or
       conditional entropy across the universe is not implemented here.
   * - yfinance dependency
     - Data quality and availability depend on Yahoo Finance's API, which
       has no SLA and may change schema without notice.

----

UI Limitations
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Detail
   * - No intraday heatmap
     - The spec mentions an intraday entropy heatmap; this requires tick
       data and is deferred to a future release.
   * - No VIX overlay
     - Correlation with VIX/India VIX is not plotted; VIX data is not in
       the fixed ticker universe.
   * - In-sample backtest only
     - The backtest threshold is fitted on the full visible history.  No
       walk-forward or out-of-sample split is performed.
   * - No mobile optimisation
     - The app is designed for wide desktop layouts; narrow viewports may
       clip chart labels.
