"""
backtest.py — Phase 4: Trade Simulation & P&L Tracking
========================================================
Simulates trades based on generated signals and tracks P&L.

Assumptions (stated explicitly as per working principles):
- Starting capital: $10,000
- Position sizing: 100% of capital deployed on each BUY signal (fully invested)
- Transaction costs: $0 (base case — flagged here for transparency)
- Signals A and B are tested SEPARATELY by default
- Trades execute at the closing price on the signal day
- Only one position open at a time (no pyramiding)
"""

import pandas as pd


def run_backtest(df: pd.DataFrame,
                 signal_col: str,
                 starting_capital: float = 10_000.0) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Simulate trades based on a signal column and return trade log + equity curve.

    Parameters
    ----------
    df               : pd.DataFrame with ['Date', 'Close', signal_col]
    signal_col       : column name containing 1 (BUY), -1 (SELL), 0 (hold)
    starting_capital : initial cash in dollars

    Returns
    -------
    trade_log    : pd.DataFrame — one row per completed trade
    equity_curve : pd.DataFrame — daily portfolio value
    """
    cash       = starting_capital
    shares     = 0.0
    in_trade   = False
    entry_price = 0.0
    entry_date  = None
    trades      = []
    equity      = []

    for _, row in df.iterrows():
        date  = row["Date"]
        price = row["Close"]
        sig   = row[signal_col]

        # BUY signal — only enter if not already in a trade
        if sig == 1 and not in_trade:
            shares      = cash / price
            cash        = 0.0
            in_trade    = True
            entry_price = price
            entry_date  = date

        # SELL signal — only exit if we're in a trade
        elif sig == -1 and in_trade:
            cash     = shares * price
            pnl      = cash - starting_capital if not trades else cash - (trades[-1]["exit_value"])
            trade_return = (price - entry_price) / entry_price * 100
            trades.append({
                "entry_date":   entry_date,
                "exit_date":    date,
                "entry_price":  entry_price,
                "exit_price":   price,
                "return_pct":   round(trade_return, 4),
                "hold_days":    (date - entry_date).days,
            })
            shares   = 0.0
            in_trade = False

        # Daily portfolio value
        portfolio_value = cash + shares * price
        equity.append({"Date": date, "Portfolio_Value": portfolio_value})

    trade_log    = pd.DataFrame(trades)
    equity_curve = pd.DataFrame(equity)
    return trade_log, equity_curve


if __name__ == "__main__":
    from data_loader import fetch_price_data, validate_price_data
    from indicators  import add_moving_averages
    from signals     import generate_all_signals

    df = fetch_price_data("SP500")
    df = validate_price_data(df)
    df = add_moving_averages(df)
    df = generate_all_signals(df)

    print("\n--- Signal A Backtest (SMA20 vs SMA50) ---")
    trades_a, equity_a = run_backtest(df, signal_col="Signal_A")
    print(trades_a)

    print("\n--- Signal B Backtest (SMA50 vs SMA200) ---")
    trades_b, equity_b = run_backtest(df, signal_col="Signal_B")
    print(trades_b)
