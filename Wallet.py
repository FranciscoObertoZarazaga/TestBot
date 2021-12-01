import pandas as pd
from Binance import Binance

class Wallet:

    def __init__(self,symbol):
        self.reward = 0
        self.crypto = 0
        self.initial_amount = 100
        self.usdt = self.initial_amount
        self.binance = Binance()
        self.symbol = symbol
        self.buy_amount = 0
        self.buy_price = 0
        self.buy_time = None
        self.loss = 0
        self.trades = pd.DataFrame(columns=['final','inicial','reward'])

    def pay(self, price,time, percentage=1):
        amount = self.usdt * percentage
        assert self.usdt >= amount
        self.buy_amount += amount
        self.buy_price = price
        self.crypto += (amount * 0.999) / self.buy_price
        self.usdt -= amount
        self.buy_time = time

    def collect(self, price, time):
        assert self.crypto > 0
        sell_price = price
        reward = self.crypto * sell_price * 0.999 - self.buy_amount
        self.usdt += reward + self.buy_amount
        self.reward += reward
        self.loss += reward if reward < 0 else 0
        trade = {'final': self.usdt, 'inicial': self.buy_amount, 'reward': reward, 'buy_price': self.buy_price, 'sell_price': price, 'buy_time': self.buy_time, 'sell_time': time}
        self.trades = self.trades.append(trade, ignore_index=True, )
        self.crypto = 0
        self.buy_amount = 0
        return self.reward

    def __str__(self):
        trades = self.trades.copy()
        trades['tasa'] = trades['final'] / trades['inicial'] - 1
        n_trades = len(trades['reward'])
        n_positive_trades = len(trades[trades['reward'] >= 0])
        n_negative_trades = n_trades - n_positive_trades
        positive_rate = trades[trades['tasa'] >= 0]['tasa'].mean() * 100
        negative_rate = trades[trades['tasa'] < 0]['tasa'].mean() * 100
        mean_rate = trades['tasa'].mean() * 100
        self.rendimiento = mean_rate * n_trades


        msg = '=' * 50 + '\n' + "{:^50}".format('RESULTADO') + '\n' + '=' * 50 + '\n'
        ganancia_bruta = self.reward + abs(self.loss)
        tasa_de_aciertos = 100 * (1 - abs(self.loss) / (abs(self.loss) * 2 + self.reward))
        tasa_de_ganancia = (self.usdt / self.initial_amount)

        titulo = ['Monto Inicial', 'Monto Final', 'Crypto Final', 'Ganancia Bruta', 'Pérdida', 'Ganancia Neta', 'Acertabilidad','Multiplicador','N° de Trades', 'N° de Trades Positivos', 'N° de Trades Negativos', 'Tasa de Aciertos', 'Tasa Promedio', 'Tasa de Ganancia Promedio', 'Tasa de Pérdida Promedio','Rendimiendo']
        valor = [self.initial_amount, self.usdt,self.crypto, ganancia_bruta,self.loss,self.reward,tasa_de_aciertos,tasa_de_ganancia,n_trades, n_positive_trades, n_negative_trades, n_negative_trades/n_positive_trades, mean_rate, positive_rate, negative_rate, self.rendimiento]
        unidad = ['U$DT', 'U$DT', 'BTC', 'U$DT', 'U$DT', 'U$DT', '%', '', '', '', '', 'N/P', '%', '%', '%', '%']
        for i,t in enumerate(titulo):
            msg += f'{t:<30}{valor[i]: >10.2f} {unidad[i]: <5}\n'
            msg += '.' * 50 + '\n' if i < len(titulo) - 1 else '=' * 50 + '\n'
        return msg

    def get_reward(self):
        return self.reward

    def isPayable(self):
        return self.usdt > 0

    def isCollectible(self):
        return self.crypto > 0




