from Indicator import smaIndicator

def ssl(df):
    period = 10
    smaHigh = smaIndicator(kline=df, periodo=period, value='High')
    smaLow = smaIndicator(kline=df, periodo=period, value='Low')
    sslDown = list()
    sslUp = list()
    for i in range(len(smaLow)):
        Hlv = hlv(df, smaHigh, smaLow, i)
        sslDown.append(smaHigh[i] if Hlv < 0 else smaLow[i])
        sslUp.append(smaLow[i] if Hlv < 0 else smaHigh[i])
    return sslDown, sslUp

def hlv(df, smaHigh, smaLow, i):
    close = df['Close']
    return 1 if close[i] > smaHigh[i] else (-1 if close[i] < smaLow[i] else hlv(df, smaHigh, smaLow, i-1))
