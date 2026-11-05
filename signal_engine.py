import yfinance as yf
import pandas as pd
import numpy as np


# ==========================
# Téléchargement
# ==========================

def get_data():

    data = yf.download(
        "NQ=F",
        period="30d",
        interval="5m",
        progress=False,
        auto_adjust=True
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


# ==========================
# Agrégation 15 minutes
# ==========================

def build_15m(df):

    d15 = df.resample("15min").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    d15 = d15.dropna()

    return d15


# ==========================
# Prix
# ==========================

def get_price():

    df = get_data()

    return float(df["Close"].iloc[-1])


# ==========================
# Signal 15 min
# ==========================

def get_15m_signal():

    df5 = get_data()
    df15 = build_15m(df5)

    close = df15["Close"]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    momentum = close.pct_change(3)

    dernier = len(close) - 1

    achat = (
        ema20.iloc[dernier] > ema50.iloc[dernier]
        and momentum.iloc[dernier] > 0
    )

    vente = (
        ema20.iloc[dernier] < ema50.iloc[dernier]
        and momentum.iloc[dernier] < 0
    )

    if achat:
        return 1, "🟢 ACHAT PRIORITAIRE"

    if vente:
        return -1, "🔴 VENTE PRIORITAIRE"

    return 0, "⚪ AUCUN SIGNAL"


# ==========================
# Validation 5 min
# ==========================

def get_premium_setup():

    df5 = get_data()

    sens, signal = get_15m_signal()

    if sens == 0:
        return {
            "signal": signal,
            "premium": False,
            "confirmation": "Aucune"
        }

    close = df5["Close"]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    derniere = len(close) - 1

    achat_valide = (
        sens == 1
        and ema20.iloc[derniere] > ema50.iloc[derniere]
    )

    vente_valide = (
        sens == -1
        and ema20.iloc[derniere] < ema50.iloc[derniere]
    )

    premium = achat_valide or vente_valide

    return {
        "signal": signal,
        "premium": premium,
        "confirmation": "✅ PREMIUM" if premium else "⏳ EN ATTENTE"
    }


# ==========================
# Contexte
# ==========================

def get_market_context():

    df = get_data()

    close = df["Close"]

    ema50 = close.ewm(span=50).mean()
    ema200 = close.ewm(span=200).mean()

    if ema50.iloc[-1] > ema200.iloc[-1]:
        return "🟢 HAUSSE"

    return "🔴 BAISSE"
