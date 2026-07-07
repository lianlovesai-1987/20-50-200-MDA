"""
indicators.py — Phase 2: Moving Average Calculations
======================================================
Calculates simple moving averages (SMA) for the 20, 50, and 200-day windows.

Math:
    SMA(n) on day t = average of closing prices over the last n trading days
    SMA_t = (P_t + P_t-1 + ... + P_t-n+1) / n

Note: The first (n-1) rows will be NaN — this is expected and correct.
No look-ahead bias: each SMA value only uses data available up to that day.
"""

import pandas as pd


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add 20-day, 50-day, and 200-day simple moving averages to the dataframe.

    Parameters
    ----------
    df : pd.DataFrame with columns ['Date', 'Close']

    Returns
    -------
    pd.DataFrame with additional columns: ['SMA20', 'SMA50', 'SMA200']
    """
    df = df.copy()

    df["SMA20"]  = df["Close"].rolling(window=20).mean()
    df["SMA50"]  = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()

    # Drop rows where any MA is NaN (first 199 rows)
    df = df.dropna(subset=["SMA20", "SMA50", "SMA200"]).reset_index(drop=True)

    print(f"Moving averages calculated. {len(df)} rows after dropping warm-up period.")
    return df


if __name__ == "__main__":
    from data_loader import fetch_price_data, validate_price_data
    df = fetch_price_data("SP500")
    df = validate_price_data(df)
    df = add_moving_averages(df)
    print(df[["Date", "Close", "SMA20", "SMA50", "SMA200"]].tail(10))
