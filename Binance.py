import time
from binance.client import Client
from binance import ThreadedWebsocketManager

API_KEY = ""  # API_TOKEN
SECRET_KEY = ""  # SECRET_KEY

class Binance:

    def __init__(self):
        self.client = Client(API_KEY, SECRET_KEY)

    def getAllTickers(self):
        ticker = self.client.get_all_tickers()
        symbols = list()
        for symbol in ticker:
            symbols.append(symbol['symbol'])
        return symbols

    #Retorna un listado de cryptomonedas disponibles en Binance
    def getAllCoins(self):
        c = self.client.get_all_coins_info()
        coins = list()
        for coin in c:
            coins.append(coin['coin'])
        return coins

    def getAllCoinsWith(self, fiat):
        ticker = self.client.get_all_tickers()
        coins = list()
        for symbol in ticker:
            coin = symbol['symbol']
            if fiat == coin[-(len(fiat)):]:
                coins.append(symbol['symbol'].replace(fiat, ''))
        return coins

    def getAllCoinsWithUSDT(self):
        return self.getAllCoinsWith('USDT')

    def getAllCoinsWithBTC(self):
        return self.getAllCoinsWith('BTC')

    def getClient(self):
        return self.client

    def getStatus(self):
        return self.client.get_system_status()

    #Devuelve el libro de órdenes de compra y venta.
    #El Bid price es el precio máximo al que un consumidor está dispuesto a comprar
    # El Ask price es el precio mínimo al que un oferente está dispuesto a vender
    def getOrderBook(self,symbol):
        try:
            return self.client.get_order_book(symbol=symbol, limit="1")
        except:
            self.reconnect()
            return self.getOrderBook(symbol)

    def get_mean(self,symbol):
        try:
            return float(self.client.get_avg_price(symbol=symbol)['price'])
        except:
            self.reconnect()
            return self.get_price(symbol)

    def get_price(self, symbol):
        try:
            order_book = self.client.get_order_book(symbol=symbol, limit="1")
            #return buy_price, sell_price
            return float(order_book['asks'][0][0]), float(order_book['bids'][0][0])
        except ConnectionError:
            self.reconnect()
            return self.get_price(symbol)
        except IndexError as e:
            return None, None

    def is_enable(self, symbol):
        return self.client.get_symbol_info(symbol)['status'] == 'TRADING'

    def are_enable(self, symbols, i=0):
        if len(symbols) == i+1:
            return self.is_enable(symbols[i])
        return self.is_enable(symbols[i]) and self.are_enable(symbols, i+1)


    def get_historical_k_lines(self,symbol,interval,start_str,end_str=None):
        return self.client.get_historical_klines(symbol, interval, start_str,end_str)

    def get_k_lines(self,symbol,interval):
        return self.client.get_klines(symbol=symbol, interval=interval)

    def get_symbol_info(self, symbol):
        return self.client.get_symbol_info(symbol)

    def reconnect(self,n=1):
        try:
            if n==1:
                print("Reconectando")
            self.getStatus()
        except:
            time.sleep(1)
            self.reconnect(0)

    def alert(self,msg):
        print('Recibido',msg)



class WebSocketBinance:
    def __init__(self):
        self.ws = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
        self.ws.start()
        self.observers = list()

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, data):
        print(data)
        for observer in self.observers: observer.update(data)

    def add(self, symbol, interval):
        self.ws.start_kline_socket(callback=self.notify, symbol=symbol, interval=interval)
