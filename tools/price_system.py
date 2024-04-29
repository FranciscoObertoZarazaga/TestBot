import random


def Close(df, i):
    return df['Close'][i]


def Open(df, i):
    return df['Open'][i]


def High(df, i):
    return df['High'][i]


def Low(df, i):
    return df['Low'][i]


def Random(df, i):
    return random.uniform(df['Low'][i], df['High'][i])


def Mean(df, i):
    return (df['Low'][i]+df['High'][i]) / 2


def Best(df, i, points):
    return df['Low'][i] if points == 1 else df['High'][i]


def Worst(df, i, points):
    return df['High'][i] if points == 1 else df['Low'][i]


PRICE = {
    'CLOSE': Close,
    'OPEN': Open,
    'HIGH': High,
    'LOW': Low,
    'RANDOM': Random,
    'MEAN': Mean,
    'BEST': Best,
    'WORST': Worst
}
