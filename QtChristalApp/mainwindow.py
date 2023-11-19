# This Python file uses the following encoding: utf-8
import sys
import os
import cv2

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QObject, Slot, Qt, QSize
#from PyQt6.QtCore import QObject, pyqtSlot, Qt, QSize
from PIL import Image
from imageSettings import *
from imageGenNoises import *
from imageFiltresTrad import *

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #--------------
        #INITIALISATION
        #--------------

        #Variables Booléennes
        self.ImageInIsSet = False
        self.ImageNdg = False
        self.ImageModified = False

        #Variables quantitatives
        self.noise_ecart_type = 20
        self.noise_noise_densite = 0.01

        self.choix_filtre = 1
        self.filter_ecart_type = 20
        self.filter_radius = 1
        self.filter_taille = 3
        self.filter_diameter = 9
        self.filter_var_couleur = 75
        self.filter_var_spatiale = 75

        self.largeur_frame = self.ui.frame_ImgIn.width()
        self.hauteur_frame = self.ui.frame_ImgIn.height()

        #Sliders
        # -- ecart_type
        self.ui.slider_ecart_type.setMinimum(0)
        self.ui.slider_ecart_type.setMaximum(100)
        self.ui.slider_ecart_type.setValue(self.filter_ecart_type)
        self.ui.slider_ecart_type.valueChanged.connect(self.update_ecart_type)
        self.ui.label_ecart_type.setText(f"Écart-type : {self.ui.slider_ecart_type.value()}")
        # -- radius
        self.ui.slider_radius.setMinimum(0)
        self.ui.slider_radius.setMaximum(100)
        self.ui.slider_radius.setValue(self.filter_radius)
        self.ui.slider_radius.valueChanged.connect(self.update_radius)
        self.ui.label_radius.setText(f"Taille noyau : {self.ui.slider_radius.value()}")
        # -- taille
        self.ui.slider_taille.setMinimum(0)
        self.ui.slider_taille.setMaximum(100)
        self.ui.slider_taille.setValue(self.filter_taille)
        self.ui.slider_taille.valueChanged.connect(self.update_taille)
        self.ui.label_taille.setText(f"Taille voisinage : { self.ui.slider_taille.value()}")
        # -- diametre
        self.ui.slider_diametre.setMinimum(5)
        self.ui.slider_diametre.setMaximum(15)
        self.ui.slider_diametre.setSingleStep(2)
        self.ui.slider_diametre.setValue(self.filter_diameter)
        self.ui.slider_diametre.valueChanged.connect(self.update_diametre)
        self.ui.label_diametre.setText(f"Diamètre voisinage : {self.ui.slider_diametre.value()}")
        # -- var_couleur
        self.ui.slider_var_couleur.setMinimum(10)
        self.ui.slider_var_couleur.setMaximum(100)
        self.ui.slider_var_couleur.setValue(self.filter_var_couleur)
        self.ui.slider_var_couleur.valueChanged.connect(self.update_var_couleur)
        self.ui.label_var_couleur.setText(f"Variance couleur : {self.ui.slider_var_couleur.value()}")
        # -- var_spatiale
        self.ui.slider_var_spatiale.setMinimum(10)
        self.ui.slider_var_spatiale.setMaximum(100)
        self.ui.slider_var_spatiale.setValue(self.filter_var_spatiale)
        self.ui.slider_var_spatiale.valueChanged.connect(self.update_var_spatiale)
        self.ui.label_var_spatiale.setText(f"Variance spatiale : {self.ui.slider_var_spatiale.value()}")


        #Lien entre les boutons UI et les fonctions
        self.ui.bouton_ouvrirImgIn.clicked.connect(self.ouvrirImage)

        #Ne pas autoriser le changement d'état des boutons
        #self.ui.bouton_poivresel.setVisible(False)
        #self.ui.bouton_gaussien.setVisible(False)
        #self.ui.bouton_chromatique.setVisible(False)
        self.ui.bouton_poivresel.setEnabled(False)
        self.ui.bouton_gaussien.setEnabled(False)
        self.ui.bouton_chromatique.setEnabled(False)
        #self.ui.bouton_afficher.clicked.connect(lambda : self.affichageImageOut())

    def affichageImageOut(self):
        print("affichage...")
        chemin_dossier_temp = tempfile.gettempdir() + "\ImgChristalTmp.jpg"
        print(chemin_dossier_temp)
        ImgOut = QImage(chemin_dossier_temp)
        #Affichage de l'image dans un label, réglage des dimensions
        largeur_ImgOut = ImgOut.width()
        hauteur_ImgOut = ImgOut.height()
        if largeur_ImgOut > hauteur_ImgOut :
            ImgOut = ImgOut.scaledToWidth(self.largeur_frame, Qt.SmoothTransformation)
        else:
            ImgOut = ImgOut.scaledToHeight(self.hauteur_frame, Qt.SmoothTransformation)
        self.ui.label_ImgOut.setPixmap(QPixmap.fromImage(ImgOut))

    def set_choix_filtre(self, choix):
        self.choix_filtre = choix

    def set_choix_filtre_var(self, choix):
        self.ui.vLay_radius.setEnabled(False)
        self.ui.vLay_diametre.setEnabled(False)
        self.ui.vLay_var_couleur.setEnabled(False)
        self.ui.vLay_var_spatiale.setEnabled(False)
        self.ui.vLay_taille.setEnabled(False)
        self.ui.vLay_ecart_type
        if choix == 1:
            self.ui.vLay_radius.setEnabled(True)
        elif choix == 2:

        elif choix == 3:

        elif choix == 4:

        elif choix == 5:


    def valider_filtres(self, image, choix):
        if choix == 1:
            filtre_gaussien(image, self.filter_radius, self)
        elif choix == 2:
            filtre_bilateral(image.filename, self.filter_diameter, self.filter_var_couleur, self.filter_var_spatiale, self)
        elif choix == 3:
            filtre_moyenneur(image, self.filter_radius, self)
        elif choix == 4:
            filtre_median(image, self.filter_taille, self)
        elif choix == 5:
            filtre_laplacien(image, self)

#def slider_value_changed(self, value):
# Mettre à jour le texte du QLabel avec la valeur actuelle du slider
#    self.sender().parent().findChild(QLabel).setText(f"Valeur actuelle : {value}")

    def update_ecart_type(self, value): # PAS FILTRE MAIS GEN NOISE
        self.filter_ecart_type = value
        self.ui.label_ecart_type.setText(f"Écart-type : {value}")

    def update_radius(self, value):
        self.filter_radius = value
        self.ui.label_radius.setText(f"Taille noyau : {value}")

    def update_taille(self, value):
        self.filter_taille = value
        self.ui.label_taille.setText(f"Taille voisinage : {value}")

    def update_diametre(self, value):
        self.filter_diametre = value
        self.ui.label_diametre.setText(f"Diamètre voisinage : {value}")

    def update_var_couleur(self, value):
        self.filter_var_couleur = value
        self.ui.label_var_couleur.setText(f"Variance couleur : {value}")

    def update_var_spatiale(self, value):
        self.filter_var_spatiale = value
        self.ui.label_var_spatiale.setText(f"Variance spatiale : {value}")

    def ouvrirImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.jpg *.jpeg)", options=options)
        if fileName:
            #Affichage du chemin de l'image sur l'UI
            self.ui.labeltext_chemin.setText(fileName)
            #Conversion Image en QPixmap
            ImgIn = QImage(fileName)
            #Affichage de l'image dans un label, réglage des dimensions
            largeur_ImgIn = ImgIn.width()
            hauteur_ImgIn = ImgIn.height()
            if largeur_ImgIn > hauteur_ImgIn :
                ImgIn = ImgIn.scaledToWidth(self.largeur_frame, Qt.SmoothTransformation)
            else:
                ImgIn = ImgIn.scaledToHeight(self.hauteur_frame, Qt.SmoothTransformation)
            self.ui.label_ImgIn.setPixmap(QPixmap.fromImage(ImgIn))

            #Définition de l'image en PIL
            image = ouvrirImageIn(fileName)

            self.ImageInIsSet = True
            self.ImageNdg = IsNdg(image)

            #Si l'image d'origine est définie
            if(self.ImageInIsSet):
                if(self.ImageNdg):
                    self.ui.bouton_poivresel.setEnabled(True)
                    self.ui.bouton_gaussien.setEnabled(True)
                else:
                    self.ui.bouton_chromatique.setVisible(True)
                    self.ui.bouton_chromatique.setEnabled(True)

            #Lien entre les boutons liés à "image" et les fonctions
            self.ui.bouton_poivresel.clicked.connect(lambda : bruit_poivre_et_sel(image, self.noise_densite, self))
            self.ui.bouton_gaussien.clicked.connect(lambda : bruit_gaussien(image, self.noise_ecart_type, self))
            self.ui.bouton_chromatique.clicked.connect(lambda : bruit_chromatique(image, self.noise_ecart_type, self))

            self.ui.radio_gaussien.toggled.connect(lambda : self.set_choix_filtre(1))
            self.ui.radio_bilateral.toggled.connect(lambda : self.set_choix_filtre(2))
            self.ui.radio_moyenneur.toggled.connect(lambda : self.set_choix_filtre(3))
            self.ui.radio_median.toggled.connect(lambda : self.set_choix_filtre(4))
            self.ui.radio_laplacien.toggled.connect(lambda : self.set_choix_filtre(5))


            self.ui.bouton_valider.clicked.connect(lambda : self.valider_filtres(image, self.choix_filtre))






if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
