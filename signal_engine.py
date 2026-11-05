import yfinance as yf

def get_price():

    data = yf.download(
        tickers="NQ=F",
        period="1d",
        interval="5m",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        return 0

    close = data["Close"]

    try:
        return float(close.iloc[-1])
    except:
        return float(close.values[-1])
