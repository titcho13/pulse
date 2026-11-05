import yfinance as yf

def get_price():
    data = yf.download("NQ=F", period="1d", interval="5m")
    return float(data["Close"].iloc[-1])
