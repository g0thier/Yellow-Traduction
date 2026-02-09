import streamlit as st

st.set_page_config(page_title="Yellow Traduction", layout="centered")

st.title("Yellow Traduction")
st.write("Ceci est un projet Streamlit minimal.")

nom = st.text_input("Ton nom")

if nom:
    st.success(f"Bienvenue {nom} !")
