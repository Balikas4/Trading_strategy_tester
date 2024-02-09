# Trading Strategy Backtesting with Backtrader
Inspired by: lth-elm L41TH
https://github.com/lth-elm/Backtrading-Python-Binance?tab=readme-ov-file

## Overview

This Python script utilizes the Backtrader library to backtest a trading strategy based on Relative Strength Index (RSI) and Bollinger Bands. The strategy is applied to historical price data of the Ethereum/USDT trading pair on the Binance exchange.

## Script Components

### 1. Data Collection

The script fetches historical price data for Ethereum/USDT from Binance for various timeframes, including 15 minutes, 30 minutes, 1 hour, 4 hours, 1 day, 3 days, 1 week, and 1 month.

### 2. Backtesting Strategy

The main strategy, `RSIBBStrategy`, is based on a combination of RSI and Bollinger Bands. The script defines buy and sell signals based on these indicators. Notably, the strategy dynamically adjusts the order size based on portfolio value and existing positions.

### 3. Timeframe Iteration

The script iterates over multiple timeframes, running the backtest for each. After running the strategy on each timeframe, the script prints the starting and ending portfolio values for analysis.

## Results

After executing the script, the printed results provide insights into the performance of the trading strategy across different timeframes. The "Starting Portfolio Value" and "Ending Portfolio Value" for each timeframe indicate the potential profitability of the strategy.

## Debugging

If the strategy does not behave as expected, consider debugging by reviewing the order size calculations, position checks, and conditions for buying/selling. Print relevant values at each step to identify potential issues.

## Further Enhancements

To further improve the script, you may consider:
- Fine-tuning strategy parameters.
- Adding additional technical indicators.
- Implementing risk management strategies.

Remember to thoroughly test any modifications to ensure the robustness of the trading strategy.

## How to Run

1. Install required Python packages using the following command in your terminal:

   ```bash
   pip install -r requirements.txt
2. Update Binance API key and secret in the `config.py` file.
3. Run the script: `get_data.py` in binance_data folder. This will take a few minutes since we're downloading 300 000 rows of data. 
4. Run the script: `rsi_boll_backtest_all_timeframes.py` to get trading strategy results on most popular timeframes.

Happy trading!
