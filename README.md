# 20/50/200 MDA Trading Strategy Backtester

## Objective
Backtest a moving-average crossover strategy on major stock indices using publicly available historical data, and report overall returns.

## Strategy Logic
- **Signal A:** 20-day MA crosses the 50-day MA
- **Signal B:** 50-day MA crosses the 200-day MA
- Upward cross (shorter MA crosses above longer MA) = **BUY**
- Downward cross (shorter MA crosses below longer MA) = **SELL**

## Data
Use publicly available historical price data for major indices (start with S&P 500, then Dow Jones). Always validate data for completeness and gaps before running any test.

## Approach
- Build the logic in clean, well-commented Python (pandas for data, numpy for math).
- Calculate MAs, detect crossovers programmatically, generate signals, then simulate trades.
- Track entry/exit prices, hold periods, and per-trade P&L.

## Required Outputs for Every Backtest
- Total return %
- Number of trades and win rate
- Maximum drawdown
- Comparison vs. buy-and-hold over the same period

## Working Principles
- Keep it simple; prioritize correctness over cleverness.
- State every assumption (starting capital, position sizing, transaction costs, whether signals A and B are tested separately or combined).
- Show the math before running it so it can be verified.
- Flag any look-ahead bias or data issues proactively.

## Project Roadmap
| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Data acquisition & validation | 🔜 Next |
| 2 | Moving average calculation | ⏳ Pending |
| 3 | Signal generation (crossover detection) | ⏳ Pending |
| 4 | Trade simulation & P&L tracking | ⏳ Pending |
| 5 | Performance analysis & metrics | ⏳ Pending |
| 6 | Multi-index validation (Dow Jones) | ⏳ Pending |

## Project Structure
```
20-50-200-MDA/
├── README.md
├── requirements.txt
├── data/
│   └── .gitkeep          # Raw & validated historical price data
├── src/
│   ├── data_loader.py    # Phase 1: Fetch & validate price data
│   ├── indicators.py     # Phase 2: Moving average calculations
│   ├── signals.py        # Phase 3: Crossover detection & signal generation
│   ├── backtest.py       # Phase 4: Trade simulation & P&L tracking
│   └── performance.py    # Phase 5: Metrics & reporting
├── results/
│   └── .gitkeep          # Backtest output CSVs and reports
└── notebooks/
    └── .gitkeep          # Exploratory analysis notebooks
```
