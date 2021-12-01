import numpy as np

def cagr(wallet,time):
    inicial = wallet.initial_amount
    final = wallet.usdt
    years = time.days / 365
    return (final/inicial)**(1/years) - 1

def volatilidad(trades, time):
    t = len(trades) / time.days
    return trades['tasa'].std() * np.sqrt(365 * t)


def SharpeRatio(cagr, vol, riskfree_rate = 0.022):
    return (cagr - riskfree_rate) / vol

def SortinoRatio(cagr,trades, time,riskfree_rate = 0.022):
    t = len(trades[trades['tasa'] < 0]['tasa']) / time.days
    neg_vol = trades[trades['tasa'] < 0]['tasa'].std() * np.sqrt(365 * t)
    return (cagr - riskfree_rate) / neg_vol
