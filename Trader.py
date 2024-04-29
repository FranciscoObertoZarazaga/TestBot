import pandas as pd

from Binance import *
from Wallet import *
import numpy as np

class Trader:

    def __init__(self):
        self.wallet = Wallet()
        self.indoor = False
        self.buy_price = 0

    def buy(self,price, time, coin='BTC'):
        if self.wallet.isPayable():
            self.wallet.pay(price,time, coin)
            self.indoor = True
            self.buy_price = price


    def sell(self,price, time, coin='BTC'):
        if self.wallet.isPositive(coin):
            reward = self.wallet.collect(price, time, coin)
            self.indoor = False
            return reward


    def wait(self):
        time.sleep(0)

    def switch(self):
        try:
            return self.buy()
        except:
            return self.sell()

    def __str__(self):
        return str(self.wallet)

    def getSummaryTrades(self, negative_only=False):
        trades = self.wallet.trades
        trades = trades[trades['reward'] < 0] if negative_only else trades
        trades.to_csv('trades.csv')
        titulos = ['COMPRA', 'VENTA']
        columnas = ['Monto', 'Precio', 'Fecha y Hora']
        msg = '\n' + '_' * 132 + '\n'
        msg += f'|{"ID": ^5}|'
        for titulo in titulos:
            msg += f'|{titulo: ^52}|'
        msg += f'|{"RESULTADO": ^15}|'
        msg += f'\n|{" ": >5}|'
        for _ in range(2):
            for columna in columnas:
                msg += f'|{columna: ^16}|'
        msg += f'|{" ": >15}|\n'
        msg += '-' * 132 + '\n'
        for i, row in trades.iterrows():
            id = i
            monto_inicial = row['inicial']
            precio_compra = row['buy_price']
            tiempo_compra = row['buy_time']
            monto_final = row['final']
            precio_venta = row['sell_price']
            tiempo_venta = row['sell_time']
            ganancia = row['reward']
            msg += f'|{id : ^5}|'
            msg += f'|{monto_inicial : ^16.2f}|'
            msg += f'|{precio_compra : ^16.2f}|'
            msg += f'|{tiempo_compra}|'
            msg += f'|{monto_final : ^16.2f}|'
            msg += f'|{precio_venta : ^16.2f}|'
            msg += f'|{tiempo_venta}|'
            msg += f'|{ganancia : ^7.2f}|'
            msg += f'|{monto_final/monto_inicial-1 : ^7.2%}|'
            msg += '\n'
        return msg


















