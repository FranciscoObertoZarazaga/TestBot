def buy(trader, price, time):
    trader.buy(price, time)
    return price, price, True


def sell(trader, price, time):
    trader.sell(price, time)
    return None, None, False


def sell_all(df, trader):
    price = df['High'][-1]
    time = df.index[-1]
    trader.sell(price, time)
