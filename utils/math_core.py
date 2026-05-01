# utils/math_core.py
# Pure Shannon entropy implementation — no Streamlit dependency.
# Information Theory × Finance series — github.com/information-theory-finance

import numpy as np
from typing import Literal


def estimate_pmf(data: np.ndarray, bins: int = 50) -> np.ndarray:
    """
    Estimate a probability mass function from continuous data via histogram.

    Parameters
    ----------
    data : array-like of floats
    bins : number of histogram bins

    Returns
    -------
    pmf : 1-D array of positive probabilities summing to 1
    """
    counts, _ = np.histogram(data, bins=bins)
    total = counts.sum()
    if total == 0:
        raise ValueError("data array is empty or all-zero")
    pmf = counts / total
    return pmf[pmf > 0]  # drop zero bins to avoid log(0)


def shannon_entropy(pmf: np.ndarray, base: float = 2.0) -> float:
    """
    Compute Shannon entropy H(X) = -∑ p(x) log_b p(x).

    Parameters
    ----------
    pmf  : probability mass function (must be positive and sum to ~1)
    base : logarithm base. 2 → bits, e → nats, 10 → hartleys

    Returns
    -------
    entropy : float ≥ 0
    """
    pmf = np.asarray(pmf, dtype=float)
    pmf = pmf[pmf > 0]
    return float(-np.sum(pmf * np.log(pmf) / np.log(base)))


def entropy_from_data(
    data: np.ndarray,
    bins: int = 50,
    base: float = 2.0,
) -> float:
    """Estimate entropy directly from raw data via PMF estimation."""
    pmf = estimate_pmf(data, bins=bins)
    return shannon_entropy(pmf, base=base)


def max_entropy(n_bins: int, base: float = 2.0) -> float:
    """
    Maximum possible entropy for a distribution over ``n_bins`` outcomes.
    Achieved by the uniform distribution: H_max = log_b(n).
    """
    return float(np.log(n_bins) / np.log(base))


def rolling_entropy(
    series: np.ndarray,
    window: int = 30,
    bins: int = 20,
    base: float = 2.0,
) -> np.ndarray:
    """
    Compute rolling Shannon entropy over a time series.

    Parameters
    ----------
    series : 1-D array of floats (e.g., log returns)
    window : rolling window size in periods
    bins   : histogram bins for PMF estimation within each window
    base   : log base for entropy units

    Returns
    -------
    result : array same length as ``series``, NaN for the first ``window`` entries
    """
    result = np.full(len(series), np.nan)
    for i in range(window, len(series) + 1):
        window_data = series[i - window : i]
        try:
            result[i - 1] = entropy_from_data(window_data, bins=bins, base=base)
        except ValueError:
            result[i - 1] = np.nan
    return result


def synthetic_entropy_curve(
    distribution: Literal["normal", "uniform", "exponential", "laplace"],
    param_values: np.ndarray,
    bins: int = 200,
    n_samples: int = 10_000,
    base: float = 2.0,
    seed: int = 42,
) -> np.ndarray:
    """
    Compute entropy for a range of distribution parameter values.
    Used for the interactive theory page plot.

    Parameters
    ----------
    distribution  : distribution family name
    param_values  : 1-D array of parameter values (std for normal, scale for others)
    bins          : histogram bins for PMF estimation
    n_samples     : Monte Carlo sample count per parameter value
    base          : log base
    seed          : random seed for reproducibility

    Returns
    -------
    entropies : array of entropy values, same length as param_values
    """
    rng = np.random.default_rng(seed)
    entropies = np.zeros(len(param_values))
    for k, p in enumerate(param_values):
        if p <= 0:
            entropies[k] = np.nan
            continue
        if distribution == "normal":
            data = rng.normal(0, p, n_samples)
        elif distribution == "uniform":
            data = rng.uniform(-p, p, n_samples)
        elif distribution == "exponential":
            data = rng.exponential(p, n_samples)
        elif distribution == "laplace":
            data = rng.laplace(0, p, n_samples)
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
        entropies[k] = entropy_from_data(data, bins=bins, base=base)
    return entropies
