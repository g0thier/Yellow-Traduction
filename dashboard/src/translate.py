from io import BytesIO
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import torch
from transformers import MarianTokenizer, MarianMTModel
import fitz  # PyMuPDF

# CONSTANTES

# Choix auto du device
if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

# Modèle de traduction anglais -> français
MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"
MAX_NEW_TOKENS = 512                           # limite sortie par ligne
BATCH_SIZE = 8                                # taille lot traduction

# Initialisation du modèle et du tokenizer
tokenizer  = MarianTokenizer.from_pretrained(MODEL_NAME)
model  = MarianMTModel.from_pretrained(MODEL_NAME).to(DEVICE).eval()

# Détecter nb de cœurs dispo et en garder 1 pour le système
MAX_WORKERS = max(1, os.cpu_count() - 1)
print(f"⚡ Utilisation de {MAX_WORKERS} threads pour la traduction (sur {os.cpu_count()} cœurs disponibles)")

# FONCTIONS

# Extraction du texte d'un PDF en blocs (coordonnées + texte)
def extract_text_blocks(doc):
    # Extraction des blocs de texte
    pages_text = []
    for page in doc:
        blocks = page.get_text("blocks")  # [(x0,y0,x1,y1,"texte",bloc_num,...)]
        page_blocks = []
        for b in blocks:
            text = b[4].strip()
            if len(text) >= 4:  # on ignore les bouts trop courts
                page_blocks.append((b[:4], text))  # coordonnées + texte
        pages_text.append(page_blocks)
    return pages_text

def translate_batch(batch):
    """Traduit un batch de textes (utilise le modèle global, partagé en RAM)."""
    inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True).to(DEVICE)
    translated = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
    return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

def translate_blocks(blocks):
    # ---- 1. Aplatir toutes les pages ----
    flat_texts = []
    for page_idx, page_blocks in enumerate(blocks, start=0):  # start=0 pour index direct
        for coords, text in page_blocks:
            flat_texts.append((page_idx, coords, text))

    print(f"➡️ Total de {len(flat_texts)} blocs de texte à traduire (toutes pages confondues)")

    # ---- 2. Créer des batches globaux ----
    batches = [(i, [t[2] for t in flat_texts[i:i+BATCH_SIZE]]) for i in range(0, len(flat_texts), BATCH_SIZE)]

    # ---- 3. Traduction en parallèle ----
    all_translations = [None] * len(flat_texts)

    n_batch = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_idx = {executor.submit(translate_batch, batch): idx for idx, batch in batches}
        
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            batch_translations = future.result()
            all_translations[idx:idx+len(batch_translations)] = batch_translations
            n_batch += 1
            print(f"  - Batch {n_batch}/{len(batches)} terminé ({round(n_batch/len(batches)*100, 2)}%)")

    # ---- 4. Reconstruction des pages ----
    translated_pages = [[] for _ in range(len(blocks))]

    for (page_idx, coords, _), trans in zip(flat_texts, all_translations):
        translated_pages[page_idx].append((coords, trans))

    print(f"\n✅ Traduction terminée : {len(translated_pages)} pages traitées")
    print("\nExemple traduction première page :", translated_pages[0][:3])
    return translated_pages

# Tailles de police à tester pour la mise en page 
# (de 100 à 4, avec plus de granularité vers les petites tailles)
sizes = (
    list(range(100, 49, -10)) +
    list(range(50, 19, -5)) +
    list(range(20, 13, -1)) +
    [round(x, 1) for x in [14 - i*0.1 for i in range(int((14-4)/0.1)+1)]]
)

# Trouve la plus grande taille de police qui rentre dans rect (binary search).
def best_font_size(page, rect, text, sizes):
    lo, hi = 0, len(sizes) - 1
    best = sizes[-1]

    while lo <= hi:
        mid = (lo + hi) // 2
        font_size = sizes[mid]
        rc = page.insert_textbox(
            rect,
            text,
            fontsize=font_size,
            color=(0, 0, 0),
            align=3,
            render_mode=3  # mesure uniquement
        )
        if rc >= 0:  # le texte tient
            best = font_size
            hi = mid - 1
        else:  # trop grand → réduire
            lo = mid + 1
    return best

def create_translated_pdf(doc, translated_pages, output_path):
    # ---- Application séquentielle ----
    for page_index, page in enumerate(doc):
        print(f"📄 Traitement page {page_index+1}/{len(doc)}")
        blocks = translated_pages[page_index]

        for coords, text in blocks:
            rect = fitz.Rect(coords)
            font_size = best_font_size(page, rect, text, sizes)
            print(f"  - Bloc {coords} : font size optimale = {font_size}")

            # dessiner rectangle jaune
            page.draw_rect(rect, color=(1, 1, 0),
                        fill=(1, 1, 0),
                        fill_opacity=0.9,
                        overlay=True)

            # insérer texte à la bonne taille
            page.insert_textbox(
                rect,
                text,
                fontsize=font_size,
                color=(0, 0, 0),
                align=3
            )

    print(f"\n✅ Mise en page terminée, sauvegarde du PDF traduit...")
    doc.save(output_path)


def translate(uploaded_file)->BytesIO|None:
    """
    Prend un fichier PDF provenant de st.file_uploader
    et renvoie le PDF avec les textes traduits.

    Retourne :
    - BytesIO contenant le PDF traduit, compatible avec st.download_button
    """
    if uploaded_file is None:
        return None

    # Vérification basique du type MIME
    if uploaded_file.type != "application/pdf":
        return None

    try:
        # Lire le contenu binaire du fichier
        pdf_bytes = uploaded_file.read()

        # Remettre le curseur à zéro
        uploaded_file.seek(0)

        # ---- Pipeline complet de traduction ----
        
        # 1. Ouvrir le PDF depuis les bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # 2. Extraire les blocs de texte
        pages_text = extract_text_blocks(doc)

        # 3. Traduire les blocs
        translations = translate_blocks(pages_text)

        # 4. Créer le PDF traduit en mémoire
        for page_index, page in enumerate(doc):
            blocks = translations[page_index]

            for coords, text in blocks:
                rect = fitz.Rect(coords)
                font_size = best_font_size(page, rect, text, sizes)

                # dessiner rectangle jaune
                page.draw_rect(rect, color=(1, 1, 0),
                            fill=(1, 1, 0),
                            fill_opacity=0.9,
                            overlay=True)

                # insérer texte à la bonne taille
                page.insert_textbox(
                    rect,
                    text,
                    fontsize=font_size,
                    color=(0, 0, 0),
                    align=3
                )

        # 5. Écrire le résultat dans un BytesIO
        output_bytes = BytesIO()
        doc.save(output_bytes, garbage=3, deflate=True)  # options facultatives mais utiles
        output_bytes.seek(0)
        
        return output_bytes

    except Exception:
        return None