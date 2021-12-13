import random
import pandas as pd
from HistoricalKlines import *
from Trader import Trader
from binance.enums import *
from datetime import datetime
from Strategy import *
import warnings
warnings.filterwarnings("ignore")


symbol = ['BTCUSDT']
start_str = '7 year ago'
end_str = None
interval = KLINE_INTERVAL_4HOUR

data, l = getMultipleHistoricalKlines(symbol, start_str, end_str, interval)

for sym in symbol:
    data[sym]['trader'] = Trader()

buy_price = 0
for i in range(l):
    if i < 2 or i >= l:
        continue

    for sym in symbol:
        df = data[sym]['kl']
        trader = data[sym]['trader']
        coin = sym.replace('USDT','')
        price = df['Close'][i]
        #price = random.uniform(df['Low'][i],df['High'][i])
        #price = (df['Low'][i]+df['High'][i]) / 2
        time = df.index[i]
        indoor = trader.indoor

        points = 0
        points += WinStrategy(df, i)

        if points > 0:
            trader.buy(price, time, coin)
            buy_price = price
        elif points < 0:
            trader.sell(price, time, coin)
            buy_price = 0

#sell all
for sym in symbol:
    df = data[sym]['kl']
    trader = data[sym]['trader']
    price = df['Close'][-1]
    time = df.index[-1]
    coin = sym.replace('USDT', '')
    trader.sell(price, time, coin)

trader = Trader()
wallet = trader.wallet
wallet.initial_amount = 0
wallet.setUSDT(0)
for sym in symbol:
    wlt = data[sym]['trader'].wallet
    wallet.addUSDT(wlt.getUSDT())
    wallet.reward += wlt.reward
    wallet.initial_amount += wlt.initial_amount
    wallet.loss += wlt.loss
    wallet.trades = pd.concat([wallet.trades,wlt.trades]).reset_index(drop=True)

kl_aux = data[symbol[0]]['kl']
tiempo = datetime.strptime(kl_aux.index[-1], '%H:%M %d-%m-%Y') - datetime.strptime(kl_aux.index[0], '%H:%M %d-%m-%Y')
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

