from SqueezeMomentumIndicator import *
from Indicator import *
from HistoricalKlines import HistoricalKlines
from Trader import Trader
from binance.enums import *
from datetime import datetime
from Strategy import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


symbol = 'BTCUSDT'
start_str = '7 year ago'
end_str = None
interval = KLINE_INTERVAL_1HOUR
src = 'klines/4hour_kline_btc.csv'

hk = HistoricalKlines(symbol=symbol,start_str=start_str,end_str=end_str, interval=interval,src=src)
kline = hk.getKlines()

kline['sm'] = SqueezeMomentumIndicator(kline)
kline['isSm'] = isSqueeze(kline)
kline['adx'], kline['di+'], kline['di-'] = adxIndicator(kline)
kline['rsi'] = rsiIndicator(kline,20)
kline['sma'] = smaIndicator(kline,10)
kline['ema'] = emaIndicator(kline,10)
kline['bbh'], kline['bbm'], kline['bbl'] = bollingerBandsIndicator(kline)
kline.dropna(inplace=True)

trader = Trader(symbol)

buy_price = 0
signal = list()
for i in range(len(kline)):
    if i < 2 or i >= len(kline):
        signal.append(0)
        continue

    price = kline['Close'][i]
    time = kline.index[i]
    indoor = trader.indoor

    points = 0
    points += WinStrategy(kline, i)
    points -= 1 if price < buy_price * .0 else 0

    if (indoor and points < 0) or (not indoor and points > 0):
        signal.append(points)
    else:
        signal.append(0)

    if points > 0:
        trader.buy(price,time)
        buy_price = price
    elif points < 0:
        trader.sell(price,time)
        buy_price = 0



trader.sell(kline['Close'][-1], kline.index[-1])
kline['signal'] = signal
tiempo = datetime.strptime(kline.index[-1], '%H:%M %d-%m-%Y') - datetime.strptime(kline.index[0], '%H:%M %d-%m-%Y')
print('#'*50)
print(f'SE SIMULARON {int(tiempo.days/365)} AÑOS, {int((tiempo.days % 365) / 31)} MESES Y{(tiempo.days % 365) % 31 + tiempo.seconds/86400: .2f} DÍAS')
print('#'*50)
print(trader)

rendimiento_diario = trader.wallet.rendimiento / (tiempo.days * 100)
print('#'*50)
print('RENDIMIENTO')
print(f'Diario:{rendimiento_diario: .2%}\nMensual:{rendimiento_diario * 30: .2%}\nAnual:{rendimiento_diario * 365: .2%}')
print('#'*50)


exit(0)
trades = trader.getSummaryTrades()

print(trades)

exit(1)
color = list()
size = list()
for i in kline['signal']:
    color.append('red' if i < 0 else ('green' if i > 0 else 'black'))
    size.append(25 if i != 0 else 0)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.plot(kline.index, kline['Close'], linewidth=1)
ax1.scatter(kline.index, kline['Close'],color=color, s=size)
ax2.plot(kline.index, kline['sm'],c='blue')
ax2.plot(kline.index, kline['adx']*100-2000,c='red')
ax2.axhline(y=5, xmin=0.1, xmax=0.9)
plt.show()

