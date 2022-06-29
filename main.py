import os
os.chdir("C:/Users/ffore/OneDrive/Documents/TIPE/")

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from squelettisation import squelettisation
from extraction_mdp import extraction_mdp
from robustesse_mdp import robustesse

##Dimension d'une matrice

def dimension(mat : list) -> (int, int):
    '''dimension(mat) renvoie les dimensions de la matrice mat : (lignes, colonnes).'''
    assert type(mat) == np.ndarray or type(mat) == list
    return len(mat), len(mat[0])

##Ouverture des images

def lit_valeurs_nb(nom_de_fichier : str) -> list:
    '''lit_valeurs_nb(nom_de_fichier) ouvre l'image nom_de_fichier et la renvoie, en noir et blanc.'''
    assert type(nom_de_fichier) == str
    print("Ouverture de l'image : " + nom_de_fichier)
    im = Image.open("C:/Users/ffore/OneDrive/Documents/TIPE/Base_donnees/" + nom_de_fichier)
    print("Taille de l'image : ", im.size)
    print("Mode : ", im.mode)
    print("Format : ", im.format)
    return formatage(np.array(im.convert('L')))

def formatage(l : np.array) -> list:
    '''formatage(l) transforme l'array numpy l en une liste où chaque pixel est codé sur 3 nombres identiques (nuances de gris, RGB).'''
    assert type(l) == np.ndarray
    n, p = dimension(l)
    val = [[[] for _ in range(1, p - 1)] for _ in range(1, n - 1)]
    for i in range(1, n - 1):
        for j in range(1, p - 1):
            temp = int(l[i][j])
            val[i - 1][j - 1] = [temp] * 3
    return val

##Traitement

def traitement(nom : str) -> None:
    assert type(nom) == str
    val = lit_valeurs_nb(nom)
    squelettisation(val)
    mdp = extraction_mdp(val)
    print("Robustesse : ", robustesse(mdp))
    plt.clf()
    plt.imshow(val)
    plt.show()
    return mdp