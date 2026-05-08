# utils/math_core.py
# Information Theory × Finance — Shannon Entropy
# Pure mathematics module. Zero Streamlit imports. Independently testable.
# Part of the information-theory-finance series.
# Author: Pranava BA

import numpy as np
import pandas as pd
from typing import Literal


# ── Core entropy computation ───────────────────────────────────────────────

def shannon_entropy(
    probs: np.ndarray,
    base: float = 2.0,
) -> float:
    """
    Compute Shannon entropy H(X) = -Σ p(x) log_b p(x).

    Parameters
    ----------
    probs : np.ndarray
        Probability mass function. Values must be non-negative; they are
        normalised internally so they need not sum to 1.
    base : float, optional
        Logarithm base. 2 → bits (default), e → nats, 10 → hartleys.

    Returns
    -------
    float
        Shannon entropy in the requested unit.

    Notes
    -----
    Zero probability terms contribute 0 to the sum (0 · log 0 := 0),
    consistent with the convention lim_{p→0} p log p = 0.
    """
    probs = np.asarray(probs, dtype=float)
    probs = probs[probs > 0]
    if probs.size == 0:
        return 0.0
    probs = probs / probs.sum()
    return float(-np.sum(probs * np.log(probs) / np.log(base)))


def max_entropy(n: int, base: float = 2.0) -> float:
    """
    Maximum entropy for a distribution over *n* equally likely outcomes.

    H_max = log_b(n)

    Parameters
    ----------
    n : int
        Number of outcomes (alphabet size).
    base : float, optional
        Logarithm base. Default 2 (bits).

    Returns
    -------
    float
        Maximum attainable entropy log_b(n).
    """
    if n <= 1:
        return 0.0
    return float(np.log(n) / np.log(base))


def normalised_entropy(probs: np.ndarray, base: float = 2.0) -> float:
    """
    Normalised entropy ∈ [0, 1]: H(X) / H_max(|Alphabet|).

    A value of 1 means the distribution is perfectly uniform; 0 means
    all mass on one outcome (deterministic).

    Parameters
    ----------
    probs : np.ndarray
        Probability mass function.
    base : float, optional
        Logarithm base.

    Returns
    -------
    float
        Normalised entropy in [0, 1].
    """
    probs = np.asarray(probs, dtype=float)
    n = probs[probs > 0].size
    h_max = max_entropy(n, base)
    if h_max == 0.0:
        return 0.0
    return shannon_entropy(probs, base) / h_max


# ── Named distributions ────────────────────────────────────────────────────

def bernoulli_entropy(p: float, base: float = 2.0) -> float:
    """
    Binary entropy function H_b(p) = -p log p - (1-p) log(1-p).

    Parameters
    ----------
    p : float
        Success probability ∈ [0, 1].
    base : float, optional
        Logarithm base.

    Returns
    -------
    float
        Binary entropy H_b(p).
    """
    p = float(np.clip(p, 1e-12, 1 - 1e-12))
    return shannon_entropy(np.array([p, 1 - p]), base)


def bernoulli_entropy_curve(
    n_points: int = 300, base: float = 2.0
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return (p_values, H_values) for the binary entropy curve.

    Useful for plotting H_b(p) vs p on [0, 1].

    Parameters
    ----------
    n_points : int, optional
        Resolution of the curve.
    base : float, optional
        Logarithm base.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        p ∈ (0, 1) and corresponding H_b(p).
    """
    ps = np.linspace(1e-6, 1 - 1e-6, n_points)
    hs = np.array([bernoulli_entropy(p, base) for p in ps])
    return ps, hs


def uniform_entropy(n: int, base: float = 2.0) -> float:
    """
    Entropy of the discrete uniform distribution over n outcomes.

    H(X) = log_b(n)

    Parameters
    ----------
    n : int
        Number of equally likely outcomes.
    base : float, optional
        Logarithm base.

    Returns
    -------
    float
        log_b(n).
    """
    return max_entropy(n, base)


def entropy_of_custom_pmf(weights: list[float], base: float = 2.0) -> float:
    """
    Compute entropy from an arbitrary list of unnormalised weights.

    Parameters
    ----------
    weights : list[float]
        Non-negative weights; normalised internally.
    base : float, optional
        Logarithm base.

    Returns
    -------
    float
        Shannon entropy.
    """
    return shannon_entropy(np.array(weights, dtype=float), base)


# ── Financial return discretisation ───────────────────────────────────────

def discretise_returns(
    returns: pd.Series,
    n_bins: int = 20,
    method: Literal["equal_width", "equal_freq"] = "equal_width",
) -> np.ndarray:
    """
    Discretise a continuous return series into a probability mass function.

    Parameters
    ----------
    returns : pd.Series
        Daily (or intraday) log-returns or percent changes.
    n_bins : int, optional
        Number of bins. Default 20.
    method : {"equal_width", "equal_freq"}, optional
        Binning strategy. "equal_width" uses fixed-width bins;
        "equal_freq" (quantile) ensures each bin has equal count.

    Returns
    -------
    np.ndarray
        Normalised probability mass function of length n_bins.
    """
    returns = returns.dropna()
    if method == "equal_freq":
        bins = pd.qcut(returns, q=n_bins, duplicates="drop")
    else:
        bins = pd.cut(returns, bins=n_bins)
    counts = bins.value_counts().sort_index().values.astype(float)
    total = counts.sum()
    if total == 0:
        return np.ones(n_bins) / n_bins
    return counts / total


def rolling_entropy(
    series: pd.Series,
    window: int = 60,
    n_bins: int = 20,
    base: float = 2.0,
    method: Literal["equal_width", "equal_freq"] = "equal_width",
) -> pd.Series:
    """
    Compute rolling Shannon entropy of a return series.

    At each date t, entropy is computed over the empirical distribution of
    returns in [t - window + 1, t].

    Parameters
    ----------
    series : pd.Series
        Return series (DatetimeIndex recommended).
    window : int, optional
        Look-back window in observations. Default 60.
    n_bins : int, optional
        Number of bins for discretisation.
    base : float, optional
        Logarithm base.
    method : {"equal_width", "equal_freq"}, optional
        Binning strategy.

    Returns
    -------
    pd.Series
        Rolling entropy values aligned to the input index, NaN for the
        initial (window - 1) observations.
    """
    result = pd.Series(index=series.index, dtype=float)
    for i in range(window - 1, len(series)):
        chunk = series.iloc[i - window + 1 : i + 1]
        pmf = discretise_returns(chunk, n_bins=n_bins, method=method)
        result.iloc[i] = shannon_entropy(pmf, base)
    return result


def rolling_volatility(series: pd.Series, window: int = 60) -> pd.Series:
    """
    Rolling annualised volatility (standard deviation × √252).

    Parameters
    ----------
    series : pd.Series
        Daily return series.
    window : int, optional
        Look-back window. Default 60.

    Returns
    -------
    pd.Series
        Annualised rolling volatility.
    """
    return series.rolling(window).std() * np.sqrt(252)


# ── Order-book entropy (simulated / discretised) ───────────────────────────

def order_book_entropy(
    bid_volumes: np.ndarray,
    ask_volumes: np.ndarray,
    base: float = 2.0,
) -> dict:
    """
    Compute Shannon entropy of bid side, ask side, and combined order book.

    Parameters
    ----------
    bid_volumes : np.ndarray
        Volume at each bid price level (index 0 = best bid).
    ask_volumes : np.ndarray
        Volume at each ask price level (index 0 = best ask).
    base : float, optional
        Logarithm base.

    Returns
    -------
    dict
        Keys: "bid_entropy", "ask_entropy", "book_entropy",
              "bid_pmf", "ask_pmf", "imbalance".
    """
    bid_volumes = np.asarray(bid_volumes, dtype=float)
    ask_volumes = np.asarray(ask_volumes, dtype=float)

    bid_pmf = bid_volumes / bid_volumes.sum() if bid_volumes.sum() > 0 else bid_volumes
    ask_pmf = ask_volumes / ask_volumes.sum() if ask_volumes.sum() > 0 else ask_volumes

    combined = np.concatenate([bid_volumes, ask_volumes])

    total_bid = bid_volumes.sum()
    total_ask = ask_volumes.sum()
    imbalance = (total_bid - total_ask) / (total_bid + total_ask + 1e-12)

    return {
        "bid_entropy": shannon_entropy(bid_pmf, base),
        "ask_entropy": shannon_entropy(ask_pmf, base),
        "book_entropy": shannon_entropy(combined, base),
        "bid_pmf": bid_pmf,
        "ask_pmf": ask_pmf,
        "imbalance": float(imbalance),
    }


def simulate_order_book(
    mid_price: float = 100.0,
    n_levels: int = 10,
    tick_size: float = 0.05,
    regime: Literal["liquid", "illiquid", "one_sided"] = "liquid",
    rng: np.random.Generator | None = None,
) -> dict:
    """
    Simulate a synthetic Level-2 order book snapshot.

    Parameters
    ----------
    mid_price : float, optional
        Reference mid-price.
    n_levels : int, optional
        Number of price levels on each side.
    tick_size : float, optional
        Spread between price levels.
    regime : {"liquid", "illiquid", "one_sided"}, optional
        Volume profile shape.
    rng : np.random.Generator or None, optional
        Random generator for reproducibility.

    Returns
    -------
    dict
        Keys: "bid_prices", "ask_prices", "bid_volumes", "ask_volumes",
              "spread", "mid_price".
    """
    if rng is None:
        rng = np.random.default_rng(42)

    bid_prices = mid_price - tick_size * (np.arange(n_levels) + 0.5)
    ask_prices = mid_price + tick_size * (np.arange(n_levels) + 0.5)

    if regime == "liquid":
        bid_vols = rng.exponential(scale=500, size=n_levels) * np.exp(-0.15 * np.arange(n_levels))
        ask_vols = rng.exponential(scale=500, size=n_levels) * np.exp(-0.15 * np.arange(n_levels))
    elif regime == "illiquid":
        bid_vols = rng.exponential(scale=50, size=n_levels)
        ask_vols = rng.exponential(scale=50, size=n_levels)
    else:  # one_sided
        bid_vols = rng.exponential(scale=800, size=n_levels) * np.exp(-0.1 * np.arange(n_levels))
        ask_vols = rng.exponential(scale=80, size=n_levels)

    spread = ask_prices[0] - bid_prices[0]

    return {
        "bid_prices": bid_prices,
        "ask_prices": ask_prices,
        "bid_volumes": bid_vols,
        "ask_volumes": ask_vols,
        "spread": spread,
        "mid_price": mid_price,
    }


# ── Backtest signal ────────────────────────────────────────────────────────

def entropy_signal(
    entropy_series: pd.Series,
    price_series: pd.Series,
    threshold_pct: float = 0.25,
    hold_days: int = 5,
) -> pd.DataFrame:
    """
    Simple entropy-threshold trading signal.

    Entry: when rolling entropy drops below the given percentile threshold
    (low entropy → low uncertainty → potential directional move).
    Exit: after *hold_days* trading sessions.

    Parameters
    ----------
    entropy_series : pd.Series
        Rolling entropy values aligned to *price_series*.
    price_series : pd.Series
        Closing prices.
    threshold_pct : float, optional
        Percentile of the entropy distribution used as the entry threshold.
        Default 0.25 (25th percentile).
    hold_days : int, optional
        Number of days to hold after entry. Default 5.

    Returns
    -------
    pd.DataFrame
        Columns: "price", "entropy", "signal", "strategy_return",
                 "buy_hold_return", "cum_strategy", "cum_buyhold".
    """
    df = pd.DataFrame({
        "price": price_series,
        "entropy": entropy_series,
    }).dropna()

    threshold = df["entropy"].quantile(threshold_pct)
    df["signal"] = 0

    in_trade = 0
    for i in range(len(df)):
        if in_trade > 0:
            df.iloc[i, df.columns.get_loc("signal")] = 1
            in_trade -= 1
        elif df["entropy"].iloc[i] < threshold:
            df.iloc[i, df.columns.get_loc("signal")] = 1
            in_trade = hold_days - 1

    df["daily_return"] = df["price"].pct_change()
    df["strategy_return"] = df["signal"].shift(1).fillna(0) * df["daily_return"]
    df["buy_hold_return"] = df["daily_return"]

    df["cum_strategy"] = (1 + df["strategy_return"]).cumprod()
    df["cum_buyhold"] = (1 + df["buy_hold_return"]).cumprod()

    return df
