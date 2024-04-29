import cbpro

PASS_PHRASE = 'idzrtm87v1q'
SECRET_KEY = 'v3GFzWxgjs6S5zx5L2jwBL/qJL2aA8035KTs+sJVDnOUdSjZnwTj9TdEUGNn73cauhL7M6ef7e4QPvatT4q7VA=='
PUBLIC_KEY = '5dd487854254e14de3ae709a05930d1d'


class CoinBase:

    def __init__(self):
        self.client = cbpro.AuthenticatedClient(PUBLIC_KEY, SECRET_KEY, PASS_PHRASE)

    def get_price(self, symbol):
        order_book = self.client.get_product_order_book(symbol, level=1)
        # return buyPrice, sellPrice
        return float(order_book['asks'][0][0]), float(order_book['bids'][0][0])

    def get_client(self):
        return self.client

    def get_symbol(self):
        symbols = self.client.get_products()
        return [symbol['id'] for symbol in symbols]
