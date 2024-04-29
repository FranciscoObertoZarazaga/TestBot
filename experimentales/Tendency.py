from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from statistics import mean
import numpy as np

def classify(df):
    kp = df.iloc[:-1]['Close']
    kf = df.iloc[1:]['Close'].reset_index(drop=True)
    df.drop(len(df) - 1, inplace=True)
    df['future'] = np.where(kp < kf, True, False)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)


def preprocess(array, grado):
    pf = PolynomialFeatures(degree=grado)
    return pf.fit_transform(np.array(array).reshape(-1, 1))


def fit(x, y, grado):
    model = LinearRegression()
    x = preprocess(x, grado)
    model.fit(X=x, y=y)
    return model


def predict(x, model, grado):
    x = preprocess(x, grado)
    return model.predict(x)


def get_model(df, i, period=10, grado=1):
    y_low = df['Low'][i-period+1:i+1]
    y_high = df['High'][i-period+1:i+1]
    y_open = df['Open'][i-period+1:i+1]
    y_close = df['Close'][i-period+1:i+1]
    y_volume = df['Volume'][i-period+1:i+1]
    x = range(period)

    model_low = fit(x, y_low, grado)
    model_high = fit(x, y_high, grado)
    model_open = fit(x, y_open, grado)
    model_close = fit(x, y_close, grado)
    model_volume = fit(x, y_volume, grado)

    models = {'model_open': model_open,
              'model_high': model_high,
              'model_low': model_low,
              'model_close': model_close,
              'model_volume': model_volume}

    predict_low = predict([period], model_low, grado)[0]
    predict_high = predict([period], model_high, grado)[0]
    predict_open = predict([period], model_open, grado)[0]
    predict_close = predict([period], model_close, grado)[0]
    predict_volume = predict([period], model_volume, grado)[0]

    predictions = {'predict_open': predict_open,
                   'predict_high': predict_high,
                   'predict_low': predict_low,
                   'predict_close': predict_close,
                   'predict_volume': predict_volume}

    return models, predictions


def get_coefs(models):
    coef_low = models['model_low'].coef_[0]
    coef_high = models['model_high'].coef_[0]
    coef_open = models['model_open'].coef_[0]
    coef_close = models['model_close'].coef_[0]
    coef_volume = models['model_volume'].coef_[0]

    coefs = {'coef_open': coef_open,
             'coef_high': coef_high,
             'coef_low': coef_low,
             'coef_close': coef_close,
             'coef_volume': coef_volume}

    media = mean(coefs.values())

    return coefs, media


def test(df, periodo=10, grado=1):
    #categoria = {'predict_open': 'Open', 'predict_high': 'High', 'predict_low': 'Low', 'predict_close': 'Close'}
    categoria = {'predict_high': 'High', 'predict_low': 'Low'}
    #categoria = {'predict_close': 'Close'}
    df = df.copy().reset_index(drop=True)
    classify(df)
    y_predict = list()
    for i in range(len(df)):
        if i < periodo:
            continue
        prediction = []
        for j in range(1,grado+1):
            models, predictions = get_model(df, i, period=periodo, grado=grado)
            for clave, valor in categoria.items():
                predict = True if predictions[clave] > df[valor][i] else False
                prediction.append(predict)
        sube = sum(prediction)
        baja = len(prediction) - sube
        prediction = True if sube > baja else False
        y_predict.append(prediction)
    y_true = df['future'][periodo:]

    tn, fp, fn, tp = confusion_matrix(y_true=y_true, y_pred=y_predict).ravel()
    tasa_positiva = tp / (tp+fp)
    tasa_negativa = tn / (tn+fn)
    tasa = (tp+tn) / (tp+tn+fp+fn)

    print(f'TN: {tn}')
    print(f'TP: {tp}')
    print(f'FN: {fn}')
    print(f'FP: {fp}')
    print(f'Tasa positiva: {tasa_positiva:.2%}')
    print(f'Tasa negativa: {tasa_negativa:.2%}')
    print(f'Tasa: {tasa:.2%}')

    return y_predict


