import streamlit as st
import yfinance as yf

st.title("Test Nasdaq")

data = yf.download(
    "NQ=F",
    period="1d",
    interval="5m",
    progress=False
)

st.write(data.tail())
