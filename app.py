import streamlit as st
from streamlit_autorefresh import st_autorefresh
from signal_engine import get_price
from datetime import datetime

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pulse Nasdaq")

# Rafraîchissement toutes les 20 secondes
st_autorefresh(interval=20000)

prix = get_price()

st.metric(
    label="Nasdaq Future (NQ=F)",
    value=f"{prix:,.2f}"
)

st.write("Dernière mise à jour :")
st.success(datetime.now().strftime("%H:%M:%S"))
from signal_engine import get_signal
signal = get_signal()

st.subheader("Signal")

st.success(signal)
