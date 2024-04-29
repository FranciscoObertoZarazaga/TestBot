from Coinbase import CoinBase
from Binance import Binance

coinbase = CoinBase()
binance = Binance()

client = coinbase.get_client()
symbols_cb = coinbase.get_symbol()
symbols_bn = binance.getAllTickers()
symbols = [symbol for symbol in symbols_cb if symbol.replace('-', '') in symbols_bn]
print('Monedas convergentes:', len(symbols))
analizadas = 0
c1 = 0.001
c2 = 0.005
ct = 0#0.082582


def arbitrar(sell_price_cb, buy_price_bn):
    crypto = 100 * (1-c1) / buy_price_bn
    crypto -= ct / buy_price_bn
    usdt = crypto * (1-c2) * sell_price_cb
    return usdt/100


while True:
    for symbol in symbols:
        try:
            buy_price_cb, sell_price_cb = coinbase.get_price(symbol)
            buy_price_bn, sell_price_bn = binance.get_price(symbol.replace('-', ''))
            tasa = arbitrar(sell_price_cb, buy_price_bn)
            if tasa > 1:
                print(symbol, tasa)
            analizadas += 1
        except Exception as e:
            continue

    print('Monedas analizadas:', analizadas)
