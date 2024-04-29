import numpy as np

def get_heikin_kandle(df):
    df_copy = df.copy()
    for i in range(df_copy.shape[0]):
        if i > 0:
            df_copy.loc[df_copy.index[i], 'Open'] = (df['Open'][i - 1] + df['Close'][i - 1]) / 2
        df_copy.loc[df_copy.index[i], 'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] + df['High'][i]) / 4

    return df_copy.iloc[1:, :]

def heiken_ashi_pivot_breakout_trailing_stop(df):
    greenHA = df['Close'] > df['Open']
    redHA = df['Close'] < df['Open']
    redToGreenHA = []
    greenToRedHA = []
    topSwing = []
    bottomSwing = []
    TS = []
    for i in range(len(greenHA)):
        rtg = redHA[i-1] and greenHA[i]
        gtr = greenHA[i-1] and redHA[i]
        redToGreenHA.append(rtg)
        greenToRedHA.append(gtr)
        topSwing.append(0 if not topSwing else (max(df['High'][i],df['High'][i-1],df['High'][i-2]) if gtr else topSwing[i-1]))
        bottomSwing.append(0 if not bottomSwing else (min(df['High'][i],df['High'][i-1],df['High'][i-2]) if rtg else bottomSwing[i-1]))
        TS.append(0 if not TS else(topSwing[i-1] if df['Close'][i] < TS[i-1] else (bottomSwing[i-1] if df['Close'][i] > TS[i-1] else TS[i-1])))
    df['TS'] = TS
    df.drop(df.index[0:3], inplace=True)

