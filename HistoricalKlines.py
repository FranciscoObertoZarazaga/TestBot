import pandas as pd
from datetime import datetime
from Binance import Binance
from indicators.SqueezeMomentumIndicator import *
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
        kline['rsi'] = rsiIndicator(kline, 2)
        kline['stochrsi'] = stochrsiIndicator(kline)
        kline['psar'] = parabolicsarIndicator(kline)
        kline['sma'] = smaIndicator(kline, 200)
        kline['ema'] = emaIndicator(kline, 200)
        kline['bbh'], kline['bbm'], kline['bbl'] = bollingerBandsIndicator(kline)
        kline['atr'] = atrIndicator(kline)
        kline['macd'], kline['macd_signal'] = macdIndicator(kline)
        kline.dropna(inplace=True)
        self.klines = kline


def getHistoricalKlines(symbol, start_str, end_str, interval):
    src = f'klines/{symbol}_{start_str}_to_{end_str}_{interval}.csv'
    hk = HistoricalKlines(symbol=symbol, start_str=start_str, end_str=end_str, interval=interval, src=src)
    kl = hk.getKlines()
    return kl

def kline_fusion(long_data, short_data,):
    group = dict()
    for i, time1 in enumerate(long_data.index):
        kline = dict()
        long_time = datetime.strptime(time1, '%H:%M %d-%m-%Y')
        subdata = short_data[short_data.index >= long_time]
        if i >= len(long_data) - 1:
            kline.update({'data': long_data.iloc[i], 'subdata': subdata})
            group.update({long_time: kline})
            continue
        long_time_future = datetime.strptime(long_data.index[i + 1], '%H:%M %d-%m-%Y')
        subdata = subdata[subdata.index < long_time_future]
        kline.update({'data': long_data.iloc[i], 'subdata': subdata})
        group.update({long_time: kline})
    return group

def get_subdata(data, i, subdata):
    long_time = datetime.strptime(data.index[i-1], '%H:%M %d-%m-%Y')
    subdata = subdata[subdata.index >= long_time]
    if i >= len(data) - 1:
        return subdata
    long_time_future = datetime.strptime(data.index[i + 1], '%H:%M %d-%m-%Y')
    subdata = subdata[subdata.index < long_time_future]
    return subdata
