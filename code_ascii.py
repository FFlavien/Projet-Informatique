def tables_ascii():
    '''Renvoie les dictionnaires des principaux caractères associés à leur code ascii et inversement.'''
    fid = open("C:/Users/ffore/OneDrive/Documents/TIPE/Base_donnees/ascii.txt", 'r')
    lignes = fid.readlines()
    dic_char = {}
    dic_code = {}
    for k in range(len(lignes) // 2): #il y a un nombre paire de lignes
        dic_char[lignes[2 * k + 1].strip("\n")] = lignes[2 * k].strip("\n")
        dic_code[lignes[2 * k].strip("\n")] = lignes[2 * k + 1].strip("\n")
    fid.close()
    return dic_code, dic_char