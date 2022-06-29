import os
os.chdir("C:/Users/ffore/OneDrive/Documents/TIPE/")

from math import sqrt, acos, pi
from hachage import md5
from code_ascii import tables_ascii

##Algorithmes de calculs

def barycentre(ter : list, bif : list) -> ((float, float), (float, float)):
    '''barycentre(ter, bif) renvoie les coordonnées des barycentres des terminaisons et des bifurcations.'''
    assert type(ter) == list and type(bif) == list
    xb, yb = 0, 0
    xt, yt = 0, 0
    nb, nt = len(bif), len(ter)
    assert nb != 0 and nt != 0
    for i,j in bif:
        xb += i
        yb += j
    for i,j in ter:
        xt += i
        yt += j
    return (xt / nt, yt / nt), (xb / nb, yb / nb)

def crossing_number(l : list, i : int, j : int) -> int:
    '''crossing_number(l, i, j) renvoie le crossing number (le nombre de transitions noir/blanc et blanc/noir) voisinage du pixel (i,j) de l.'''
    assert type(l) == list and type(i) == int and type(j) == int
    voisins = []
    coordonnees = [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1), (i-1, j)]
    for m, p in coordonnees:
        voisins.append(l[m][p][0])
    temp = voisins[-1]
    a = 0
    for k in voisins:
        if k != temp:
            a += 1
            temp = k
    return a

def somme(l : list) -> float:
    '''somme(l) renvoie la somme des éléments de l.'''
    assert type(l) == list
    s = 0
    for k in l:
        s = s + k
    return s

##Algorithmes de tris

def decoupe(l : list) -> (list, list):
    '''decoupe(l) coupe la liste l en 2 listes.'''
    assert type(l) == list
    n = len(l)
    return l[:n//2], l[n//2:]

def fusion(l1 : list, l2 : list) -> list:
    '''fusion(l1, l2) fusionne les listes l1 et l2 supposées triées par ordre croissant en une liste elle aussi triée par ordre croissant.'''
    assert type(l1) == list and type(l2) == list
    if l1 == []:
        return l2
    elif l2 == []:
        return l1
    else:
        l = []
        while l1 != [] and l2 != []:
            if l1[0][0] <= l2[0][0]:
                l.append(l1[0])
                l1 = l1[1:]
            else:
                l.append(l2[0])
                l2 = l2[1:]
        if l1 != []:
            for k in l1:
                l.append(k)
        elif l2 != []:
            for k in l2:
                l.append(k)
        return l

def tri_fusion(l : list) -> (list, list):
    '''tri_fusion(l) effectue le tri de la liste l avec la méthode de tri fusion, où l est une liste de couple, le tri étant basé sur la première composante de chaque couple.'''
    assert type(l) == list
    if l == [] or len(l) == 1:
        return l
    else:
        l1, l2 = decoupe(l)
        return fusion(tri_fusion(l1), tri_fusion(l2))

##Changement d'écritures

def hex_dec(mess : str) -> int:
    ''''hex_dec(mess) transforme le mess de l'héxadécimal vers la base 10.'''
    assert type(mess) == str
    dico = {'0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, 'a' : 10, 'b' : 11, 'c' : 12, 'd' : 13, 'e' : 14, 'f' : 15}
    s = 0
    n = len(mess)
    for k in range(n):
        s = s + dico[mess[len(mess) - 1 - k]] * 16 ** k
    return s

def base_mdp(nbi : int) -> str:
    '''base_mdp(nbi) transforme l'entier nbi en un mot de passe en utilisant la base 95.'''
    assert type(nbi) == int
    dic_ascii, _ = tables_ascii()
    mdp = ""
    temp = nbi
    while temp != 0:
        a = str(temp % 95 + 32)
        while len(a) < 3:
            a = '0' + a
        mdp = dic_ascii[a] + mdp
        temp = temp // 95
    return mdp

##Algorithmes principaux

def terminaison_bifurcation(l : list) -> (list, list):
    '''termminaison_bifurcation(l) renvoie les listes des coordonnées des pixels terminaisons et bifurcations de l.'''
    assert type(l) == list
    mat_cro_num, ter, bif = [], [], []
    for i in range(1, len(l) - 1):
        temp = []
        for j in range(1, len(l[0]) - 1):
            if l[i][j] == [255,255,255]:
                temp.append(crossing_number(l, i, j))
            else:
                temp.append(0)
        mat_cro_num.append(temp)
    for i in range(1, len(l) - 1):
        for j in range(1, len(l[0]) - 1):
            if mat_cro_num[i - 1][j - 1] == 2:
                ter.append((i, j))
            elif mat_cro_num[i - 1][j - 1] == 6 or mat_cro_num[i - 1][j - 1] == 8:
                bif.append((i,j))
    return ter, bif

def extraction_mdp(l: list) -> str:
    '''extraction_mdp(l) renvoie le mot de passe extrait de l, où l est une liste représentant une image binarisée.'''
    print("Recherche des minuties et extraction du mot de passe.")
    ter, bif = terminaison_bifurcation(l)
    print(len(bif), " bifurcations trouvées.")
    print(len(ter), " terminaisons trouvées.")
    dter, dbif = [], []
    (xbt, ybt), (xbb, ybb) = barycentre(ter, bif)

    abif = []
    for i,j in bif:
        dx, dy = i - xbb, j - ybb
        r = sqrt(dx ** 2 + dy ** 2)
        assert r != 0
        dbif.append(int(r))
        teta = abs(acos(dy / r))
        if dx < 0:
            teta = (- teta) % (2 * pi)
        abif.append(teta)

    assert len(dbif) == len(abif)
    assert len(dbif) >= 6

    pour_tri = [(dbif[i], abif[i]) for i in range(len(dbif))]
    l_coupleb = tri_fusion(pour_tri)[:6]
    dbif = [x for (x, y) in l_coupleb]
    encore_pour_tri = [(y,x) for (x,y) in l_coupleb]
    l_coupleb2 = tri_fusion(encore_pour_tri)
    abif = [x for (x,_) in l_coupleb2]

    angle_bif = [int((2 * pi - abif[len(abif) - 1] + abif[0]) * 10) / (10)]
    for k in range(len(abif) - 1):
        angle_bif.append(int((abif[k + 1] - abif[k]) * 10) / (10))
    assert len(angle_bif) == 6
    assert somme(angle_bif) >= 5.8 and somme(angle_bif) <= 6.6

    encore_tri = [(angle_bif[i], None) for i in range(len(angle_bif))]
    l_coupleb2 = tri_fusion(encore_tri)
    angle_bif = [l_coupleb2[i][0] for i in range(len(l_coupleb2))]

    ater = []
    for i,j in ter:
        dx, dy = i - xbb, j - ybb
        r = sqrt(dx ** 2 + dy ** 2)
        assert r != 0
        dter.append(int(r))
        teta = abs(acos(dy / r))
        if dx < 0:
            teta = (- teta) % (2 * pi)
        ater.append(teta)

    assert len(dter) == len(ater)
    assert len(dter) >= 6

    pour_tri = [(dter[i], ater[i]) for i in range(len(dter))]
    l_couplet = tri_fusion(pour_tri)[:6]
    dter = [x for (x,_) in l_couplet]
    encore_pour_tri = [(y,x) for (x,y) in l_couplet]
    l_couplet2 = tri_fusion(encore_pour_tri)
    ater = [x for (x,_) in l_couplet2]

    angle_ter = [int((2 * pi - ater[len(abif) - 1] + ater[0]) * 10) / (10)]
    for k in range(len(ater) - 1):
        angle_ter.append(int((ater[k + 1] - ater[k]) * 10) / 10)
    assert len(angle_ter) == 6
    assert somme(angle_ter) >= 5.8 and somme(angle_ter) <= 6.6

    encore_tri = [(angle_ter[i], None) for i in range(len(angle_ter))]
    l_couplet2 = tri_fusion(encore_tri)
    angle_ter = [l_couplet2[i][0] for i in range(len(l_couplet2))]

    chaine = ""
    for liste in [dter, angle_ter, dbif, angle_bif]:
        for i in liste:
            car = str(int(i))
            while len(car) != 3:
                car = "0" + car
            chaine = chaine + car

    return base_mdp(hex_dec(md5(chaine)))