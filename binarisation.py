##Dimension d'une matrice

def dimension(mat : list) -> (int, int):
    '''dimension(mat) renvoie les dimensions de la matrice mat : (lignes, colonnes).'''
    return len(mat), len(mat[0])

##Algorithmes de calcul

def somme(l : list) -> float:
    '''somme(l) renvoie la somme des éléments de l.'''
    assert type(l) == list
    s = 0
    for k in l:
        s = s + k
    return s

def moy_pond(l : list, p : int) -> float:
    '''moy_pond(l , p) effectue une moyenne pondérée de la liste m, sachant que le premier élément de la liste l est le pixel p.'''
    assert type(l) == list and type(p) == int
    s = somme(l)
    if len(l) == 0 or s == 0:
        return 0
    moy = 0
    for k in range(len(l)):
        moy += (k + p) * l[k]
    return moy / s

def indice_max(l : list) -> int:
    '''indice_max(l) renvoie l'indice de la première occurence du maximum de la liste l.'''
    assert type(l) == list
    m = 0
    for k in range(1, len(l)):
        if l[k] > l[m]:
            m = k
    return m

def decoupe(l :list, taille : int) -> list:
    '''decoupe(l, taille) découpe la liste l, représentant une image, en bloc de taille * taille pixels.'''
    ligne = []
    n, p = dimension(l)
    for i in range(n//taille + 1):
        temp = l[taille * i: taille * (i + 1)]
        bloc = []
        for j in range(p//taille + 1):
            att = []
            for k in range(len(temp)):
                att.append(temp[k][taille * j: taille * (j + 1)])
            bloc.append(att)
        ligne.append(bloc)
    return ligne

##Algorithmes de binarisation

def histogramme(l : list) -> list:
    '''histogramme(l) renvoie l'histogramme de la liste l.'''
    assert type(l) == list
    h = [0 for _ in range(256)]
    for i in l:
        for j in i:
            h[j[0]] += 1
    return h

def seuil(l : list, s : int) -> None:
    '''seuil(l, s) effectue un seuillage de la liste l au niveau s (modifie l en place).'''
    assert type(l) == list and type(s) == int
    n, p = dimension(l)
    for i in range(n):
        for j in range(p):
            if l[i][j][0] <= s:
                l[i][j] = [0, 0, 0]
            else:
                l[i][j] = [255, 255, 255]
    return None

def otsu(l : list) -> int:
    '''otsu(l) renvoie le seuil détecté avec la méthode d'Otsu.'''
    assert type(l) == list
    histo = histogramme(l)
    w1, w2, mu1, mu2 = 0, 1, 0, moy_pond(histo, 0)
    sigma = [w1 * w2 * (mu1 - mu2) ** 2]
    total = somme(histo)
    for i in range(1,256):
        temp = somme(histo[i:])
        w1 = (total - temp)/ total
        w2 = temp / total
        mu1 = moy_pond(histo[:i],0)
        mu2 = moy_pond(histo[i:],i)
        sigma.append(w1 * w2 * (mu1 - mu2) ** 2)
    return indice_max(sigma)

def binarisation(l : list, taille : int = 20) -> None:
    '''binarisation(l, taille) effectue la binarisation de l avec la méthode d'Otsu (modifie l en place) en découpant la liste l en sous listes représentants des images de taille * taille pixels.'''
    assert type(l) == list and type(taille) == int
    print("Binarisation du squelette.")
    ligne = decoupe(l, taille)
    c,d = dimension(ligne)
    for a in range(c):
        for b in range(d):
            seuil(ligne[a][b], otsu(ligne[a][b]))
    n, p = dimension(l)
    for i in range(n):
        for j in range(p):
            l[i][j] = ligne[i//taille][j//taille][i%taille][j%taille]
    return None