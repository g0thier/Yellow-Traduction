import streamlit as st
from src.translate import translate

st.set_page_config(page_title="Yellow Traduction", layout="centered")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("src/styles.css")

st.title("Yellow Traduction")

# File uploader limité à 200 Mo et fichiers PDF uniquement
uploaded_file = st.file_uploader(
    "Chargez le document en anglais à traduire en français.",
    type="pdf",
    accept_multiple_files=False,
    help="Fichier PDF limité à 200 Mo",
)

# Initialisation du state
if "translated_pdf" not in st.session_state:
    st.session_state.translated_pdf = None
if "last_file_name" not in st.session_state:
    st.session_state.last_file_name = None

if uploaded_file is not None:
    # pour éviter les rechargements de page de strealit à chaque interaction, on vérifie si le fichier a changé
    if uploaded_file.name != st.session_state.last_file_name:
        with st.spinner("Traduction en cours..."):
            st.session_state.translated_pdf = translate(uploaded_file)
            st.session_state.last_file_name = uploaded_file.name

    # Affichage du résultat
    if st.session_state.translated_pdf is not None:
        st.success("Traduction terminée!")

        st.download_button(
            label="Télécharger le PDF traduit",
            data=st.session_state.translated_pdf,
            file_name=f"traduit_{uploaded_file.name}",
            mime="application/pdf",
        )
    else:
        st.error("Erreur lors de la traduction du fichier.")
