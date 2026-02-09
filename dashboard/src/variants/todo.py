import streamlit as st

# Sélecteur de paire de langues
options = ["Anglais-Français"]
selection = st.radio(
    "Modèle de traduction",
    options,
    index=0,  # ✅ jamais None
    help="Sélectionnez la paire de langues pour la traduction",
)

import os
import platform
import psutil

# Affichage des infos système
caption = (
    f"OS : {platform.system()} {platform.release()} "
    f"• Arch : {platform.machine()} "
    f"• CPU : {platform.processor() or 'N/A'} "
    f"• Cœurs : {os.cpu_count()} "
    f"• Swap : {round(psutil.swap_memory().total / (1024**3), 2)} GB "
    f"• RAM : {round(psutil.virtual_memory().total / (1024**3), 2)} GB "
    f"• Python : {platform.python_version()}"
)

st.caption(caption)