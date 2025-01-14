from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from keras.src.layers import LayerNormalization, MultiHeadAttention
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Input, Bidirectional

def ar_model(series, lags):
    """
    Создание и обучение авторегрессионной модели (AR)

    series: временной ряд
    lags: количество лагов (задержек)
    """

    model = ARIMA(series, order=(lags, 0, 0))
    model_fit = model.fit()

    return model_fit

def ma_model(series, lags):
    """
    Создание и обучение модели скользящего среднего (MA)

    series: временной ряд
    lags: количество лагов (задержек)
    """

    model = ARIMA(series, order=(0, 0, lags))
    model_fit = model.fit()

    return model_fit

def arima_model(series, order=(1, 1, 1)):
    """
    Создание и обучение модели ARIMA

    series: временной ряд
    order: параметры модели ARIMA (p, d, q)
    """

    model = ARIMA(series, order=order)
    model_fit = model.fit()

    return model_fit

def sarima_model(series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
    """
    Создание и обучение модели SARIMA
    """
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()
    return model_fit

def holt_winters_model(series, seasonal_periods, trend='add', seasonal='add'):
    """
    Создание и обучение модели Хольта-Винтерса

    series: временной ряд
    seasonal_periods: количество периодов сезонности
    trend: тип тренда (add или mul)
    seasonal: тип сезонности (add или mul)
    """

    model = ExponentialSmoothing(series, trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
    model_fit = model.fit()
    return model_fit

def lstm_model(series, n_steps, n_features=1, epochs=10, batch_size=1):
    """
    Создание и обучение модели LSTM.

    series (np.array): Временной ряд в формате массива numpy.
    n_steps (int): Количество временных шагов для каждого входного образца.
    n_features (int): Количество признаков на временной шаг (обычно 1 для одномерного временного ряда).
    epochs (int): Количество эпох обучения.
    batch_size (int): Размер батча при обучении.

    Возвращает:
        model (Sequential): Обученная модель LSTM.
    """

    X, y = [], []
    for i in range(len(series) - n_steps):
        X.append(series[i:i + n_steps])
        y.append(series[i + n_steps])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    model = Sequential()
    model.add(Input(shape=(n_steps, n_features)))  #
    model.add(LSTM(50, activation='relu', return_sequences=True))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

    return model

def bilstm_model(series, n_steps, n_features, epochs=10, batch_size=1):
    """
     Создание и обучение модели Bi-LSTM.
    series (np.array): Временной ряд в формате массива numpy.
    n_steps (int): Количество временных шагов для каждого входного образца.
    n_features (int): Количество признаков на временном шаге.
    epochs (int): Количество эпох обучения.
    batch_size (int): Размер батча при обучении.
    """

    X, y = [], []
    for i in range(len(series) - n_steps):
        X.append(series[i:i + n_steps])
        y.append(series[i + n_steps])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], n_features))


    model = Sequential()
    model.add(Input(shape=(n_steps, n_features)))
    model.add(Bidirectional(LSTM(50, activation='relu', return_sequences=True)))
    model.add(Bidirectional(LSTM(50, activation='relu')))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')


    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

    return model

def timemixer_model(series, n_steps, n_features, epochs=10, batch_size=1):
    """
    Создание и обучение модели TimeMixer для временных рядов.

    series (np.array): Временной ряд в формате массива numpy.
    n_steps (int): Количество временных шагов для каждого входного образца.
    n_features (int): Количество признаков на временном шаге.
    epochs (int): Количество эпох обучения.
    batch_size (int): Размер пакета при обучении.
    """
    # Подготовка данных
    X, y = [], []
    for i in range(len(series) - n_steps):
        X.append(series[i:i + n_steps])
        y.append(series[i + n_steps])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    # Определение входов модели
    inputs = Input(shape=(n_steps, n_features))
    x = LayerNormalization()(inputs)
    # Обратите внимание, query и value устанавливаются как x, key тоже может быть x, если не указано иначе
    attention_output = MultiHeadAttention(num_heads=2, key_dim=n_features)(x, x)
    x = Dense(64, activation='relu')(attention_output)
    outputs = Dense(1)(x)

    # Создание и компиляция модели
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Обучение модели
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

    return model
