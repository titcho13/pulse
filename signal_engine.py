import yfinance as yf

def get_price():

    data = yf.download(
        "NQ=F",
        period="1d",
        interval="5m",
        progress=False
    )

    if data.empty:
        return 0

    return float(data["Close"].iloc[-1, 0])
