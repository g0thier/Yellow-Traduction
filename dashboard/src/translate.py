from io import BytesIO
from time import sleep

def translate(uploaded_file):
    """
    Prend un fichier PDF provenant de st.file_uploader
    et renvoie le PDF tel quel (sans modification).

    Retourne :
    - bytes ou BytesIO compatibles avec st.download_button
    """
    sleep(3)  # Simule un temps de traitement (à remplacer par la vraie traduction)

    if uploaded_file is None:
        return None

    # Vérification basique du type MIME
    if uploaded_file.type != "application/pdf":
        return None

    try:
        # Lire le contenu binaire du fichier
        pdf_bytes = uploaded_file.read()

        # Remettre le curseur à zéro (bonne pratique si réutilisé ailleurs)
        uploaded_file.seek(0)

        # Retourner un buffer BytesIO (compatible Streamlit)
        return BytesIO(pdf_bytes)

    except Exception:
        return None
