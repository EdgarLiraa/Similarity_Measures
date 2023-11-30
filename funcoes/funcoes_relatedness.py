from owlready2 import *
import math
from funcoes_similarity import *
from funcoes_ic import *
from sim_caminhos import *
from sim_info_content import *

def dict_union(dict1, dict2, onto):
    dict_resposta = dict()
    for classe in onto.classes():
        dict_resposta[classe] = set()
    dict_resposta[Thing] = set()
    for chave in dict1:

        dict_resposta[chave].update(dict1[chave])
        dict_resposta[chave].update(dict2[chave])
    
    return dict_resposta

def ic_temp(classe,profundidade = 12, max_node = 955):
    
    inicial = 0
    for x in classe.descendants():
        inicial += depthClass(x)
    if inicial == 0:
        inicial = 1
    
    x = depthClass(classe)
    
    if x == 0:

        x = 1
    
    return (math.log(x)/math.log(profundidade))*(1-(math.log(1/inicial+1)/math.log(max_node)))    
    
def calcula_peso(caminho, dict_is_a):
   
    if len(caminho) == 1:
        return 0
    
    classe_ant = caminho[0]
    classe_inicial = caminho[0]
    tipo = None
    peso = 0
    cont_obj = 0

    for classe in caminho[1:]:
        
        if (classe in dict_is_a[classe_ant]) and tipo == None:
            tipo = "is_a"
 
        elif (classe in dict_is_a[classe_ant]) and tipo == None:
            tipo = "obj_prop"
            cont_obj += 1

        elif (classe in dict_is_a[classe_ant]) and tipo == "is_a":
            pass

        elif (classe not in dict_is_a[classe_ant]) and tipo == "is_a":
            
            tipo = "obj_prop"
            peso += math.fabs(ic_temp(classe_inicial)-ic_temp(classe_ant))
            classe_inicial = classe_ant
            cont_obj += 1

        elif (classe not in dict_is_a[classe_ant]) and tipo == "obj_prop":
            cont_obj += 1

        elif (classe in dict_is_a[classe_ant] and tipo == "obj_prop"):
            peso += 0.5*(cont_obj/(1+cont_obj))
            cont_obj = 0
            classe_inicial = classe_ant

        classe_ant = classe

    if tipo == "is_a":
        peso += math.fabs(ic_temp(classe_inicial)-ic_temp(classe_ant))
    else:
        peso += 1*(cont_obj/(1+cont_obj))

    return peso

def faz_dicionario_obj_prop(onto):
    
    dicionario = dict()
    dicionario[Thing] = set()

    for classe in onto.classes():
        dicionario[classe] = set()
    
    for prop in onto.properties():

        try:

            if (prop.range[0].__class__ == ThingClass) and (prop.domain[0].__class__ == ThingClass):
                for classeDomain in prop.domain:
                    for classeRange in prop.range:
                        dicionario[classeDomain].add(classeRange)
                        dicionario[classeRange].add(classeDomain)
        except:
            continue

    return dicionario

def faz_dicionario_is_a(onto):

    dicionario = dict()
    dicionario[Thing] = set()

    for classe in onto.classes():
        dicionario[classe] = set()
    
    for classe in onto.classes():
        for classePai in classe.is_a:
            dicionario[classe].add(classePai)
            dicionario[classePai].add(classe)

    return dicionario

def caminhos_possiveis(lista:list,classe1:owlready2.owl_class, classe2:owlready2.owl_class,caminhos:list, dicionario:dict(), visitados:list):

    if classe1 in visitados:
        return
    
    lista.append(classe1)
    visitados.append(classe1)
    
    if (classe1 == classe2):
        caminhos.append(lista)
        return
    
    for classe in dicionario[classe1]:
        caminhos_possiveis(lista.copy(), classe, classe2, caminhos, dicionario, visitados.copy())

def menor_caminho(classe1,classe2,dicionario):

    caminhos = []
    caminhos_possiveis([],classe1, classe2,caminhos, dicionario,[])   
    
    if len(caminhos) == 0:
        return None
    
    caminhoMin = min(caminhos, key=len)

    return caminhoMin

def calc_rel_other(conceito1, conceito2, dict, peso = 1):

    if conceito1 == conceito2:
        return 1
    
    distancia = menor_caminho(conceito1,conceito2,dict)
    if distancia == None:
        return 0
    
    return peso/(peso+len(distancia))

def nearest_descendant_common(classe1,classe2,dict_is_a):

    conj = list((classe1.descendants()) & (classe2.descendants()))
    ncd = None

    if len(conj) == 0:
        return ncd

    menor = 9999
    for classe in conj:

        menor_temp1 = len(menor_caminho(classe,classe2,dict_is_a))

        if menor_temp1 < menor:
            ncd = classe
            menor = menor_temp1

        menor_temp2 = len(menor_caminho(classe,classe2,dict_is_a))

        if menor_temp2 < menor:
            ncd = classe
            menor = menor_temp2

    return ncd

def sim_ncd(classe1,classe2,dicionario,peso = 4):

    ncd = nearest_descendant_common(classe1,classe2,dicionario)
    
    if ncd == None:
        return 0
    
    return peso/(peso+len(menor_caminho(classe1,ncd,dicionario))+len(menor_caminho(classe2,ncd,dicionario)))

def sim_noun(conceito1, conceito2, dicionario_is_a):
    
    lista = []
    lista.append(sim_li(conceito1,conceito2))
    lista.append(sim_ncd(conceito1,conceito2, dicionario_is_a))

    return max(lista)