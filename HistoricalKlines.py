import pandas as pd
from datetime import datetime
from Binance import Binance
from SqueezeMomentumIndicator import *
from Indicator import *
import os

class HistoricalKlines:
    def __init__(self,symbol,interval,start_str,src,end_str=None):
        self.binance = Binance()
        self.klines = pd.DataFrame()
        self.symbol = symbol
        self.interval = interval
        self.start_str = start_str
        self.end_str = end_str
        self.src = src
        self.load()

    def load(self,):
        try:
            assert self.src is not None and os.path.exists(self.src)
            self.klines = pd.read_csv(self.src)
            self.klines.set_index('Time', inplace=True)
        except:
            self._download()
            self._calculate()
            self.klines.set_index('Time', inplace=True)
            self.save()

    def save(self):
        self.klines.to_csv(self.src)

    def getKlines(self):
        return self.klines

    def _download(self):
        colums, times = ['Time','Open','High','Low','Close','Volume','ignore','ignore','ignore','ignore','ignore','ignore'], list()
        self.klines = pd.DataFrame(self.binance.get_historical_k_lines(symbol=self.symbol,interval=self.interval,start_str=self.start_str,end_str=self.end_str),columns=colums)
        [times.append(datetime.fromtimestamp(int(str(time))/1000).strftime('%H:%M %d-%m-%Y')) for time in self.klines['Time']]
        self.klines['Time'] = times
        self.klines = self.klines.drop(['ignore','ignore','ignore','ignore','ignore','ignore'], axis=1)
        self.klines['mean'] = self.klines['Close'].rolling(window=20).mean()
        self.klines[['Open','High','Low','Close','Volume', 'mean']] = self.klines[['Open','High','Low','Close','Volume', 'mean']].astype(float)

    def _calculate(self):
        kline = self.klines
        kline['sm'] = SqueezeMomentumIndicator(kline)
        kline['isSm'] = isSqueeze(kline)
        kline['adx'], kline['di+'], kline['di-'] = adxIndicator(kline)
        kline['rsi'] = rsiIndicator(kline, 20)
        kline['sma'] = smaIndicator(kline, 10)
        kline['sma55'] = smaIndicator(kline, 55)
        kline['ema'] = emaIndicator(kline, 10)
        kline['bbh'], kline['bbm'], kline['bbl'] = bollingerBandsIndicator(kline)
        kline.dropna(inplace=True)
        self.klines = kline

def getMultipleHistoricalKlines(symbols, start_str, end_str, interval):
    kls = dict()
    l = 0
    for symbol in symbols:
        src = f'klines/{symbol}_{start_str}_to_{end_str}_{interval}.csv'
        hk = HistoricalKlines(symbol=symbol, start_str=start_str, end_str=end_str, interval=interval, src=src)
        kl = hk.getKlines()
        kls[symbol] = {'kl': kl}
    kls = matchKL(kls, symbols)
    l = len(kls[symbols[0]]['kl'])
    return kls, l

def cutKL(longKL, shortKL):
    return longKL.loc[shortKL.index[0]:shortKL.index[-1]]

def matchKL(kl,symbol):
    for s1 in symbol:
        for s2 in symbol:
            kl1 = kl[s1]
            kl2 = kl[s2]
            if len(kl1) > len(kl2):
                kl[s1] = cutKL(kl1, kl2)
            elif len(kl1) < len(kl2):
                kl[s2] = cutKL(kl2, kl1)

    return kl