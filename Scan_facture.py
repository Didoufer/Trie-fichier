import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from google.cloud import vision
import os
import unicodedata

# Config Google Vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\comptabilite\Documents\vision.json"

# Liste des fournisseurs
FOURNISSEURS = [
    "Marseille Dépôt", "CEVAM", "Delphi", "Eurorepar", "Purflux", "Valeo", "Bosch", "Sasic", "NPS",
    "Chaussende", "Da Silva", "Edenred", "NPS", "JBM", "amazon", "So tech", "wiltec", "akkunet",
    "LKQ", "Fedex", "Sodise", "chatreix", "IVIBlUE", "Gerilec", "culture pneus", "CDAL", "acrom",
    "LAD", "ICS", "ROAZHON", "Boudon","akwel","ferron","Dantherm","solaufil", "CLAS","B PARTS","Orange",
    "Norauto","ELECTRO DEPOT","EDF","dauphin","odycé meditec","prokap","Top fishing","Crédit agricole",
    "Volvo","Bureau vallé","Accusplus","surplus autos","Micromania","rst","ICS","lexcom","renault",
    "aurelia car","DEG","ebay","ecotec","ID","Suez","total energie","PAP SUD","Defi","Corteco","AutoControl",
    "Intrum","boulanger","King Tony","boulanger","parts and go"
    
]

def normalize(txt):
    txt = unicodedata.normalize("NFD", txt)
    return ''.join(c for c in txt if unicodedata.category(c) != "Mn").upper()

FOURN_NORMAL = [normalize(f) for f in FOURNISSEURS]
client = vision.ImageAnnotatorClient()

def detecter_nom_entreprise(img_bytes):
    image = vision.Image(content=img_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return "Inconnue"

    texte = texts[0].description
    lignes = normalize(texte).splitlines()

    for l in lignes[:10]:
        for idx, f in enumerate(FOURN_NORMAL):
            if f in l:
                return FOURNISSEURS[idx]

    for l in lignes:
        if l.isupper() and 5 < len(l) < 40:
            return l.title()

    return "Inconnue"

def get_nom_unique(dossier, nom_base):
    nom_base = nom_base.strip().replace(" ", "_")
    base, ext = os.path.splitext(nom_base)
    ext = ext if ext else ".pdf"
    chemin = os.path.join(dossier, f"{base}.pdf")
    compteur = 1
    while os.path.exists(chemin):
        chemin = os.path.join(dossier, f"{base}_{compteur}.pdf")
        compteur += 1
    return chemin

def trier_pdf_par_blocs(pdf_path, dossier_sortie):
    doc = fitz.open(pdf_path)
    pages_groupées = []
    groupe_courant = {"nom": None, "pages": []}

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")

        nom_detecté = detecter_nom_entreprise(img_bytes)

        if nom_detecté == groupe_courant["nom"]:
            groupe_courant["pages"].append(i)
        else:
            if groupe_courant["pages"]:
                pages_groupées.append(groupe_courant)
            groupe_courant = {"nom": nom_detecté, "pages": [i]}

    if groupe_courant["pages"]:
        pages_groupées.append(groupe_courant)

    # Sauvegarde des groupes
    for groupe in pages_groupées:
        pdf_new = fitz.open()
        for num in groupe["pages"]:
            pdf_new.insert_pdf(doc, from_page=num, to_page=num)
        nom_fichier_base = f"{groupe['nom']}.pdf"
        chemin = get_nom_unique(dossier_sortie, nom_fichier_base)
        pdf_new.save(chemin)

    doc.close()

# Interface utilisateur
def lancer_traitement():
    pdf_path = filedialog.askopenfilename(title="Choisir le fichier PDF", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return

    dossier_sortie = filedialog.askdirectory(title="Choisir le dossier de destination")
    if not dossier_sortie:
        return

    try:
        trier_pdf_par_blocs(pdf_path, dossier_sortie)
        messagebox.showinfo("Succès", "Factures triées et regroupées avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# GUI
root = tk.Tk()
root.title("Tri de Factures - Multi-pages")
root.geometry("400x200")

label = tk.Label(root, text="Clique sur le bouton pour traiter ton PDF :", pady=20)
label.pack()

btn = tk.Button(root, text="Sélectionner et Traiter le PDF", command=lancer_traitement, bg="#4CAF50", fg="white", font=("Arial", 12))
btn.pack(pady=10)

root.mainloop()
