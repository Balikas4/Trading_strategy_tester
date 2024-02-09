import backtest, csv, os
from pathlib import Path

def write_results_csv(writer, datapath, start, end, strategy, period, commission_val, portofolio, stake_val, quantity, plot):
    end_val, totalwin, totalloss, pnl_net, sqn = backtest.runbacktest(
        datapath, start, end, period, strategy, commission_val, portofolio, stake_val, quantity, plot)
    profit = (pnl_net / portofolio) * 100

    # view the data in the console while processing
    print('data processed: %s, %s (Period %d) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' %
          (datapath[5:], strategy, period, end_val, totalwin, totalloss, sqn))

    writer.writerow([sep[0], sep[3], start, end, strategy, period, round(end_val, 3), round(profit, 3), totalwin, totalloss, sqn])

commission_val = 0.04 # 0.04% taker fees binance usdt futures
portofolio = 10000.0 # amount of money we start with
stake_val = 1
quantity = 0.10 # percentage to buy based on the current portofolio amount
# here it would correspond to a unit equivalent to 1000$ if the value of our portofolio didn't change

start = '2017-01-01'
end = '2022-01-01'
strategies = ['BB', 'RSI']
periodRange = range(10, 31)
plot = False

commission_val = 0.04
portofolio = 10000.0
stake_val = 1
quantity = 0.10
start = '2017-01-01'
end = '2022-01-01'
strategies = ['BB', 'RSI']
periodRange = range(10, 31)
plot = False

for strategy in strategies:
    for data in os.listdir("./binance_data"):
        datapath = Path('./binance_data') / data

        sep = datapath.stem.split('-')  # ignore name file 'data/' and '.csv'

        print('\n ------------ ', datapath)
        print()
        print('Strategy:', strategy)
        dataname = f'result/{strategy}-{sep[0]}-{start.replace("-","")}-{end.replace("-","")}-{sep[3]}.csv'

        print("File path:", dataname)
        with open(dataname, 'w', newline='') as csvfile:
            result_writer = csv.writer(csvfile, delimiter=',')
            result_writer.writerow(
                ['Pair', 'Timeframe', 'Start', 'End', 'Strategy', 'Period', 'Final value', '%', 'Total win', 'Total loss', 'SQN'])  # init header

            for period in periodRange:
                write_results_csv(result_writer, datapath, start, end, strategy, period, commission_val, portofolio, stake_val, quantity, plot)
        csvfile.close()