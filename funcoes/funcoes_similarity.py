from owlready2 import *

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

# Encontra todos caminhos entre a classe como parametro e a lista de ancestrais da segunda classe
def caminhos_is_a(lista,classeAtual, classesComuns, caminhos):
    
    lista.append(classeAtual)
    if(((classeAtual in classesComuns) == True)):
        caminhos.append(lista)
        
    for classe in classeAtual.is_a:
        caminhos_is_a(lista.copy(), classe, classesComuns, caminhos)

#Encontra o LCS = Ancestral comum mais especifico entre duas classes
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

# Retorna o caminho referente a profundidade de um conceito na ontologia
def depthCaminho(classe1):
    
    Caminhos = []
    caminhos_is_a([], classe1, Thing.ancestors(), Caminhos)
    menorCaminho = min(Caminhos, key=len)
    
    return menorCaminho

# Retorna a profundidade da classe
def depthClass(classe1):

    return len(depthCaminho(classe1))-1

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