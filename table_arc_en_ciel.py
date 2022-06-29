import os
os.chdir("C:/Users/ffore/OneDrive/Documents/TIPE/")

from hachage import md5
from code_ascii import tables_ascii
from random import randint

##Algorithmes de calculs

def hex_dec(mess : str) -> int:
    ''''hex_dec(mess) transforme le mess de l'héxadécimal vers la base 10.'''
    assert type(mess) == str
    dico = {'0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, 'a' : 10, 'b' : 11, 'c' : 12, 'd' : 13, 'e' : 14, 'f' : 15}
    s = 0
    n = len(mess)
    for k in range(n):
        s = s + dico[mess[len(mess) - 1 - k]] * 16 ** k
    return s

def reduction(mess : str, x : str) -> str:
    '''reduction(mess, x) transforme l'empreinte mess en un nouveau mot de passe commençant par x.'''
    assert type(mess) == str and type(x) == str
    while len(x) != 3:
        x = '0' + x
    mot = ""
    motd = hex_dec(mess)
    dico_ascii, _ = tables_ascii()
    while motd != 0:
        q = str(motd % 95 + 32)
        motd = motd // 95
        while len(q) != 3:
            q = '0' + q
        mot = dico_ascii[str(q)] + mot
    return dico_ascii[x] + mot

def bout(mot : str) -> str:
    '''bout(mot) renvoie l'extrémité de la ligne de mot dans une table arc-en-ciel, en effectuant 95 réductions et hachages successifs.'''
    assert type(mot) == str
    for k in range(95):
        mot = reduction(md5(mot), str(k + 32))
    return mot

##Algorithme de recherche

def recherche(empr : str, table : str) -> bool or str:
    '''recherche(empr, table) recherche le mot de passe correspondant à l'empreinte numérique empr dans la table table.'''
    assert type(empr) == str and type(table) == str
    nom = "C:/Users/ffore/OneDrive/Documents/TIPE/Base_donnees/" + table + ".txt"
    fid = open(nom, 'r')
    nbred = int(fid.readline().strip("\n"))
    lignes = fid.readlines()
    fid.close()
    l1 = []
    l2 = []
    h = 0
    verite = True
    for k in lignes:
        m = k.split("°")
        l1.append(m[1].strip("\n"))
        l2.append(m[0])
    i = nbred - 1
    while i != -1:
        mot = ''
        while not mot in l1 and i != -1:
            mot = reduction(empr, str(i + 32))
            for k in range(i + 1, nbred):
                mot = reduction(md5(mot), str(k + 32))
            i -= 1
        if mot in l1:
            h = 0
            while verite and h < len(l1):
                if l1[h] == mot:
                    mdp = l2[h]
                    for l in range(i):
                        mdp = reduction(md5(mdp), str(l + 32))
                    verite = not md5(mdp) == empr
                    if not verite:
                        i = -1
                h += 1
        else:
            mdp = False
    return mdp

##Création de la tabla arc_en_ciel

def creation(n : int) -> None:
    '''creation(n) construit la table arc-en-ciel avec la fonction md5 et des fonctions de réductions qui sont des changements de base 95 en base 16, avec ajout d'un caractère différent à chaque étape pour optimisation (ajoute n lignes si la table existe déjà).'''
    nom = "C:/Users/ffore/OneDrive/Documents/TIPE/Base_donnees/table.txt"
    assert type(n) == int
    dico_ascii, _ = tables_ascii()
    dictio = {}
    fid = open(nom, "a")
    if fid.readlines() == []:
        fid.write("95\n")
    mdp = ""
    for k in range(n):
        o = randint(0,15)
        while len(mdp) != o:
           i = str(randint(32, len(dico_ascii) + 32 - 1))
           while len(i) != 3:
               i = '0' + i
           mdp = mdp + dico_ascii[i]
        if not mdp in dictio:
            print("aller")
            dictio[mdp] = k
            mdpi = mdp
            mdp = bout(mdp)
            fid.write(mdpi + "°" + mdp + "\n")
    fid.close()
    return None