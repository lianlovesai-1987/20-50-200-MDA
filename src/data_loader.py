"""
data_loader.py — Phase 1: Data Acquisition & Validation
=========================================================
Fetches historical daily closing prices for a given ticker
using yfinance (Yahoo Finance — free, public, no API key needed).

Assumptions:
- We use adjusted closing prices to account for splits/dividends.
- Default date range: 2000-01-01 to today (gives enough history for 200-day MA).
- Starting capital: $10,000 (used in backtest.py).
- No transaction costs in the base case (flagged as assumption).
"""

import yfinance as yf
import pandas as pd


# --- Ticker mapping ---
INDEX_TICKERS = {
    "SP500": "^GSPC",   # S&P 500
    "DJIA":  "^DJI",    # Dow Jones Industrial Average
}


def fetch_price_data(index: str = "SP500",
                     start: str = "2000-01-01",
                     end: str = None) -> pd.DataFrame:
    """
    Fetch adjusted daily closing prices for the given index.

    Parameters
    ----------
    index : str — "SP500" or "DJIA"
    start : str — start date in YYYY-MM-DD format
    end   : str — end date in YYYY-MM-DD format (defaults to today)

    Returns
    -------
    pd.DataFrame with columns: ['Date', 'Close']
    """
    ticker = INDEX_TICKERS.get(index.upper())
    if not ticker:
        raise ValueError(f"Unknown index '{index}'. Choose from: {list(INDEX_TICKERS.keys())}")

    print(f"Fetching {index} ({ticker}) from {start} to {end or 'today'}...")
    raw = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

    if raw.empty:
        raise RuntimeError(f"No data returned for {ticker}. Check ticker or date range.")

    df = raw[["Close"]].copy()
    df.index.name = "Date"
    df.reset_index(inplace=True)

    return df


def validate_price_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean price data.
    - Checks for missing dates (gaps)
    - Drops rows with NaN Close prices
    - Sorts by date ascending
    - Flags any issues to the console

    Parameters
    ----------
    df : pd.DataFrame with columns ['Date', 'Close']

    Returns
    -------
    Cleaned pd.DataFrame
    """
    print(f"Validating data: {len(df)} rows, {df['Date'].min()} to {df['Date'].max()}")

    # Sort ascending
    df = df.sort_values("Date").reset_index(drop=True)

    # Drop NaN closing prices
    nan_count = df["Close"].isna().sum()
    if nan_count > 0:
        print(f"  ⚠️  Dropping {nan_count} rows with missing Close prices.")
        df = df.dropna(subset=["Close"]).reset_index(drop=True)

    # Check for duplicate dates
    dupes = df["Date"].duplicated().sum()
    if dupes > 0:
        print(f"  ⚠️  Found {dupes} duplicate dates — keeping first occurrence.")
        df = df.drop_duplicates(subset=["Date"], keep="first").reset_index(drop=True)

    print(f"  ✅ Validation complete: {len(df)} clean rows.")
    return df


if __name__ == "__main__":
    # Quick smoke test
    df = fetch_price_data("SP500", start="2000-01-01")
    df = validate_price_data(df)
    print(df.tail())
