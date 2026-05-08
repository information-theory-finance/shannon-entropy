.. _data_notes:

Data Notes
==========

This page documents the data source, tickers, date range, known quality
issues, and the DuckDB schema used for caching.

----

Data Source
-----------

All price data is fetched via `yfinance <https://github.com/ranaroussi/yfinance>`_
with ``auto_adjust=True`` (dividend and split adjustments applied
automatically by the library).  Data is persisted locally in a DuckDB
database at ``data/nse.duckdb`` and refreshed incrementally: only the gap
between the last stored date and today is re-fetched on each run.

.. note::

   The ``data/`` directory is excluded from version control via ``.gitignore``.
   The database is created at runtime on first run.

----

Tickers
-------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - yfinance symbol
     - Exchange name
     - Notes
   * - ``^NSEI``
     - NSE NIFTY 50 Index
     - Index level; ``Volume`` column is always 0 for indices in yfinance.

----

Date Range
----------

Default start date: **2018-01-01** (configurable via the ``start`` parameter
of ``ensure_data``).  End date: always the most recent available trading day.
The full history spans approximately 1,800 trading sessions as of 2026.

----

Known Data Quality Issues
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Issue
     - Detail
   * - Zero volume for index
     - ``^NSEI`` is an index; yfinance always returns 0 for the Volume field.
       This column is not used in any entropy calculation.
   * - Holiday NaNs
     - NSE holidays produce gaps in the date series.  Rows for non-trading
       days are simply absent; no forward-fill is applied.
   * - yfinance rate limits
     - Excessive calls within a short window may result in ``429 Too Many
       Requests``.  The DuckDB caching layer mitigates this by re-fetching
       only missing days.
   * - Adjusted prices
     - ``auto_adjust=True`` modifies historical prices retroactively on
       corporate events.  This can cause small discontinuities on re-fetch.

----

DuckDB Schema
-------------

.. code-block:: sql

   CREATE TABLE IF NOT EXISTS prices (
       ticker  VARCHAR,
       date    DATE,
       open    DOUBLE,
       high    DOUBLE,
       low     DOUBLE,
       close   DOUBLE,
       volume  BIGINT,
       PRIMARY KEY (ticker, date)
   );
