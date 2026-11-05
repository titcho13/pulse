import streamlit as st
from streamlit_autorefresh import st_autorefresh

from signal_engine import get_price

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pulse Nasdaq")

st_autorefresh(interval=20000)

prix = get_price()

st.metric(
    "Nasdaq Future",
    round(prix, 2)
)
