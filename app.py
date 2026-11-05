import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

from signal_engine import (
    get_price,
    get_market_context,
    get_premium_setup
)

# ==========================
# CONFIG APPLICATION
# ==========================

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

# ==========================
# MOT DE PASSE
# ==========================

PASSWORD = "NASDAQ2026!"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("🔒 Pulse Nasdaq")

    password = st.text_input(
        "Mot de passe",
        type="password"
    )

    if st.button("Connexion"):

        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()

        else:
            st.error("Mot de passe incorrect")

    st.stop()

# ==========================
# AUTO REFRESH
# ==========================

st_autorefresh(
    interval=20000,
    key="pulse_refresh"
)

# ==========================
# CHARGEMENT DONNEES
# ==========================

try:

    prix = get_price()
    contexte = get_market_context()
    setup = get_premium_setup()

except Exception as e:

    st.error(f"Erreur : {e}")
    st.stop()

# ==========================
# ENTETE
# ==========================

st.title("📈 Pulse Nasdaq")

st.caption(
    "Version 15 min → validation 5 min • Mise à jour automatique toutes les 20 secondes"
)

# ==========================
# INDICATEURS
# ==========================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "NASDAQ Future",
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
        "🟢 ACTIF"
    )

# ==========================
# CONTEXTE MARCHE
# ==========================

st.markdown("---")

st.subheader("Contexte Marché")

if "HAUSSE" in contexte:
    st.success(contexte)
else:
    st.error(contexte)

# ==========================
# SIGNAL 15 MIN
# ==========================

st.markdown("---")

st.subheader("Signal 15 Minutes")

signal = setup["signal"]

if "ACHAT" in signal:
    st.success(signal)

elif "VENTE" in signal:
    st.error(signal)

else:
    st.warning(signal)

# ==========================
# VALIDATION 5 MIN
# ==========================

st.subheader("Validation 5 Minutes")

validation = setup["confirmation"]

if setup["premium"]:
    st.success(validation)
else:
    st.warning(validation)

# ==========================
# TABLEAU RECAP
# ==========================

st.markdown("---")

st.subheader("Résumé")

resume = {
    "Prix Nasdaq": f"{prix:,.2f}",
    "Contexte": contexte,
    "Signal 15 min": signal,
    "Validation 5 min": validation,
    "Dernière mise à jour": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
}

st.json(resume)

# ==========================
# AIDE
# ==========================

st.markdown("---")

with st.expander("Comment fonctionne Pulse Nasdaq ?"):

    st.markdown("""
### Étape 1
Analyse des bougies 15 minutes.

### Étape 2
Détection :

- ACHAT PRIORITAIRE
- VENTE PRIORITAIRE

### Étape 3
Validation du même sens sur les bougies 5 minutes.

### Résultat

✅ PREMIUM = validation obtenue

⏳ EN ATTENTE = validation absente
""")

# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.caption(
    "Pulse Nasdaq V2 • 15 min → 5 min • Yahoo Finance • Streamlit Cloud"
)
