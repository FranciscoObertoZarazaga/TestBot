import threading
import pandas
import pandas as pd

from HistoricalKlines import *
from binance.enums import *
import warnings
from Test import test
warnings.filterwarnings("ignore")

from Binance import WebSocketBinance
ws = WebSocketBinance()
ws.add('BTCUSDT', '1H')
exit()

'''print('Arbitraje')
from Arbitraje import *
'''
print('Arbitraje triangular')
from ArbitrajeTriangular import *

exit()
bnc = Binance()
coins = bnc.getAllCoinsWithUSDT()
df = pandas.DataFrame(columns=['symbol', 'points'])
for c3 in coins:
    symbol = c3 + 'USDT'
    print('-' * 50, f'\n{symbol}')
    start_str = '1 week ago'
    end_str = None
    interval = KLINE_INTERVAL_5MINUTE

    try:
        data = getHistoricalKlines(symbol, start_str, end_str, interval)
    except:
        continue

    try:
        points = test(data, imprimir_resultados=0)
    except:
        continue
    aux = pd.DataFrame({'symbol': symbol, 'points': points}, index=[0])
    df = pd.concat([df, aux], ignore_index=True)

df = df.sort_values(by='points', axis=0)
print(df)
