from owlready2 import *
import pandas as pd
from datetime import datetime
from threading import *
import math

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
#Encontra os caminhos de uma classe a outra
def caminhos_No_Grafo(lista ,classeAtual, classe2, caminhos, invertido):

    lista.append(classeAtual)
    if(classeAtual == classe2):
        if invertido == (True):
            caminhos.append(lista[::-1])
        else: 
            caminhos.append(lista)

    for classe in classeAtual.is_a:
        caminhos_No_Grafo(lista.copy(), classe, classe2, caminhos, invertido)

#Retorna o menor caminho entre as classe1 e classe2
def caminho_Mais_Curto(classe1, classe2):

    caminhos1 = []
    caminhos2 = []
    ancestrais1 = classe1.ancestors()
    ancestrais2 = classe2.ancestors()
    termosComuns = list((classe1.descendants() | ancestrais1) & (classe2.descendants() | ancestrais2))

    for classe in termosComuns:
        if classe in ancestrais1:
            caminhos_No_Grafo([],classe1, classe, caminhos1, False)
        else:
            caminhos_No_Grafo([],classe, classe1, caminhos1, True)
        if classe in ancestrais2:
            caminhos_No_Grafo([],classe2, classe, caminhos2, False)
        else:
            caminhos_No_Grafo([],classe, classe2, caminhos2, True)
    
    listaFinal = []

    for y in caminhos2:
        for x in caminhos1:
            if x[-1] == y[-1]:
                listaFinal.append(x+y)
    
    menorCaminho = min(listaFinal, key=len)
    
    return menorCaminho

#Calcula a Distancia Conceitual entre as Classes 1 e 2
def distancia_conceitual(classe1,classe2):
    return len(caminho_Mais_Curto(classe1, classe2))-2

#Calcula SimPath

#Encontra todos caminhos entre a classe como parametro e a lista de ancestrais da segunda classe
def caminhos_is_a(lista,classeAtual, classesComuns, caminhos):
    
    lista.append(classeAtual)
    if(((classeAtual in classesComuns) == True)):
        caminhos.append(lista)
        
    for classe in classeAtual.is_a:
        caminhos_is_a(lista.copy(), classe, classesComuns, caminhos)



#Encontra o LCS = Ancestral comum mais especifico entre duas classes
#def encontraLCS(classe1, classe2):
#
#    intersec = list(classe1.ancestors() & classe2.ancestors())
#    
#    caminhos1 = []
#    caminhos2 = []
#
#    caminhos_is_a([], classe1, intersec, caminhos1)
#    caminhos_is_a([], classe2, intersec, caminhos2)
#
#    listaFinal = []
#    
#    for y in caminhos2:
#        for x in caminhos1:
#            if x[-1] == y[-1]:
#                listaFinal.append(x+y)
#    
#    menorCaminho = min(listaFinal, key=len)
#    
#    
#    lcs = menorCaminho[-1]
#    return lcs

def encontraLCS(classe1, classe2):

    intersec = list(classe1.ancestors() & classe2.ancestors())
    
    caminhos1 = []
    caminhos2 = []

    caminhos_is_a([], classe1, intersec, caminhos1)
    caminhos_is_a([], classe2, intersec, caminhos2)

    listaFinal = []

    for y in caminhos2:
        for x in caminhos1:
            if x[-1] == y[-1]:
                listaFinal.append(x+y)
    
    
    dist_menorCaminho = len(min(listaFinal, key=len))
    
    candidatos = []
    for x in listaFinal:
        if len(x) == dist_menorCaminho:
            candidatos.append(x[-1])
    
    profundidade = -1

    for x in candidatos:
        depthTemp = depthClassMax(x)
        if depthTemp > profundidade:
            profundidade = depthTemp
            lcs = x

    return lcs


def depthCaminhoMAX(classe1):
    
    Caminhos = []
    caminhos_is_a([], classe1, Thing.ancestors(), Caminhos)
    maiorCaminho = max(Caminhos, key=len)
    
    return maiorCaminho
 
def depthClassMax(classe1):
    if classe1.name == "Thing":
        return 1
    return len(depthCaminhoMAX(classe1))-1


def depthCaminho(classe1):
    
    Caminhos = []
    caminhos_is_a([], classe1, Thing.ancestors(), Caminhos)
    menorCaminho = min(Caminhos, key=len)
    
    return menorCaminho

def depthClass(classe1):

    return len(depthCaminho(classe1))-1

# Medida de Similaridade de Rada
def sim_path(classe1, classe2):
        
    distancia = distancia_conceitual(classe1,classe2)
    
    if (distancia == 0):
        return 1/1
    return 1/distancia

#Medida de similaridade Wu and Palmer
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

############################## Leacock #############################################

#def sim_leacock(classe1, classe2, onto):
#    return -math.log10(distancia_conceitual(classe1,classe2)/profundidadeMax(onto))

def sim_leacock(classe1, classe2, profundidade):
    
    dist = distancia_conceitual(classe1,classe2)
    if dist == 0:
        return 1/1
    return -(math.log10(dist/(2*profundidade)))

############################## Li ##################################################
def sim_li( classe1, classe2, alpha = 0.2, beta = 0.6):

    e = math.e
    dist_conceitual = distancia_conceitual(classe1,classe2)
    depth_LCS = depthClassMax(encontraLCS(classe1, classe2))

    conta = e**(-alpha*dist_conceitual)*((e**(beta*depth_LCS)-e**(-beta*depth_LCS))/(e**(beta*depth_LCS)+e**(-beta*depth_LCS)))
    
    return conta

############################## Nguyan ##############################################
#def sim_nguyan(classe1,classe2,onto):
#    return math.log2(2+((distancia_conceitual(classe1,classe2)-1)*(-depthClassMax(encontraLCS(classe1, classe2))+profundidadeMax(onto)))) 
def sim_nguyan(classe1,classe2,profundidade):
    dist = distancia_conceitual(classe1,classe2)
    if dist == 0:
        return 1
    return math.log2(2+((distancia_conceitual(classe1,classe2)-1)*(-depthClassMax(encontraLCS(classe1, classe2))+profundidade))) 

############################## Batet ###############################################

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

############################## AUXILIARES ##########################################

#Mostra o caminhos entre as classes
def mostraCaminho(classe1, classe2):
    lista = caminho_Mais_Curto(classe1, classe2)
    
    lcs = lista[-1]
    lista.pop(-1)
    for x in range(0, len(lista)):
        if lista[x] == lcs:
            lista[x+1:] = reversed(lista[x+1:])
            break
    return lista 

#Procura as classes na Ontologia
def Search_Classes(onto, classe1, classe2):
    
    if classe1 == "Thing":
        classe1 = Thing
    if classe2 == "Thing":
        classe2 = Thing
    
    for classe in onto.classes():
        if (classe.name == classe1): 
            classe1 = classe
        if (classe.name == classe2):
            classe2 = classe

    return classe1, classe2

def Show_Classes(onto):
    for classe in onto.classes():
        print(classe.name, end = " | ")

#Salva a Matriz de similaridade da ontologia (Demorado)
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
    
    matriz_SimPath.to_csv("SPath.csv")
    matriz_WuP.to_csv("WuP.csv")
    matriz_Batet.to_csv("Batet.csv")
    matriz_Li.to_csv("Li.csv")
    matriz_Leacock.to_csv("Leacock.csv")
    matriz_Nguyan.to_csv("Nguyan.csv")

if __name__ == "__main__":

    onto = get_ontology("../Ontologias/ontoqsar22v9.owl").load()
    
    listaX = list(onto.classes())
    profundidade = profundidadeMax(onto)
    
    salva_planilha(onto)

    #for classeX in listaX:
    #    for classeY in listaX:
    #        sim_path(classeX,classeY)
    #        sim_wup(classeX,classeY)
    #        sim_li(classeX,classeY)
    #        sim_batet(classeX,classeY)
    #        sim_leacock(classeX,classeY, profundidade)
    #        sim_nguyan(classeX,classeY, profundidade)


# WuP
# LCS:
#   Menor caminho entre os ancestrais dos termos 1 e 2
#       Caso hajam mais de dois ancestrais com a mesma menor distancia dos termos 1 e 2:
#           Usar Ancestral com menor profundidade possivel
# 
# Profundidade termos 1 e 2:
# Menor Caminho até Thing
# 
############################################################
# 
# SPath 
# Distancia Conceitual:
#   Is_a - Se tornam caminhos de "ida e volta"