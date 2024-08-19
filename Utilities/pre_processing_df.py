# import pandas_ta as pdta
from ta.trend import EMAIndicator
import ta
import numpy as np

async def AddIndicators(df):
    supertrande_candles = 50
    # supertrande_multiplier = 4
    # super_trend = pdta.supertrend(high=df['High'], low=df['Low'], close=df['Close'], length=supertrande_candles, multiplier=supertrande_multiplier)
    # df['SuperTrend'] = super_trend['SUPERTd_50_4.0']
    df['Candle'] = df.apply(lambda row: 'Green' if row['Close'] >= row['Open'] else 'Red', axis=1)
    df['CandleBody'] = abs(df['High'] - df['Low'])
    # ----------------------------------------------------------------------------------------------------------------------------

    df['9EMA'] = EMAIndicator(close=df['Close'], window=5, fillna=False).ema_indicator()
    df['15EMA'] = EMAIndicator(close=df['Close'], window=15, fillna=False).ema_indicator()
    df['50EMA'] = EMAIndicator(close=df['Close'], window=50, fillna=False).ema_indicator()
    df['200EMA'] = EMAIndicator(close=df['Close'], window=200, fillna=False).ema_indicator()
    # ----------------------------------------------------------------------------------------------------------------------------

    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=12).rsi()
    df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume']).volume_weighted_average_price()
    # ----------------------------------------------------------------------------------------------------------------------------

    adx = ta.trend.ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=14, fillna=False)
    df['ADX'] = adx.adx()
    df['D+'] = adx.adx_pos()
    df['D-'] = adx.adx_neg()

    # ----------------------------------------------------------------------------------------------------------------------------

    upper_shadow = df['High'] - df[['Close', 'Open']].max(axis=1)
    lower_shadow = df[['Close', 'Open']].min(axis=1) - df['Low']
    total_range = upper_shadow + lower_shadow
    df['upper_shadow_pr'] = (upper_shadow / total_range) * 100
    df['lower_shadow_pr'] = (lower_shadow / total_range) * 100
    df['Candle_Signal'] = np.select(
        [np.logical_and(df['upper_shadow_pr'] <= 30, df['lower_shadow_pr'] >= 70),
         np.logical_and(df['upper_shadow_pr'] >= 70, df['lower_shadow_pr'] <= 30)],
        ['Bullish', 'Bearish'],
        default='Neutral'
    )

    return df