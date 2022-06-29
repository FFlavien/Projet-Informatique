##Une pile de priorité est une liste de deux éléments : une liste de 256 listes, représentant les différentes priorités de 0 à 255, et un entier représentant l'indice de la liste de plus petite priorité. L'entier est None si la pile est vide.

def pile_priorite_vide():
    '''Créer une pile de priorité vide : [[[], ..., []], None].'''
    return [[[] for _ in range(256)], None]

def empile(pile_prio, pixel : tuple, p : int):
    '''Empile pixel sur la pile de priorité, à la priorité p.'''
    assert p >= 0 and p < 256
    if pixel in pile_prio[0][p]:
        return None
    pile_prio[0][p].append(pixel)
    if pile_prio[1] == None:
        pile_prio[1] = p
    else:
        pile_prio[1] = min(p, pile_prio[1])
    return None

def est_vide(pile_prio):
    '''Renvoie True si la pile de priorité est vide, False sinon.'''
    return pile_prio[1] == None

def depile(pile_prio):
    '''Dépile l'élément de plus petite priorité.'''
    temp = pile_prio[1]
    if len(pile_prio[0][pile_prio[1]]) == 1:
        i = pile_prio[1] + 1
        while i < 256 and pile_prio[0][i] == []:
            i = i + 1
        if i == 256:
            pile_prio[1] = None
        else:
            pile_prio[1] = i
    return pile_prio[0][temp].pop()