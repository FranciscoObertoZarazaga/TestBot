from datetime import datetime
def point(trader, data):
    wallet = trader.wallet
    tiempo = datetime.strptime(data.index[-1], '%H:%M %d-%m-%Y') - datetime.strptime(data.index[0], '%H:%M %d-%m-%Y')
    wallet.trades['tasa'] = wallet.trades['final'] / wallet.trades['inicial'] - 1

    acertabilidad = (1 - abs(wallet.loss) / (abs(wallet.loss) * 2 + wallet.reward))
    multiplicador = (wallet.getUSDT() / wallet.initial_amount)

    n_trades = len(wallet.trades['reward'])
    tasa_de_aciertos = get_tasa_de_aciertos(wallet, n_trades)
    mean_rate = wallet.trades['tasa'].mean()
    rendimiento_diario = mean_rate * n_trades / (tiempo.days)
    points = ((wallet.trades['tasa'].mean() + 1) / 2) * ((rendimiento_diario + 1) / 2) * tasa_de_aciertos * acertabilidad * multiplicador / n_trades
    print(points*100)
    return points

def get_tasa_de_aciertos(wallet, n_trades):
    n_positive_trades = len(wallet.trades[wallet.trades['reward'] >= 0])
    n_negative_trades = n_trades - n_positive_trades
    return n_negative_trades/n_positive_trades
