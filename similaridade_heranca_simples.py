from owlready2 import *
import pandas as pd
from datetime import datetime
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

#def sim_nguyan(classe1, classe2,onto):
#
#    #distancia conceitual
#    distancia_conceitual = dist_conceitual(classe1,classe2)
#    if (distancia_conceitual == 0):
#        distancia_conceitual = 1
#    
#    #LCS
#    lcs = encontra_lcs(classe1,classe2)
#    depth_LCS = profundidade_class(lcs)
#    depth_max = profundidadeMax(onto)
#
#    return math.log2(2+((distancia_conceitual-1)*(-depth_LCS+depth_max))) 

def sim_nguyan(classe1, classe2,depth_max):

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

    return - (math.log2(conta))

def sim_li(classe1, classe2, alpha = 0.2, beta = 0.6):
    
    e = math.e
    
    #distancia conceitual
    distancia_conceitual = dist_conceitual(classe1,classe2)
    depth_LCS = profundidade_class(encontra_lcs(classe1,classe2))
 
    conta = e**(-alpha*distancia_conceitual)*((e**(beta*depth_LCS)-e**(-beta*depth_LCS))/(e**(beta*depth_LCS)+e**(-beta*depth_LCS)))
    
    return conta

#############Salva Sequencial#############
def salva_planilha(onto):

    listaX = list(onto.classes()) 

    simpath_values = []
    listaIndex = []
    for elem in listaX:
        listaIndex.append(elem.name)

    matriz_WuP = pd.DataFrame(simpath_values,columns = listaIndex,index = listaIndex)
    matriz_SimPath = pd.DataFrame(simpath_values,columns = listaIndex,index = listaIndex)
    matriz_Batet = pd.DataFrame(simpath_values,columns = listaIndex,index = listaIndex)
    matriz_Li = pd.DataFrame(simpath_values,columns = listaIndex,index = listaIndex)
    matriz_Leacock = pd.DataFrame(simpath_values,columns = listaIndex,index = listaIndex)
    matriz_Nguyan = pd.DataFrame(simpath_values,columns = listaIndex,index = listaIndex)
    profundidade = profundidadeMax(onto)

    time0 = time.time()
    for classeX in listaX:
        for classeY in listaX:
            matriz_SimPath.loc[classeX.name, classeY.name] = round(sim_path(classeX, classeY), 4)
    time1 = time.time()
    print("Duração SimPath = ", time1 - time0)

    for classeX in listaX:
        for classeY in listaX:        
            matriz_WuP.loc[classeX.name, classeY.name] = round(sim_wup(classeX, classeY), 4)
    
    time2 = time.time()
    print("Duração Sim_WuP = ", time2 - time1)

    for classeX in listaX:
        for classeY in listaX:        
            matriz_Li.loc[classeX.name, classeY.name] = round(sim_li(classeX, classeY), 4)
    
    time3 = time.time()
    print("Duração Sim_Li = ", time3 - time2)
    
    for classeX in listaX:
        for classeY in listaX:        
            matriz_Batet.loc[classeX.name, classeY.name] = round(sim_batet(classeX, classeY), 4)
    
    time4 = time.time()
    print("Duração Sim_Batet = ", time4 - time3)

    for classeX in listaX:
        for classeY in listaX:        
            matriz_Leacock.loc[classeX.name, classeY.name] = round(sim_leacock(classeX, classeY, profundidade), 4)
    
    time5 = time.time()
    print("Duração Sim_Leacock = ", time5 - time4)
    
    for classeX in listaX:
        for classeY in listaX:        
            matriz_Nguyan.loc[classeX.name, classeY.name] = round(sim_nguyan(classeX, classeY, profundidade), 4)
    
    time6 = time.time()
    print("Duração Sim_Nguyan = ", time6 - time5)

    matriz_SimPath.to_csv("simples_SPath.csv")
    matriz_WuP.to_csv("simples_WuP.csv")
    matriz_Batet.to_csv("simples_Batet.csv")
    matriz_Li.to_csv("simples_Li.csv")
    matriz_Leacock.to_csv("simples_Leacock.csv")
    matriz_Nguyan.to_csv("simples_Nguyan.csv")
 
if __name__ == "__main__":
    onto = get_ontology("../Ontologias/ontoqsar22v9.owl").load()
    
    salva_planilha(onto)
