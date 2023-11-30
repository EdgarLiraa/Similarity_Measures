from owlready2 import *
from funcoes.funcoes_similarity import *
import math

def sim_path(classe1, classe2):
        
    distancia = distancia_conceitual(classe1,classe2)
    
    if (distancia == 0):
        return 1/1
    return 1/distancia

def sim_wup(classe1, classe2):

    if(classe1 == classe2):
        return 1/1
    
    #Distancia conceitual entre a Thing e uma classe é a profundidade
    depth_C1 = depthClass(classe1)
    depth_C2 = depthClass(classe2)
    depth_LCS = depthClassMax(encontraLCS(classe1, classe2))
    
    if(depth_C1 == 0):
        depth_C1=1
    if(depth_C2 == 0):
        depth_C2=1    
    if(depth_LCS == 0):
        depth_LCS=1   

    return (2*depth_LCS)/(depth_C1+depth_C2)

def sim_leacock(classe1, classe2, profundidade):
    
    dist = distancia_conceitual(classe1,classe2)
    if dist == 0:
        return 1/1
    return -(math.log10(dist/(2*profundidade)))

def sim_li( classe1, classe2, alpha = 0.2, beta = 0.6):

    e = math.e
    dist_conceitual = distancia_conceitual(classe1,classe2)
    depth_LCS = depthClassMax(encontraLCS(classe1, classe2))

    conta = e**(-alpha*dist_conceitual)*((e**(beta*depth_LCS)-e**(-beta*depth_LCS))/(e**(beta*depth_LCS)+e**(-beta*depth_LCS)))
    
    return conta

def sim_nguyan(classe1,classe2,profundidade):
    dist = distancia_conceitual(classe1,classe2)
    if dist == 0:
        return 1
    return math.log2(2+((distancia_conceitual(classe1,classe2)-1)*(-depthClassMax(encontraLCS(classe1, classe2))+profundidade))) 

def sim_batet(classe1,classe2):

    if classe1 == classe2:
        return 1
    
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