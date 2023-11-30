from owlready2 import *
import math

def dist_conceitual(classe1, classe2):
    distancia_conceitual = 0
    termosComuns = list(classe1.ancestors() & classe2.ancestors())
    
    while (not(classe1 in termosComuns)):
        classe1 = classe1.is_a[0]
        distancia_conceitual = distancia_conceitual + 1
    while (not(classe2 in termosComuns)):
        classe2 = classe2.is_a[0]
        distancia_conceitual = distancia_conceitual + 1

    return distancia_conceitual

def encontra_lcs(classe1,classe2):
    
    listaConceito1 = classe1.ancestors()
    listaConceito2 = classe2.ancestors()
    
    termosComuns = list(listaConceito1 & listaConceito2)

    while (not(classe1 in termosComuns)):
        classe1 = classe1.is_a[0]
    
    return classe1

def profundidade_class(classe1):
    if classe1.name == "Thing":
        return 1
    return len(classe1.ancestors())-1

def profundidadeMax(onto):
    
    depth_max = 0
    for classe in onto.classes():
        classe_temp = classe
        depth_temp = 0
        while (classe_temp.name != "Thing"):
            classe_temp = classe_temp.is_a[0]
            depth_temp = depth_temp + 1
        if depth_temp > depth_max:
            depth_max = depth_temp  

    return depth_max

def sim_path(classe1, classe2):

    distancia_conceitual = dist_conceitual(classe1,classe2)    
    
    if distancia_conceitual != 0:
        return 1/distancia_conceitual
    else:
        return 1/1

def sim_wup(classe1, classe2):
          
    lcs = encontra_lcs(classe1,classe2)
    death_LCS = profundidade_class(lcs)
    death_C1 = profundidade_class(classe1)
    death_C2 = profundidade_class(classe2)

    return 2*death_LCS/(death_C1+death_C2)

def sim_leacock(classe1, classe2, depth_max):
    
    distancia_conceitual = dist_conceitual(classe1,classe2)
    if distancia_conceitual == 0:
        return 1/1
    return -(math.log10(distancia_conceitual/(2*depth_max))) 

def sim_nguyan(classe1, classe2, depth_max):

    #distancia conceitual
    distancia_conceitual = dist_conceitual(classe1,classe2)
    if (distancia_conceitual == 0):
        return 1
    
    #LCS
    lcs = encontra_lcs(classe1,classe2)
    depth_LCS = profundidade_class(lcs)
    #depth_max = profundidadeMax(onto)

    return math.log2(2+((distancia_conceitual-1)*(-depth_LCS+depth_max))) 

def sim_batet(classe1,classe2):

    listaConceito1 = classe1.ancestors()
    listaConceito2 = classe2.ancestors()
    interserc = list(listaConceito1 & listaConceito2)
    uniao = list(listaConceito1 | listaConceito2)
    tamUniao = len(uniao)
    tamIntersec = len(interserc)
    
    conta = (tamUniao-tamIntersec)/tamUniao
    if conta == 0:
        conta = 1

    return -(math.log2(conta))

def sim_li(classe1, classe2, alpha = 0.2, beta = 0.6):
    
    e = math.e
    
    distancia_conceitual = dist_conceitual(classe1,classe2)
    depth_LCS = profundidade_class(encontra_lcs(classe1,classe2))
 
    conta = e**(-alpha*distancia_conceitual)*((e**(beta*depth_LCS)-e**(-beta*depth_LCS))/(e**(beta*depth_LCS)+e**(-beta*depth_LCS)))

    return conta