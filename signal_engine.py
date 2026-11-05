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
