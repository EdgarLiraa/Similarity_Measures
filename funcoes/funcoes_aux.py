from owlready2 import *

def numeroDeConceitos(onto):
    cont = 1
    for _ in onto.classes():
        cont+=1
    return cont

def num_folhas_classe(classe):
    folhas = 0

    for item in classe.descendants():
        if len(item.descendants()) == 1:
            folhas+=1

    return folhas