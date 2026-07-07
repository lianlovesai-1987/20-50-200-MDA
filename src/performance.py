"""
performance.py — Phase 5: Performance Analysis & Metrics
=========================================================
Calculates and prints all required backtest metrics.

Required outputs (per working principles):
- Total return %
- Number of trades and win rate
- Maximum drawdown
- Comparison vs. buy-and-hold over the same period
"""

import pandas as pd
import numpy as np


def calculate_max_drawdown(equity_curve: pd.DataFrame) -> float:
    """
    Maximum drawdown = largest peak-to-trough decline in portfolio value.

    Math:
        rolling_max = cumulative maximum of portfolio value up to each day
        drawdown    = (portfolio_value - rolling_max) / rolling_max
        max_dd      = minimum of drawdown series (most negative value)
    """
    values      = equity_curve["Portfolio_Value"]
    rolling_max = values.cummax()
    drawdown    = (values - rolling_max) / rolling_max
    return drawdown.min() * 100  # return as percentage


def calculate_buy_and_hold(df: pd.DataFrame, starting_capital: float = 10_000.0) -> float:
    """
    Buy-and-hold return over the same period.
    Buys at the first available close price, sells at the last.
    """
    start_price = df["Close"].iloc[0]
    end_price   = df["Close"].iloc[-1]
    return (end_price - start_price) / start_price * 100


def print_performance_report(trade_log: pd.DataFrame,
                              equity_curve: pd.DataFrame,
                              df: pd.DataFrame,
                              signal_label: str,
                              starting_capital: float = 10_000.0):
    """
    Print a full performance report to console.
    """
    print(f"\n{'='*55}")
    print(f"  BACKTEST REPORT — {signal_label}")
    print(f"{'='*55}")

    if trade_log.empty:
        print("  No completed trades found.")
        return

    final_value   = equity_curve["Portfolio_Value"].iloc[-1]
    total_return  = (final_value - starting_capital) / starting_capital * 100
    num_trades    = len(trade_log)
    winning       = (trade_log["return_pct"] > 0).sum()
    win_rate      = winning / num_trades * 100 if num_trades > 0 else 0
    max_dd        = calculate_max_drawdown(equity_curve)
    bnh_return    = calculate_buy_and_hold(df, starting_capital)

    print(f"  Period:              {df['Date'].iloc[0].date()} → {df['Date'].iloc[-1].date()}")
    print(f"  Starting Capital:    ${starting_capital:,.2f}")
    print(f"  Final Value:         ${final_value:,.2f}")
    print(f"  Total Return:        {total_return:.2f}%")
    print(f"  Buy & Hold Return:   {bnh_return:.2f}%")
    print(f"  Outperformance:      {total_return - bnh_return:.2f}%")
    print(f"  Number of Trades:    {num_trades}")
    print(f"  Win Rate:            {win_rate:.1f}% ({winning}/{num_trades})")
    print(f"  Max Drawdown:        {max_dd:.2f}%")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    from data_loader import fetch_price_data, validate_price_data
    from indicators  import add_moving_averages
    from signals     import generate_all_signals
    from backtest    import run_backtest

    df = fetch_price_data("SP500")
    df = validate_price_data(df)
    df = add_moving_averages(df)
    df = generate_all_signals(df)

    trades_a, equity_a = run_backtest(df, "Signal_A")
    print_performance_report(trades_a, equity_a, df, "Signal A — SMA20 vs SMA50")

    trades_b, equity_b = run_backtest(df, "Signal_B")
    print_performance_report(trades_b, equity_b, df, "Signal B — SMA50 vs SMA200")
