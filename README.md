# Scanner de Factures – OCR Google Vision

Ce projet permet de scanner des factures PDF, d’en extraire automatiquement :  
- Le numéro de facture  
- Le montant TTC  

Puis d’exporter ces données dans un fichier Excel (.xlsx).  
L’OCR (reconnaissance de texte) est réalisé grâce à l’API Google Cloud Vision.

## Fonctionnalités

- Sélection d’un fichier PDF via une interface graphique simple (Tkinter)  
- Conversion du PDF en images haute qualité avec Poppler  
- Lecture du texte par Google Cloud Vision API  
- Extraction du numéro de facture et du montant TTC  
- Sauvegarde automatique dans un fichier Excel avec `openpyxl`  
- Interface graphique pour lancer le traitement facilement

## Installation

### Pré-requis
- Python 3.9 ou supérieur  
- Compte Google Cloud avec l’API Vision activée  
- Fichier de clé JSON de service Google (ex : `vision.json`)  

### Dépendances Python
Installez les librairies nécessaires :

```bash
pip install google-cloud-vision pdf2image pillow openpyxl


Dans le script Python, configurez les chemins :
poppler_path = r"C:\poppler\Library\bin"
cle_google = r"C:\Users\comptabilite\Documents\vision.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cle_google
