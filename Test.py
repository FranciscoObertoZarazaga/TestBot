from Strategy import WinStrategy

def subtrade(subdata, trader):
    for j in range(len(subdata)):
        if j < 5:
            continue
        points = WinStrategy(subdata, j)

        price = subdata['Close'][j]
        # price = random.uniform(df['Low'][i],df['High'][i])
        # price = (df['Low'][i]+df['High'][i]) / 2
        time = subdata.index[j]

        if points > 0:
            trader.buy(price, time)
        elif points < 0:
            trader.sell(price, time)


def get_macro(data, i):
    if i == 0:
        return False
    result = WinStrategy(data, i)
    if result == 1:
        return True
    elif result == -1:
        return False
    else:
        return get_macro(data, i-1)
