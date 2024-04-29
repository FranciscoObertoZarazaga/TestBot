import random

def SqueezeStrategy(df, n):
    sm = df['sm']

    isMin = sm[n] > sm[n - 1] and sm[n - 2] > sm[n - 1]
    isMax = sm[n] < sm[n - 1] and sm[n - 2] < sm[n - 1]
    if isMin:
        return 1
    '''if isMax:
        return -1'''
    return 0

def SqueezeBusterStrategy(df, n):
    sm = df['sm']
    up = sm[n] > sm[n - 1]
    down = sm[n] < sm[n - 1]
    atr = df['atr'][n]
    price = df['Close'][n]
    volatilidad_relativa = atr * 100 / price
    if random.randint(0,100) > 100:
        up, down = down, up
    if up and volatilidad_relativa > 0.5:
        return 1
    if down:
        return -1
    return 0

def RSIStratygy(df,n):
    rsi = df['rsi']
    '''if rsi[n] > 70:
        return -1'''
    if rsi[n-1] < 30 and rsi[n] > 30:
        return 1
    return 0

def BBStrategy(df, n):
    price = df['Close'][n]
    bbl = df['bbl'][n]
    bbh = df['bbh'][n]
    if price < bbl:
        return 1
    if price > bbh:
        return -1
    return 0

def TrendStrategy(df,t):
    price = df['Close']
    if price[t] > price[t-1]:
        return 1
    else:
        return -1


def WinStrategy(df, n):
    adx = df['adx']
    sm = df['sm']
    sma = df['sma']
    di_pos = df['di+']
    di_neg = df['di-']
    price = df['Close']
    isMin = adx[n] > adx[n-1] and adx[n-2] > adx[n-1]
    isMax = adx[n] < adx[n - 1] and adx[n - 2] < adx[n - 1]
    isUp = price[n] > sma[n]
    isMagic = sm[n] > sm[n-1]

    if isMin:
        if adx[n-1] < 30:
            if isMagic:
                return 1
            if isUp:
                return 1
            return -1

    '''
    if adx[n] < 30:
        if isUp and price[n-1] < sma[n-1] and isMagic:
            return 1
    '''

    return 0

def GodStrategy(df, n, y=None):
    price = df['Close']
    #y = price[n] < price[n+1]
    if y == None:
        return 0
    if price[n] < price[n-1] and y:
        return 1
    if price[n] > price[n-1] and not y:
        return -1
    return 0

def NovechentaStrategy(df,t):
    adx = df['adx']
    sm = df['sm']

    #Si el adx alcanza un mínimo o un máximo
    if (adx[t] < adx[t-1] and adx[t-2] < adx[t-1]) or (adx[t] > adx[t-1] and adx[t-2] > adx[t-1]):
        #Si el monitor es bajista con direccion alcista
        if sm[t] > sm[t-1] and sm[t] < 0:
            #Compro
            return 1
        #Si el monitor es alcista con direccion bajista
        if sm[t] < sm[t-1] and sm[t] > 0:
            #Vendo
            return -1
    return 0


def GeranatorStrategy(df, n):
    adx = df['adx']
    sm = df['sm']
    di_pos = df['di+']
    di_neg = df['di-']
    isMin = adx[n] > adx[n - 1] and adx[n - 2] > adx[n - 1]
    if isMin:
        if adx[n] < 30 and adx[n] > 20:
            if di_pos[n] > di_neg[n]:
                return 1
            if di_pos[n] < di_neg[n]:
                return -1
    return 0

def new_strategy(df, n):
    sm = df['sm']
    is_sm = df['isSm']
    if is_sm[n] and sm[n] > 0:
        return 1
    return 0

def ssl_strategy(df, n, buy_price):
    smaLow, smaHigh = df['smaLow'], df['smaHigh']
    macd, macd_signal = df['macd'], df['macd_signal']
    if smaHigh[n] > smaLow[n] and macd[n] > macd_signal[n] and df['Close'][n] > df['ema'][n]:
        return 1

    if buy_price == None:
        return 0

    if smaHigh[n] < smaLow[n] and smaHigh[n-1] > smaLow[n-1] and df['Close'][n] > buy_price:
        return -1

    return 0

def rsi_two_periods(df, n):
    price = df['Close'][n]
    ema = df['ema'][n]

    if price > ema and df['rsi'][n] > 10 and df['rsi'][n-1] < 10:
        return 1

    return 0






