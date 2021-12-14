def get_heikin_kandle(df):
    df_copy = df.copy()
    for i in range(df_copy.shape[0]):
        if i > 0:
            df_copy.loc[df_copy.index[i], 'Open'] = (df['Open'][i - 1] + df['Close'][i - 1]) / 2
        df_copy.loc[df_copy.index[i], 'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] + df['High'][i]) / 4

    return df_copy.iloc[1:, :]