from datetime import datetime


def print_results(df, trader):
    tiempo = datetime.strptime(df.index[-1], '%H:%M %d-%m-%Y') - datetime.strptime(df.index[0], '%H:%M %d-%m-%Y')
    print('#' * 50)
    print(f'SE SIMULARON {int(tiempo.days / 365)} AÑOS, {int((tiempo.days % 365) / 31)} MESES Y{(tiempo.days % 365) % 31 + tiempo.seconds / 86400: .2f} DÍAS')
    print('#' * 50)
    print(trader)

    rendimiento_diario = trader.wallet.rendimiento / (tiempo.days * 100)
    print('#' * 50)
    print('RENDIMIENTO')
    print(f'Diario:{rendimiento_diario: .2%}\nMensual:{rendimiento_diario * 30: .2%}\nAnual:{rendimiento_diario * 365: .2%}')
    print('#' * 50)


def print_trades(trader, make_doc):
    trades = trader.getSummaryTrades()
    print(trades)

    if make_doc:
        doc = open('trades.txt', 'w')
        doc.write(trades)
        doc.close()


