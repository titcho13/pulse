import streamlit as st
from streamlit_autorefresh import st_autorefresh
from signal_engine import get_price, get_market_context, get_signal
from datetime import datetime

# =====================
# CONFIGURATION
# =====================

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

# =====================
# MOT DE PASSE
# =====================

PASSWORD = "NASDAQ2026!"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("🔒 Pulse Nasdaq")

    pwd = st.text_input(
        "Mot de passe",
        type="password"
    )

    if st.button("Connexion"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect")

    st.stop()

# =====================
# RAFRAICHISSEMENT
# =====================

st_autorefresh(
    interval=20000,
    key="refresh"
)

# =====================
# RECUPERATION DONNEES
# =====================

prix = get_price()
contexte = get_market_context()
signal = get_signal()

# =====================
# TITRE
# =====================

st.title("📈 Pulse Nasdaq")

st.caption("Mise à jour automatique toutes les 20 secondes")

# =====================
# PRIX
# =====================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Nasdaq Future (NQ=F)",
        f"{prix:,.2f}"
    )

with col2:
    st.metric(
        "Heure",
        datetime.now().strftime("%H:%M:%S")
    )

with col3:
    st.metric(
        "Statut",
        "🟢 Actif"
    )

# =====================
# CONTEXTE
# =====================

st.subheader("Contexte Marché")

if "HAUSSE" in contexte:
    st.success(contexte)
else:
    st.error(contexte)

# =====================
# SIGNAL
# =====================

st.subheader("Signal Actuel")

if "ACHAT" in signal:
    st.success(signal)
else:
    st.error(signal)

# =====================
# INFORMATIONS
# =====================

st.markdown("---")

st.subheader("Informations")

st.write(f"Prix actuel : {prix:,.2f}")

st.write(f"Contexte : {contexte}")

st.write(f"Signal : {signal}")

st.write(
    f"Dernière mise à jour : "
    f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)

# =====================
# PIED DE PAGE
# =====================

st.markdown("---")

st.caption(
    "Pulse Nasdaq V1 • GitHub + Streamlit Cloud • Yahoo Finance"
)
