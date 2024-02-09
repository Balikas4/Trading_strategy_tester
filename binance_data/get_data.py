import os
import config
import csv
from binance.client import Client
from datetime import datetime

client = Client(config.API_KEY, config.API_SECRET)

csv_file_path = "ETHUSDT-2017-2022-1mth.csv"

timeframes = [
    Client.KLINE_INTERVAL_15MINUTE,
    Client.KLINE_INTERVAL_30MINUTE,
    Client.KLINE_INTERVAL_1HOUR,
    Client.KLINE_INTERVAL_4HOUR,
    Client.KLINE_INTERVAL_1DAY,
    Client.KLINE_INTERVAL_3DAY,
    Client.KLINE_INTERVAL_1WEEK,
    Client.KLINE_INTERVAL_1MONTH
]

for timeframe in timeframes:
    csv_file_path = f"ETHUSDT-2017-2022-{timeframe}.csv"

    # Check if the file already exists
    file_exists = os.path.isfile(csv_file_path)

    # Open the file in write mode, creating it if it doesn't exist
    with open(csv_file_path, "a", newline="") as csvfile:
        candlestick_writer = csv.writer(csvfile, delimiter=",")

        # If the file doesn't exist, write the header row
        if not file_exists:
            header = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
            candlestick_writer.writerow(header)

        candlesticks = client.get_historical_klines("ETHUSDT", timeframe, "1 Jan, 2017", "1 Jan, 2022")

        for candlestick in candlesticks:
            # Convert the timestamp to a datetime object
            dt = datetime.utcfromtimestamp(candlestick[0] / 1000)
            # Format the datetime object as a string
            formatted_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            # Replace the timestamp with the formatted timestamp
            candlestick[0] = formatted_timestamp

            print(candlestick[0])
            candlestick_writer.writerow(candlestick)