from PIL import Image, ImageFilter
import sys
import os

# Vérification des arguments
if len(sys.argv) != 3:
    print("Utilisation : python f_gaussien.py le_chemin.jpg radius(ex: 1)")
    sys.exit(1)

image_path = sys.argv[1]
rad = int(sys.argv[2])

# Ouverture de l'image
image = Image.open(image_path)

# Appliquer le filtre Laplacien pour accentuer les contours
filtered_image = image.filter(ImageFilter.GaussianBlur(radius=rad))

# Nom du fichier d'entrée sans l'extension
nom_fichier_base, extension = os.path.splitext(os.path.basename(image_path))

# Création du nouveau nom de fichier pour l'image de sortie
nom_image_sortie = "../imgoutdenoised/" + nom_fichier_base + f"_gaussien_{rad}.jpg"

# Enregistrement de l'image modifiée
filtered_image.save(nom_image_sortie)
