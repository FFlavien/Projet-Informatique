import os
os.chdir("C:/Users/ffore/OneDrive/Documents/TIPE/")

from hachage import md5

def premiers_bits(mess : str, x : int, prefixe : str) -> str:
    '''premiers_bits(mess, x, prefixe) renvoie les 2x premiers bits de l'empreinte numérique de la concaténation de préfixe et mess par md5.'''
    assert type(mess) == str and type(x) == int and type(prefixe) == str
    return md5(prefixe + mess)[:x * 2]

def young(prefixe : str, nb : int) -> (str, str):
    '''young(prefixe, nb) renvoie deux mots de passe, ayant les nb premiers caractères et les mêmes 2 * nb premiers bits une fois hachés par md5.'''
    assert type(prefixe) == str and type(nb) == int
    lent = premiers_bits(prefixe, nb, prefixe)
    rapide = premiers_bits(lent, nb, prefixe)
    while lent != rapide:
        lent = premiers_bits(lent, nb, prefixe)
        rapide = premiers_bits(premiers_bits(rapide, nb, prefixe), nb, prefixe)
    long_cycle = 0
    lent = prefixe
    while lent != rapide:
        m1 = rapide
        m0 = lent
        lent = premiers_bits(lent, nb, prefixe)
        rapide = premiers_bits(rapide, nb, prefixe)
        long_cycle += 1
    if long_cycle == 0:
        return "Aucune collision trouvée !\n"
    return prefixe + m0, prefixe + m1