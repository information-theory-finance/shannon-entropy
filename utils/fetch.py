# utils/fetch.py
# Information Theory × Finance — Shannon Entropy
# Data fetching and DuckDB caching layer.
# Part of the information-theory-finance series.
# Author: Pranava BA

import yfinance as yf
import duckdb
from pathlib import Path
from datetime import date, timedelta
import pandas as pd

DB_PATH = Path("data/nse.duckdb")

CREATE_TABLE_SQL = """
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
"""


def ensure_data(ticker: str, start: str = "2018-01-01") -> pd.DataFrame:
    """
    Fetch and cache OHLCV data for *ticker* in a local DuckDB database.

    Steps
    -----
    1. Connect to DuckDB (create if not exists).
    2. Create ``prices`` table if not present.
    3. Check latest stored date for this ticker.
    4. If a gap exists between that date and today, fetch the missing
       days via yfinance.
    5. Upsert new rows into DuckDB.
    6. Return the full OHLCV DataFrame for the ticker.

    Parameters
    ----------
    ticker : str
        yfinance ticker symbol (e.g. ``"^NSEI"``).
    start : str, optional
        ISO date string for the historical start. Default ``"2018-01-01"``.

    Returns
    -------
    pd.DataFrame
        Columns: ticker, date, open, high, low, close, volume.
    """
    DB_PATH.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute(CREATE_TABLE_SQL)

    result = con.execute(
        "SELECT MAX(date) FROM prices WHERE ticker = ?", [ticker]
    ).fetchone()
    latest = result[0]

    fetch_start = start
    if latest is not None:
        next_day = (latest + timedelta(days=1)).strftime("%Y-%m-%d")
        if next_day >= date.today().strftime("%Y-%m-%d"):
            return con.execute(
                "SELECT * FROM prices WHERE ticker = ? ORDER BY date", [ticker]
            ).df()
        fetch_start = next_day

    raw = yf.download(ticker, start=fetch_start, progress=False, auto_adjust=True)
    if not raw.empty:
        raw = raw.reset_index()
        raw.columns = [c[0] if isinstance(c, tuple) else c for c in raw.columns]
        raw["ticker"] = ticker
        raw = raw.rename(columns={
            "Date": "date", "Open": "open", "High": "high",
            "Low": "low", "Close": "close", "Volume": "volume"
        })[["ticker", "date", "open", "high", "low", "close", "volume"]]
        con.execute("INSERT OR REPLACE INTO prices SELECT * FROM raw")

    df = con.execute(
        "SELECT * FROM prices WHERE ticker = ? ORDER BY date", [ticker]
    ).df()
    con.close()
    return df


def get_ohlcv(ticker: str) -> pd.DataFrame:
    """
    Public entry point. Return the full OHLCV DataFrame for *ticker*.

    Parameters
    ----------
    ticker : str
        yfinance ticker symbol.

    Returns
    -------
    pd.DataFrame
        Columns: ticker, date, open, high, low, close, volume.
    """
    return ensure_data(ticker)
