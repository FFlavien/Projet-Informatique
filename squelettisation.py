import os
os.chdir("C:/Users/ffore/OneDrive/Documents/TIPE/")

from math import sqrt, erf, sqrt, pi
from copy import deepcopy
from pile_priorite import *
from binarisation import binarisation

##Dimension d'une matrice

def dimension(mat : list) -> (int, int):
    '''dimension(mat) renvoie les dimensions de la matrice mat : (lignes, colonnes).'''
    return len(mat), len(mat[0])

##Algorithmes de calculs

def moyenne(l : list) -> float:
    '''moyenne(l) renvoie la moyenne de l (tous les poids sont égaux à 1).'''
    assert type(l) == list
    n = len(l)
    m = 0
    for i in range(n):
        m = m + l[i]
    return m / n

def ecart_type(l : list, moy : float) -> float:
    '''ecart_type(l, moy) renvoie l'écart type des éléments de l à la moyenne moy.'''
    assert type(l) == list and type(moy) == float
    e = 0
    n = len(l)
    for p in l:
        e = e + (p - moy) ** 2
    return sqrt(e / n)

def tau(alpha : float, sigma : float, mu : float, x : int, n : int) -> float:
    '''tau(alpha, sigma, mu, x, n) effectue le calcul de tau, nécessaire à l'évaluation du paramètre local de la squelettisation.'''
    assert type(alpha) == float and type(sigma == float) and type(mu) == float and type(x) == int and type(n) == int and n > 1
    return fncr_rec((1 - (1 - alpha) ** (1/(n - 1))) * fncr((x - mu) / sigma))

def fncr(x : float) -> float:
    '''f est la fonction de répartition de la loi normale centrée réduite.'''
    assert type(x) == float
    return 1 / 2 + erf(x / sqrt(2)) / 2

def fncr_rec(x : float) -> float:
    '''fncr_rec est la réciproque de fncr.'''
    assert type(x) == float
    return sqrt(2) * erf_rec(2 * x - 1)

def erf_rec(x : float) -> float:
    '''erf_rec est la réciproque de la fonction erf (erreur).'''
    assert type(x) == float
    return 1 / 2 * sqrt(pi) * (x + pi / 12  * (x ** 3) + 7 * (pi ** 2) * (x ** 5) / 480  + 127 * (pi ** 3) * (x ** 7) / 40320 + 4369 * (pi ** 4) * (x ** 9) / 5806080 + 34807 * (pi ** 5) / 182476800 * (x ** 11))

##Algorithme utile

def coordonnees_voisins(i : int, j : int) -> list:
    '''coordonnees_voisins(i, j) renvoie la liste des coordonnées des voisins de (i,j), en partant du pixel en haut à gauche, et en tournant dans le sans anti-horaire.'''
    assert type(i) == int and type(j) == int
    return [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1), (i-1, j)]

##Points particuliers

def coupe_sombre(l : list, i : int, j : int) -> (list, list, list):
    '''coupe_sombre(l, i, j) renvoie la coupe sombre du pixel de coordonnées i,j, les coordonnées de ses voisins les plus sombres et une liste de booléens, représentant les composantes sombres qui sont 4-connexes.'''
    assert type(l) == list and type(i) == int and type(j) == int
    coupe, coord_sombre, t, est_4_conn = [], [], [], []
    verite = False
    co_voisins = coordonnees_voisins(i, j)
    for x in range(len(co_voisins)):
        a, b = co_voisins[x]
        if l[a][b][0] < l[i][j][0]:
            t.append(l[a][b][0])
            coord_sombre.append((a,b))
            if x % 2 == 1: #la composante est 4-connexe
                verite = True
        elif t != []:
            coupe.append(t)
            t = []
            est_4_conn.append(verite)
            verite = False
    if t != []:
        assert len(coupe) == len(est_4_conn)
        if l[i - 1][j - 1][0] < l[i][j][0] and len(coupe) >= 1:
            for k in t:
                coupe[0].append(k)
            est_4_conn[0] = est_4_conn[0] or verite
        else:
            coupe.append(t)
            est_4_conn.append(verite)
    return coupe, coord_sombre, est_4_conn

def extremite(l : list, i : int, j : int) -> bool:
    '''extremite(l, i, j) renvoie True si le pixel (i,j) est extrémité.'''
    assert type(l) == list and type(i) == int and type(j) == int
    coupe, _, _ = coupe_sombre(l, i, j)
    return len(coupe) == 1 and len(coupe[0]) == 7

def pic(l : list, i : int, j : int) -> bool:
    '''pic(l, i, j) renvoie True si le pixel (i, j) est pic.'''
    assert type(l) == list and type(i) == int and type(j) == int
    coupe, _, _ = coupe_sombre(l, i, j)
    return len(coupe) == 1 and len(coupe[0]) == 8

def simple(l : list, i : int, j : int) -> bool:
    '''simple(l, i, j) renvoie True si le pixel (i,j) est simple.'''
    assert type(l) == list and type(i) == int and type(j) == int
    coupe, _, est_4_conn = coupe_sombre(l, i, j)
    return len(coupe) == 1 and True in est_4_conn and len(coupe[0]) != 8

##Algorithmes de traitements des impuretés

def nettoie(l : list) -> None:
    '''nettoie(l) nettoie le squelette de la liste l.'''
    assert type(l) == list
    print("Nettoyage des impuretés.")
    enleve_simple(l)
    enleve_isole(l)
    enleve_aberrations(l)
    enleve_simple(l)
    enleve_isole(l)
    return None

def enleve_isole(l : list) -> None:
    '''enleve_isole(l) enlève les points isolés (blanc et que des voisins noirs) de la liste.'''
    assert type(l) == list
    n, p = dimension(l)
    for i in range(1, n - 1):
        for j in range(1, p - 1):
            co = coordonnees_voisins(i, j)
            if l[i][j][0] == 255 and [l[a][b][0] for (a,b) in co].count(255) == 0:
                l[i][j] = [0,0,0]
    return None

def enleve_aberrations(l : list) -> None:
    '''enleve_aberrations(l) enlève les aberrations du squelette de la liste l.'''
    assert type(l) == list
    n, p = dimension(l)
    for i in range(1, n - 1):
        for j in range(1, p - 1):
            if l[i][j][0] == 255 and extremite(l, i, j):
                remonte_aberrations(l, i, j, [])
    return None

def remonte_aberrations(l : list, i : int, j : int, ab: list) -> None:
    '''remonte_aberrations(l, i, j, ab) parcours l'aberration du pixel i,j, remplit la liste de l'aberration ab et si elle a une longueur plus petite que c lorsque l'algorithme arrive à une bifurcation ou une terminaison, elle met à 0 tous les pixels de l'aberration.'''
    assert type(l) == list and type(i) == int and type(j) == int and type(ab) == list
    n, p = dimension(l)
    if len(ab) >= 20:
        return None
    else:
        if i == n - 1 or i == 0 or j == p - 1 or j == 0:
                for a,b in ab:
                    l[a][b] = [0,0,0]
        else:
            co = [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]
            ent = [l[x][y][0] for (x,y) in co]
            if (ent.count(255) == 1 and len(ab) != 0) or (ent.count(255) != 2 and ent.count(255) != 1):
                for a,b in ab:
                    l[a][b] = [0,0,0]
            else:
                for a,b in co:
                    if l[a][b][0] == 255 and not ((a,b) in ab):
                        ab.append((i, j))
                        remonte_aberrations(l, a, b, ab)
    return None

def enleve_simple(l : list) -> None:
    '''enleve_simple(l) enlève les points simples et non extrémités de l.'''
    assert type(l) == list
    n, p = dimension(l)
    for i in range(1, n - 1):
        for j in range(1, p - 1):
            if simple(l, i, j) and not extremite(l, i, j):
                l[i][j] = [0,0,0]
    return None

##Squelettisation

def abaissable(l : list, initiale : list, i : int, j : int, alpha : float) -> bool:
    '''abaissable(l, initiale, i, j, alpha) renvoie true si le pixel (i,j) est abaissable (le paramètre lambda est calculé localement), avec l la liste évoluant, initiale la liste des valeurs initiales, et alpha le paramètre de précision, fixé par défaut à 10 ** -3.'''
    assert type(l) == list and type(i) == int and type(j) == int and type(alpha) == float
    coupe, coord_sombre, est_4_conn = coupe_sombre(l, i, j)

    #nombre de composantes connexes
    k = len(coupe)

    #liste de tous les pixels plus sombres avec le pixel i,j
    coupe_sombre_complete = [l[i][j][0]]
    for a in coupe:
        for b in a:
            coupe_sombre_complete.append(b)

    #nombre de pixels plus sombres
    n = len(coupe_sombre_complete)

    if k == 1:

        #liste des valeurs initiales des pixels plus sombres et du pixel i,j
        coupe_initiale = [initiale[z][r][0] for z,r in coord_sombre]
        coupe_initiale.append(initiale[i][j][0])

        mu = moyenne(coupe_initiale)
        sigma = ecart_type(coupe_initiale, mu)

        if n == 9:
            #pic
            if sigma == 0:
                return min(coupe_initiale) >= mu
            return min(coupe_initiale) >= mu + sigma * tau(alpha, sigma, mu, initiale[i][j][0], n)
        elif n == 8:
            #extrémité
            if sigma == 0:
                return min(coupe_initiale) >= mu
            return min(coupe_initiale) >= mu + sigma * tau(alpha, sigma, mu, initiale[i][j][0], n)
        else:
            return False
    elif k >= 2 and est_4_conn.count(True) >= 2:
        #crête
        co_voisins = coordonnees_voisins(i, j)
        #liste des composantes 4_connexes
        comp_4_conn = [coupe[a] if est_4_conn else _ for a in range(k)]

        #k représente désormais le nombre de composantes 4_connexes
        k = len(comp_4_conn)

        #valeurs du voisinage en prenant les valeurs courantes
        voisinage_courant = [l[a][b][0] for (a,b) in co_voisins]
        voisinage_courant.append(l[i][j][0])

        #valeurs du voisinage en prenant les valeurs initiales
        voisinage_initial = [initiale[a][b][0] for (a,b) in co_voisins]
        voisinage_initial.append(initiale[i][j][0])

        mu = moyenne(voisinage_courant)
        sigma = ecart_type(voisinage_initial, moyenne(voisinage_initial))

        if k == 2:
            alpha0 = 0.0316
        elif k == 3:
            alpha0 = 0.0184
        elif k == 4:
            alpha0 = 0.0130
        o = 0
        for x in range(len(comp_4_conn)):
            if sigma == 0:
                if min(comp_4_conn[x]) >= mu:
                    o = o + 1
            elif min(comp_4_conn[x]) >= mu + sigma * tau(alpha0, sigma, mu, l[i][j][0], len(comp_4_conn[x]) + 1):
                o = o + 1
        return o >= k - 1
    else:
        return False

def squelettisation(l : list, alpha : int = 10**-3) -> None:
    '''squelettisation(l, alpha) effectue la squelettisation paramétrée de la liste l avec la précision alpha, valant à défaut 10**-3 (modifie l), et binarise l'image obtenue.'''
    assert type(l) == list and type(alpha) == float
    print("Squelettisation de l'image.")
    initiale = deepcopy(l)
    pile_prio = pile_priorite_vide()
    n, p = dimension(l)
    for i in range(1, n - 1):
        for j in range(1, p - 1):
            if abaissable(l, initiale, i, j, alpha) or (simple(l, i, j) and not extremite(l, i, j)):
                empile(pile_prio, (i,j), l[i][j][0])
    while not est_vide(pile_prio):
        (i, j) = depile(pile_prio)
        coordonnees = coordonnees_voisins(i, j)
        if abaissable(l, initiale, i, j, alpha) or (simple(l, i, j) and not extremite(l, i, j)):
            l[i][j] = [max([l[a][b][0] for a,b in coordonnees if l[a][b][0] < l[i][j][0]])] * 3
        for a,b in coordonnees:
            if (a != 0 and a != n - 1 and b != 0 and b != p - 1) and (abaissable(l, initiale, a, b, alpha) or (simple(l, a, b) and not extremite(l, a, b))):
                empile(pile_prio, (a, b), l[a][b][0])
    binarisation(l)
    nettoie(l)
    return None