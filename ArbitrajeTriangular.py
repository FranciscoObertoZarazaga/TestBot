from Binance import Binance
from Wallet import Wallet
from datetime import datetime

binance = Binance()
wallet = Wallet()
C1 = 'USDT'
#C2 = ['BTC', 'BNB', 'ETH']
C2 = binance.getAllCoins()
pares_base = binance.getAllCoinsWith(C1)


def get_triangle(c2):
    pares = binance.getAllCoinsWith(c2)
    return [coin for coin in pares_base if coin in pares]


def is_enable(s13, s23):
    status = (
                binance.get_symbol_info(s13)['status'],
                binance.get_symbol_info(s23)['status']
    )
    return status[0] == status[1] == 'TRADING'


def arbitraje(p12, p13, p23, c2, c3):
    wallet.pay(p12, datetime.now, c2)
    wallet.pay(p23, datetime.now, c3, fiat=c2)
    wallet.collect(p13, datetime.now(), c3)


def calculate(p12, p13, p23, d=0.999):
    den = p12 * p23
    num = p13 * d**3
    return num/den


def run(s12, s13, s23, c2, c3):
    try:
        #assert is_enable(s13, s23)
        orderbook = binance.client.get_orderbook_tickers()
        symbols = [symbol for symbol in orderbook if symbol['symbol'] in (s12, s13, s23)]
        p12 = [symbol['bidPrice'] for symbol in symbols if symbol['symbol'] == s12][0]
        p13 = [symbol['askPrice'] for symbol in symbols if symbol['symbol'] == s13][0]
        p23 = [symbol['bidPrice'] for symbol in symbols if symbol['symbol'] == s23][0]
        rate = calculate(p12, p13, p23)
        assert rate > 1
        arbitraje(p12, p13, p23, c2, c3)
        print(c3 + c2, round(rate, 4))
    except Exception as e:
        return


total = 0
for c2 in C2:
    triangle = get_triangle(c2)
    total += len(triangle)
    for c3 in triangle:
        s12, s13, s23 = f'{c2}{C1}', f'{c3}{C1}', f'{c3}{c2}'
        run(s12, s13, s23, c3, c2)
print('Triangulos analizados:', total)
#print(wallet)
print('Terminado')
