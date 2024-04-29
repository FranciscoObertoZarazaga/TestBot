from Binance import Binance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_df(book):
    return pd.DataFrame(book, columns=['price', 'qty']).astype(float)

def weighted_average(df):
    prod = df['price'] * df['qty']
    return prod.sum() / df['qty'].sum()

def group(df, group_len):
    data_len = len(df)
    assert data_len % group_len == 0
    n_group = int(data_len / group_len)
    data = pd.DataFrame([], columns=['price', 'qty'])

    for i in range(n_group):
        bag = df.iloc[i*group_len:(i+1)*group_len, :]
        qty = bag['qty'].sum()
        price = weighted_average(bag)
        df_aux = pd.DataFrame([[price, qty]], columns=['price', 'qty'])
        data = pd.concat([data, df_aux], ignore_index=True)

    return data

class BookAnalyzer:
    def __init__(self, n_grupos, datos_por_grupo):
        self.binance = Binance()
        self.order_book = self.binance.getOrderBook('BTCUSDT')
        self.bid = get_df(self.order_book['bids'])
        self.ask = get_df(self.order_book['asks'])
        self.datos_por_grupo = datos_por_grupo
        self.n_grupos = n_grupos
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1, figsize=(13,7))

    def model(self, df):
        coefs = np.polyfit(df['price'], df['qty'], self.n_grupos)
        poly = np.poly1d(coefs)
        return poly(df['price'])

    def plot_function(self, df, f):
        self.axes.scatter(df['price'], df['qty'])
        self.axes.plot(df['price'], f)

    def plot_cumulative(self, df):
        self.axes.bar(df['price'], df['cumulative'])


    def run(self):
        ask = group(self.ask, self.datos_por_grupo)
        bid = group(self.bid, self.datos_por_grupo)
        oferta = self.model(ask)
        demanda = self.model(bid)

        self.plot_function(bid, demanda)
        self.plot_function(ask, oferta)
        plt.show()

    def graficar(self):
        oferta = self.model(self.ask)
        demanda = self.model(self.bid)

        self.axes.bar(self.bid['price'], self.bid['qty'])
        self.axes.bar(self.ask['price'], self.ask['qty'])
        plt.show()

    def run_simulation(self):
        price = self.simulate(self.bid, 600)
        print('Movimiento del BID:', self.bid['price'].iloc[0] - price)
        price = self.simulate(self.ask, 600)
        print('Movimiento del ASK:',price - self.ask['price'].iloc[0])

    def run_cumulative(self):
        self.bid['cumulative'] = self.bid['qty'].cumsum()
        self.ask['cumulative'] = self.ask['qty'].cumsum()
        self.plot_cumulative(self.bid)
        self.plot_cumulative(self.ask)
        plt.show()

    #SIMULA una operacion de volumen vol que se descuenta del bid o ask (df) y retorna el precio al que se movió el activo
    def simulate(self, df, vol):
        result = 0
        vol = vol * (-1)
        while not (result > 0) and len(df) > 1:
            qty = df['qty'].iloc[0]
            result = qty + vol
            vol = result
            if not (result > 0):
                df = df.iloc[1:]

        return df['price'].iloc[0]


