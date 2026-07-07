"""
signals.py — Phase 3: Crossover Detection & Signal Generation
==============================================================
Detects crossover events and generates BUY/SELL signals.

Signal A: 20-day SMA crosses the 50-day SMA
Signal B: 50-day SMA crosses the 200-day SMA

Logic:
    A crossover UP   on day t: shorter_MA[t-1] < longer_MA[t-1]  AND  shorter_MA[t] >= longer_MA[t]  → BUY
    A crossover DOWN on day t: shorter_MA[t-1] > longer_MA[t-1]  AND  shorter_MA[t] <= longer_MA[t]  → SELL

No look-ahead bias: signals are generated using only data from the previous day
to determine if a cross occurred at today's open/close.
"""

import pandas as pd


def detect_crossovers(df: pd.DataFrame,
                      fast_col: str,
                      slow_col: str,
                      signal_label: str) -> pd.DataFrame:
    """
    Detect crossover events between two moving average columns.

    Parameters
    ----------
    df           : pd.DataFrame with the two MA columns
    fast_col     : column name of the shorter (faster) MA
    slow_col     : column name of the longer (slower) MA
    signal_label : label for the signal column (e.g. 'Signal_A')

    Returns
    -------
    pd.DataFrame with an added signal column:
        1  = BUY  (fast crossed above slow)
       -1  = SELL (fast crossed below slow)
        0  = no signal
    """
    df = df.copy()

    prev_fast = df[fast_col].shift(1)
    prev_slow = df[slow_col].shift(1)

    buy_signal  = (prev_fast < prev_slow) & (df[fast_col] >= df[slow_col])
    sell_signal = (prev_fast > prev_slow) & (df[fast_col] <= df[slow_col])

    df[signal_label] = 0
    df.loc[buy_signal,  signal_label] = 1
    df.loc[sell_signal, signal_label] = -1

    buys  = (df[signal_label] ==  1).sum()
    sells = (df[signal_label] == -1).sum()
    print(f"{signal_label}: {buys} BUY signals, {sells} SELL signals detected.")

    return df


def generate_all_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate both Signal A and Signal B on the dataframe.

    Signal A: SMA20 vs SMA50
    Signal B: SMA50 vs SMA200
    """
    df = detect_crossovers(df, fast_col="SMA20", slow_col="SMA50",  signal_label="Signal_A")
    df = detect_crossovers(df, fast_col="SMA50", slow_col="SMA200", signal_label="Signal_B")
    return df


if __name__ == "__main__":
    from data_loader import fetch_price_data, validate_price_data
    from indicators import add_moving_averages

    df = fetch_price_data("SP500")
    df = validate_price_data(df)
    df = add_moving_averages(df)
    df = generate_all_signals(df)

    signals = df[(df["Signal_A"] != 0) | (df["Signal_B"] != 0)]
    print(signals[["Date", "Close", "SMA20", "SMA50", "SMA200", "Signal_A", "Signal_B"]].head(20))
