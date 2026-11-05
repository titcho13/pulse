import yfinance as yf
import pandas as pd


# ==========================
# TELECHARGEMENT DONNEES
# ==========================

def get_data():

    data = yf.download(
        "NQ=F",
        period="30d",
        interval="5m",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        return pd.DataFrame()

    # Corrige les MultiIndex Yahoo Finance
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


# ==========================
# PRIX ACTUEL
# ==========================

def get_price():

    df = get_data()

    if df.empty:
        return 0

    return float(df["Close"].iloc[-1])


# ==========================
# CONTEXTE DE MARCHE
# ==========================

def get_market_context():

    df = get_data()

    if df.empty:
        return "Données indisponibles"

    close = df["Close"]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    if ema20.iloc[-1] > ema50.iloc[-1]:
        return "🟢 HAUSSE"

    return "🔴 BAISSE"


# ==========================
# SIGNAL SIMPLE
# ==========================

def get_signal():

    df = get_data()

    if df.empty:
        return "AUCUN SIGNAL"

    close = df["Close"]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    if ema20.iloc[-1] > ema50.iloc[-1]:
        return "🟢 ACHAT"

    return "🔴 VENTE"


# ==========================
# FORCE DU SIGNAL
# ==========================

def get_probability():

    df = get_data()

    if df.empty:
        return 0

    close = df["Close"]

    ema20 = close.ewm(span=20).mean()
    ema50 = close.ewm(span=50).mean()

    ecart = abs(
        (ema20.iloc[-1] - ema50.iloc[-1])
        / ema50.iloc[-1]
    ) * 100

    score = min(round(ecart * 100), 95)

    return max(score, 50)


# ==========================
# HEURE DERNIERE BOUGIE
# ==========================

def get_last_bar_time():

    df = get_data()

    if df.empty:
        return "N/A"

    return str(df.index[-1])


# ==========================
# DASHBOARD
# ==========================

def get_dashboard_data():

    return {
        "prix": get_price(),
        "contexte": get_market_context(),
        "signal": get_signal(),
        "probabilite": get_probability(),
        "derniere_bougie": get_last_bar_time()
    }

