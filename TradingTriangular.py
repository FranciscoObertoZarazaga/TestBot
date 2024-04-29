from Binance import Binance
from time import sleep
from Wallet import Wallet
from datetime import datetime

binance = Binance()
usdt = 100
wallet = Wallet()
C1 = 'USDT'
C2 = ['BTC']
#C2 = binance.getAllCoinsWith(C1)


def get_triangle(c2):
    par1 = binance.getAllCoinsWith(C1)
    par2 = binance.getAllCoinsWith(c2)
    return [coin for coin in par1 if coin in par2]


def calculate(p12, p13, p23, d=0.999):
    den = p12 * p23
    num = p13 * d**3
    return num/den

def arbitraje(p12, p13, p23, c2, c3):
    wallet.pay(p12, datetime.now, c2)
    wallet.pay(p23, datetime.now, c3, fiat=c2)
    wallet.collect(p13, datetime.now(), c3)


def run(s12, s13, s23, c2, c3, p12):
    try:
        assert binance.are_enable((s12, s13, s23))
        orderbook = binance.client.get_orderbook_tickers()
        symbols = [symbol for symbol in orderbook if symbol['symbol'] in (s13, s23)]
        p13 = float([symbol['bidPrice'] for symbol in symbols if symbol['symbol'] == s13][0])
        p23 = float([symbol['askPrice'] for symbol in symbols if symbol['symbol'] == s23][0])
        rate = calculate(p12, p13, p23)
        assert rate > 1
        p12_ = binance.get_price(s12)[0]
        #assert p12_ <= p12
        arbitraje(p12, p13, p23, c2, c3)
        print('#' * 50)
        print('Tasa:', rate)
        print('Par', s23, round(rate, 4))
        print('Precio compra', p12, 'Precio actual:', p12_)
        print(f'Triangulo de precios ({s12}, {s23}, {s13}):', p12, p23, p13)
        print('#' * 50)
    except Exception as e:
        return

total = 0
for c2 in C2:
    triangle = get_triangle(c2)
    s12 = f'{c2}{C1}'
    p12, _ = binance.get_price(s12)
    total += len(triangle)
    sleep(600)
    for c3 in triangle:
        s13, s23 = f'{c3}{C1}', f'{c3}{c2}'
        #print('Analizando:', (s12, s23, s13))
        run(s12, s13, s23, c3, c2, p12)
    print(wallet)
