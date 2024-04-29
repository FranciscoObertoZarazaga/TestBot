from tools.stop_loss_take_proffit import stop_loss, take_proffit
from tools.print_results import print_results, print_trades
from tools.buy_sell import buy, sell, sell_all
from tools.price_system import PRICE
from Trader import Trader
from Strategy import *
from Point import point


def test(data, imprimir_resultados=1, imprimir_trades=0):
    large = len(data)
    trader = Trader()
    buy_price = None
    max_price = None
    indoor = False

    for i in range(large):
        if i < 2:
            continue

        time = data.index[i]

        ###SISTEMA DE PRECIOS###
        price = PRICE['RANDOM'](data, i)
        ###FIN SISTEMA DE PRECIOS###

        ###ESTRATEGIA###
        points = SqueezeStrategy(data, i)
        ###FIN ESTRATEGIA###

        ###STOP LOSS###
        if indoor:
            if max_price < price:
                max_price = price

            tp_price = take_proffit(price, max_price, buy_price, .95, 1.005)
            if tp_price is not None:
                price, points = tp_price, -1

            sl_price = stop_loss(price, buy_price, .95)
            if sl_price is not None:
                price, points = sl_price, -1
        ###FIN STOP LOSS###

        ###COMPRA y VENTA###
        if points > 0 and not indoor:
            buy_price, max_price, indoor = buy(trader, price, time)
        elif points < 0 and indoor:
            buy_price, max_price, indoor = sell(trader, price, time)
        ###FIN COMPRA y VENTA###

    ###SELL ALL###
    sell_all(data, trader)
    ###FIN SELL ALL###

    ###GENERATE POINTS###
    points = point(trader, data)
    ###FIN GENERATE POINTS###

    ###PRINT RESULTS###
    try:
        if imprimir_resultados:
            print_results(data, trader)
    except:
        print('No se realizaron suficientes trades')
    ###FIN PRINT RESULTS###

    ###PRINT TRADES###
    if imprimir_trades:
        print_trades(trader, make_doc=False)
    ###FIN PRINT TRADES###

    return points
