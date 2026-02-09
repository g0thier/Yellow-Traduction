import streamlit as st

# Sélecteur de paire de langues
options = ["Anglais-Français"]
selection = st.radio(
    "Modèle de traduction",
    options,
    index=0,  # ✅ jamais None
    help="Sélectionnez la paire de langues pour la traduction",
)