import random
import pandas as pd
from HistoricalKlines import *
from Trader import Trader
from binance.enums import *
from datetime import datetime
from Strategy import *
from Test import *
import warnings
warnings.filterwarnings("ignore")


symbol = 'BTCUSDT'
start_str = '1 week ago'
end_str = None
interval = KLINE_INTERVAL_5MINUTE

data = getHistoricalKlines(symbol, start_str, end_str, interval)

interval = KLINE_INTERVAL_1MINUTE
subdata = getHistoricalKlines(symbol, start_str, end_str, interval)

subdata.index = pd.to_datetime(subdata.index, format='%H:%M %d-%m-%Y')

large = len(data)
trader = Trader()

buy_price = 0

for i in range(large):
    if i < 4 or i >= large:
        continue

    macro = get_macro(data, i)
    if macro:
        subtrade(get_subdata(data, i, subdata), trader)


#sell all
price = data['Close'][-1]
time = data.index[-1]
trader.sell(price, time)

tiempo = datetime.strptime(time, '%H:%M %d-%m-%Y') - datetime.strptime(data.index[0], '%H:%M %d-%m-%Y')
print('#'*50)
print(f'SE SIMULARON {int(tiempo.days/365)} AÑOS, {int((tiempo.days % 365) / 31)} MESES Y{(tiempo.days % 365) % 31 + tiempo.seconds/86400: .2f} DÍAS')
print('#'*50)
print(trader)

rendimiento_diario = trader.wallet.rendimiento / (tiempo.days * 100)
print('#'*50)
print('RENDIMIENTO')
print(f'Diario:{rendimiento_diario: .2%}\nMensual:{rendimiento_diario * 30: .2%}\nAnual:{rendimiento_diario * 365: .2%}')
print('#'*50)

exit(1)
trades = trader.getSummaryTrades()
print(trades)

