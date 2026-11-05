import yfinance as yf
import pandas as pd
import numpy as np

def get_data():

    data = yf.download(
        "NQ=F",
        period="30d",
        interval="5m",
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data
    def get_price():

    df = get_data()

    return float(df["Close"].iloc[-1])
    def get_market_context():

    df = get_data()

    close = df["Close"]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    if ema20.iloc[-1] > ema50.iloc[-1]:
        return "🟢 HAUSSE"

    return "🔴 BAISSE"
