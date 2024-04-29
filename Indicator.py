from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from ta.volume import *

def adxIndicator(kline, periodo=14):
    adx = ADXIndicator(kline['High'],kline['Low'],kline['Close'],periodo)
    return adx.adx(), adx.adx_pos(), adx.adx_neg()

def smaIndicator(kline, periodo=50, value="Close"):
    return SMAIndicator(kline[value], periodo).sma_indicator()

def rsiIndicator(kline, periodo=2):
    aux = RSIIndicator(kline['Close'], periodo, False)
    return aux.rsi()


def stochrsiIndicator(kline, periodo=14):
    return stochrsi(kline['Close'], window=periodo, fillna=False)

def bollingerBandsIndicator(kline, periodo=14):
    bb = BollingerBands(kline['Close'], periodo, 2, False)
    return bb.bollinger_hband(), bb.bollinger_mavg(), bb.bollinger_lband()

def aroonIndicator(kline, periodo=25):
    aroon = AroonIndicator(kline['Close'],periodo)
    return aroon.aroon_indicator(), aroon.aroon_up(), aroon.aroon_down()

def cciIndicator(kline):
    cci = CCIIndicator(kline['High'], kline['Low'], kline['Close'])
    return cci.cci()

def emaIndicator(kline, periodos):
    ema = EMAIndicator(kline['Close'], periodos)
    return ema.ema_indicator()

def awesomeOscilatorIndicator(kline):
    ao = AwesomeOscillatorIndicator(kline['High'],kline['Low'])
    return ao.awesome_oscillator()

def kamaIndicator(kline):
    kama = KAMAIndicator(kline['Close'])
    return kama.kama()

def percentagePriceOscillatorIndicator(kline):
    ppo = PercentagePriceOscillator(kline['Close'])
    return ppo.ppo()

def rocIndicator(kline):
    roc = ROCIndicator(kline['Close'])
    return roc.roc()

def stochasticOscillatorIndicator(kline):
    so = StochasticOscillator(kline['Close'],kline['High'],kline['Low'])
    return so.stoch()

def accDistIndexIndicator(kline):
    adi = AccDistIndexIndicator(kline['High'], kline['Low'], kline['Close'], kline['Volume'])
    return adi.acc_dist_index()

def parabolicsarIndicator(kline, step=.02):
    return PSARIndicator(kline['High'], kline['Low'], kline['Close'], step=step, fillna=False)

def atrIndicator(kline, window=14):
    return average_true_range(kline['High'], kline['Low'], kline['Close'], window=window,  fillna=False)

def macdIndicator(kline, fast=12, slow=26, signal=9):
    macd = MACD(kline['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
    return macd.macd(), macd.macd_signal()
