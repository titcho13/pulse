import yfinance as yf
import pandas as pd

def get_data():

    data = yf.download(
        "NQ=F",
        period="5d",
        interval="5m",
        progress=False
    )

    return data


def get_price():

    data = get_data()

    return float(data["Close"].iloc[-1, 0])


def get_signal():

    data = get_data()

    close = data["Close"].iloc[:, 0]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    if ema20.iloc[-1] > ema50.iloc[-1]:
        return "🟢 ACHAT"

    return "🔴 VENTE"
