##Evaluation de la robustesse d'un mot de passe

minuscule = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
majuscule = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
chiffre =  ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
caracteres_speciaux = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '@']

def robustesse(mdp : str):
    """robustesse(mdp) renvoie la robustesse de mdp, c'est-à-dire une note sur 5 représentant la difficulté que le pirate rencontrera lors de la tentative de cassage de mdp (5 étant la difficulté maximale).
    La note est nulle si mdp a une longueur inférieure ou égale à 8, ou s'il apparaît dans un dictionnaire, et est sinon calculée comme suit: on ajoute 0.5 à chaque fois que la longueur augmmente de 1 à partir de 8, et on ajoute 0.125 pour chaque type de caractères différents, avec un maximum de 2 * 0.125 = 0.25 par type (correspondant à deux caractères par type)."""
    n = len(mdp)
    if n >= 16:
        n = 16
    if n <= 8 or dico(mdp):
        return 0.0
    else:
        nbtype = [0, 0, 0, 0]
        for k in mdp:
            if k in minuscule:
                nbtype[0] = min([nbtype[0] + 1,2])
            elif k in majuscule:
                nbtype[1] = min([nbtype[1] + 1,2])
            elif k in chiffre:
                nbtype[2] = min([nbtype[2] + 1,2])
            else:
                nbtype[3] = min([nbtype[3] + 1,2])
        return 0.5 * (n  - 8) + (nbtype[0] + nbtype[1] + nbtype[2] + nbtype[3]) / 8

def dico(mdp : str):
    """dico(mdp) renvoie True si mdp appartient à l'un des dictionnaires de la base de donnée, False sinon."""
    fid1 = open("C:/Users/ffore/Desktop/TIPE/Base_donnee/Dictionnaires/français.txt", 'r', encoding = 'UTF-8')
    lignes1 = fid1.readlines()
    fid1.close()
    fid2 = open("C:/Users/ffore/Desktop/TIPE/Base_donnee/Dictionnaires/mot_de_passe.txt", 'r', encoding = 'UTF-8')
    lignes2 = fid2.readlines()
    fid2.close()
    return not (mdp in lignes1 or mdp in lignes2)