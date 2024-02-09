import backtrader as bt
import pandas as pd

# Load CSV data into pandas DataFrame

timeframes = ['15m', '30m', '1h', '4h', '1d', '3d', '1w', '1M']

for timeframe in timeframes:
    df = pd.read_csv(f'binance_data/ETHUSDT-2017-2022-{timeframe}.csv', parse_dates=True, index_col='timestamp')

    # Define the RSI strategy class
    class RSIBBStrategy(bt.Strategy):
        params = (
            ("rsi_period", 14),
            ("rsi_overbought", 70),
            ("rsi_oversold", 30),
            ("bollinger_period", 20),
        )

        def __init__(self):
            self.closes = []
            self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
            self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.bollinger_period)

        def next(self):
            self.closes.append(self.data.close[0])
            last_rsi = self.rsi[0]
            last_low_boll = self.bollinger.lines.bot[0]
            last_up_boll = self.bollinger.lines.top[0]

            if last_rsi < self.params.rsi_oversold and last_low_boll < self.data.close[0]:
                # Buy big signal
                order_size = self.calculate_order_quantity_buy()
                # print(f"Buying big {order_size} shares.")
                self.buy(size=order_size)
            elif last_rsi < self.params.rsi_oversold or last_low_boll < self.data.close[0]:
                # Buy small signal
                order_size = self.calculate_order_quantity_buy()
                # print(f"Buying small {order_size} shares.")
                self.buy(size=order_size)
            if last_rsi > self.params.rsi_overbought and last_up_boll < self.data.close[0]:
                # Sell big signal
                order_size = self.calculate_order_quantity_sell()
                # print(f"Selling big {order_size} shares.")
                self.sell(size=order_size)
            elif last_rsi > self.params.rsi_overbought or last_up_boll < self.data.close[0]:
                # Sell small signal
                order_size = self.calculate_order_quantity_sell()
                # print(f"Selling small {order_size} shares.")
                self.sell(size=order_size)

        def calculate_order_quantity_buy(self):
            # Calculate buy order quantity based on the cash of the portfolio
            value = self.broker.get_cash()
            # print("Current cash:", value)

            if value > 10:
                order_size = min(value / self.closes[0], value) * 0.1
                order_size = round(order_size, 8)  # Adjust the rounding based on your requirements
                # print(f"Buy order size: {order_size}")
                return order_size
            else:
                print("Not enough cash to buy.")
                return 0

        def calculate_order_quantity_sell(self):
            position = self.broker.getposition(data=self.data)
            # Calculate sell order quantity based on the asset of the portfolio
            if position:
                # Calculate sell order quantity based on 50% of the current position size
                order_size = float(position.size * 0.1)
                # print(f"Current position size: {position.size}")
                return round(order_size, 8)
            else:
                print("No position to sell.")
                return 0

    # Convert the pandas DataFrame to Backtrader data feed
    data = bt.feeds.PandasData(dataname=df)

    # Create a Backtrader Cerebro engine
    cerebro = bt.Cerebro()

    # Add the data feed to Cerebro
    cerebro.adddata(data)

    # Add the strategy to Cerebro
    cerebro.addstrategy(RSIBBStrategy)

    # Set the initial cash amount for backtesting
    cerebro.broker.set_cash(100000)

    # Print the starting cash amount
    print(f"Starting Portfolio Value for {timeframe}: {cerebro.broker.getvalue()}")

    # Run the backtest
    cerebro.run()

    # Print the final cash amount
    print(f"Ending Portfolio Value for {timeframe}: {cerebro.broker.getvalue()}")
