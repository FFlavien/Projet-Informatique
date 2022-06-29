import os
os.chdir("C:/Users/ffore/OneDrive/Documents/TIPE/")

from code_ascii import tables_ascii
from math import sin, floor

dic_code, dic_char = tables_ascii()

##Opérateurs sur les nombres binaires

def et(a : str, b : str) -> str:
    '''et(a, b) est l'opérateur "et logique termes à termes" entre a et b.
    Conditions : a et b sont deux chaînes de caractères de même longueur, représentant des nombres binaires.'''
    assert type(a) == str and type(b) == str and len(a) == len(b)
    mot = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "1":
            mot = mot + "1"
        else:
            mot = mot + "0"
    return mot

def ou(a : str, b : str) -> str:
    '''ou(a, b) est l'opérateur "ou logique termes à termes" entre a et b.
    Conditions : a et b sont deux chaînes de caractères de même longueur, représentant des nombres binaires.'''
    assert type(a) == str and type(b) == str and len(a) == len(b)
    mot = ""
    for i in range(len(a)):
        if a[i] == "0" and b[i] == "0":
            mot = mot + "0"
        else:
            mot = mot + "1"
    return mot

def non(a : str) -> str:
    '''non(a) est l'opérateur "négation termes à termes" de a.
    Conditions : a est un chaîne de caractères représentant un nombre binaire.'''
    assert type(a) == str
    mot = ""
    for i in range(len(a)):
        mot = mot + str((int(a[i]) + 1) % 2)
    return mot

def xou(a : str, b : str) -> str:
    '''xou(a, b) est l'opérateur "ou exclusif logique termes à termes" entre a et b.
    Conditions : a et b sont deux chaînes de caractères de même longueur, représentant des nombres binaires.'''
    assert type(a) == str and type(b) == str and len(a) == len(b)
    mot = ""
    for i in range(len(a)):
        mot = mot + str((int(a[i]) + int(b[i])) % 2)
    return mot

def rotationg(mess : str, n : int) -> str:
    '''rotationg(mess, n) effectue une rotation de n bits vers la gauche sur le message mess.
    Conditions : mess est une chaîne de caractères, représentant un nombre binaire et n un entier.'''
    assert type(n) == int and type(mess) == str
    n = n % len(mess)
    code = mess[n:] + mess[:n]
    return code

##Changements d'écritures

def str_ascii(mdpi : str) -> str:
    '''str_ascii(mdpi) convertit mdpi, une chaine de caractères, en convention ASCII.'''
    assert type(mdpi) == str
    mdpc = ""
    for i in mdpi:
        mdpc = mdpc + dic_char[i]
    return mdpc

def dec_binaire(a : int, n : int) -> str:
    '''dec_binaire(a, n) convertit a de la base 10 vers la base 2 sur n bits.'''
    assert type(a) == int and type(n) == int and 2 ** n > a
    (q, r) = (0, a)
    mdp = ''
    for i in range(n):
        q = r // 2 ** (n - 1 - i)
        mdp = mdp + str(q)
        r = r % 2 ** (n - 1 - i)
    return mdp

def binaire_dec(b : str) -> int:
    '''binaire_dec(b) convertit b de la base 2 vers la base 10.'''
    assert type(b) == str
    somme = 0
    n = len(b)
    for l in range(n):
        somme = somme + int(b[n - 1 - l]) * 2 ** l
    return somme

def endian(i : int, n : int) -> str:
    '''endian(i, n) convertit l'entier i de la base 10 vers la base 2 sur n bits avec la convention little-endian'''
    assert type(i) == int and type(n) == int
    mdpi = dec_binaire(i, n)
    mdp = ""
    for k in range(0, len(mdpi) - 7, 8):
        mdp = mdpi[k:k + 8] + mdp
    return mdp

##Algorithme de découpe

def decoupage(mot : str, n : int) -> list:
    '''decoupage(mot, n) découpe la chaîne de caractères mot en blocs de n caractères.'''
    assert type(mot) == str and type(n) == int and n * (len(mot) // n) == len(mot)
    return [mot[r * n : n + r * n] for r in range(len(mot) // n)]

##Algorithmes d'initialisations

def padding(mdpi : str, longueur : int) -> str:
    '''padding(mdpi, longueur) effectue l'étape de padding, et renvoie mdpi, auquel on a rajouté le bit 1, et autant de bits 0 que nécessaire pour avoir une longueur égale à 448 modulo 512, ainsi que la longueur du mot de passe initial en binaire (chaque caractère est représenté sur 8 bits) et avec la convention little endian.'''
    assert type(mdpi) == str and type(longueur) == int
    mdp = mdpi + "1"
    while (len(mdp) % 512) != 448:
        mdp = mdp + "0"
    long = endian(longueur * 8, 64)
    return mdp + long

def initialisation(mdpi : str) -> tuple:
    '''initialisation(mdpi) initialise les différentes constantes de l'algorithme, et effectue l'étape de padding.'''
    h0 = "01100111010001010010001100000001"
    h1 = "11101111110011011010101110001001"
    h2 = "10011000101110101101110011111110"
    h3 = "00010000001100100101010001110110"
    r = [7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22, 5,  9, 14, 20,  5, 9,
        14, 20,  5,  9, 14, 20,  5,  9, 14, 20, 4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        4, 11, 16, 23, 6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]
    k = []
    mdpbin = ""
    mdpascii = str_ascii(mdpi)
    list_car = [mdpascii[p:p + 3] for p in range(0, len(mdpascii) - 2, 3)]
    list_bin = [dec_binaire(int(u), 8) for u in list_car]
    for o in list_bin:
        mdpbin = mdpbin + o
    for i in range(64):
        k.append(floor(abs(sin(i + 1)) * 2 ** 32))
    return h0, h1, h2, h3, r, k, padding(mdpbin, len(mdpi))

##Algorithme prinicipal

def md5(mdpi : str):
    '''md5(mdpi) renvoie l'empreinte numérique du mot de passe mdpi par la fonction de hachage md5.'''
    h0, h1, h2, h3, r, k, mdpbin = initialisation(mdpi)
    bloc_512 = decoupage(mdpbin, 512)
    for p in bloc_512:
        bloc_32 = decoupage(p, 32)
        bloc_32 = [endian(binaire_dec(bloc_32[k]),32) for k in range(len(bloc_32))]
        a = h0
        b = h1
        c = h2
        d = h3
        for i  in range(64):
            if i >= 0 and i <= 15:
                f = ou(et(b, c), et(non(b), d))
                g = i
            elif i >= 16 and i <= 31:
                f = ou(et(d, b), et(non(d), c))
                g = (5 * i + 1) % 16
            elif i >= 32 and i <= 47:
                f = xou(xou(b, c), d)
                g = (3 * i + 5) % 16
            elif i >= 48 and i <= 63:
                f = xou(c, ou(b, non(d)))
                g = (7 * i) % 16
            tempo = d
            d = c
            c = b
            z = rotationg(dec_binaire((binaire_dec(a) + binaire_dec(f) + k[i] + binaire_dec(bloc_32[g])) % (2 **32),32), r[i])
            b = dec_binaire((binaire_dec(z) + binaire_dec(b)) % (2 ** 32) ,32)
            a = tempo
        h0 = dec_binaire((binaire_dec(h0) + binaire_dec(a)) % (2 ** 32), 32)
        h1 = dec_binaire((binaire_dec(h1) + binaire_dec(b)) % (2 ** 32), 32)
        h2 = dec_binaire((binaire_dec(h2) + binaire_dec(c)) % (2 ** 32), 32)
        h3 = dec_binaire((binaire_dec(h3) + binaire_dec(d)) % (2 ** 32), 32)
    h0 = endian(binaire_dec(h0), 32)
    h1 = endian(binaire_dec(h1), 32)
    h2 = endian(binaire_dec(h2), 32)
    h3 = endian(binaire_dec(h3), 32)
    mdp = (str(hex(binaire_dec(h0 + h1 + h2 + h3)))).strip("0x")
    while len(mdp) != 32:
        mdp = '0' + mdp
    return mdp