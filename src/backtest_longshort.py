"""
backtest_longshort.py — Long/Short Trade Simulation
=====================================================
Upward cross  → LONG  (+1): profit when market rises
Downward cross → SHORT (-1): profit when market falls
Always in the market after the first signal.

Math (no look-ahead bias):
    r_strategy(t) = position(t-1) * r_market(t)
    equity(t)     = starting_capital * cumulative_product(1 + r_strategy)
    Position changes take effect from the NEXT day's return,
    since the signal is only known at that day's close.

Assumptions:
- Starting capital: $10,000, 100% of equity per position
- No transaction costs, no margin/borrow costs on shorts
- Signals A and B tested separately
"""

import pandas as pd
import numpy as np


def run_backtest_longshort(df: pd.DataFrame,
                           signal_col: str,
                           starting_capital: float = 10_000.0):
    """
    Long/short backtest. Returns (trade_log, equity_curve).
    """
    df = df.reset_index(drop=True).copy()

    # Build position series: +1 after BUY, -1 after SELL, carry forward
    position = df[signal_col].replace(0, np.nan).ffill().fillna(0)

    # Daily market return
    mkt_ret = df["Close"].pct_change().fillna(0)

    # Strategy return: yesterday's position × today's market return
    strat_ret = position.shift(1).fillna(0) * mkt_ret

    equity = starting_capital * (1 + strat_ret).cumprod()
    equity_curve = pd.DataFrame({"Date": df["Date"], "Portfolio_Value": equity})

    # ── Trade log: one row per position leg (long or short) ──
    trades = []
    entry_i = None
    entry_dir = 0
    for i in range(len(df)):
        sig = df.loc[i, signal_col]
        if sig != 0:
            if entry_i is not None and sig != entry_dir:
                # close previous leg
                ep, xp = df.loc[entry_i, "Close"], df.loc[i, "Close"]
                direction = "LONG" if entry_dir == 1 else "SHORT"
                ret = (xp - ep) / ep * 100 if entry_dir == 1 else (ep - xp) / ep * 100
                trades.append({
                    "direction":   direction,
                    "entry_date":  df.loc[entry_i, "Date"],
                    "exit_date":   df.loc[i, "Date"],
                    "entry_price": round(ep, 2),
                    "exit_price":  round(xp, 2),
                    "return_pct":  round(ret, 4),
                    "hold_days":   (df.loc[i, "Date"] - df.loc[entry_i, "Date"]).days,
                })
            entry_i, entry_dir = i, sig

    # Close final open leg at last price (mark-to-market)
    if entry_i is not None and entry_i < len(df) - 1:
        i = len(df) - 1
        ep, xp = df.loc[entry_i, "Close"], df.loc[i, "Close"]
        direction = "LONG" if entry_dir == 1 else "SHORT"
        ret = (xp - ep) / ep * 100 if entry_dir == 1 else (ep - xp) / ep * 100
        trades.append({
            "direction": direction, "entry_date": df.loc[entry_i, "Date"],
            "exit_date": df.loc[i, "Date"], "entry_price": round(ep, 2),
            "exit_price": round(xp, 2), "return_pct": round(ret, 4),
            "hold_days": (df.loc[i, "Date"] - df.loc[entry_i, "Date"]).days,
        })

    return pd.DataFrame(trades), equity_curve
