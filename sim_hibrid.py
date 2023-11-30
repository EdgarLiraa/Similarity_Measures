from owlready2 import *
from funcoes.funcoes_similarity import depthClass, encontraLCS, distancia_conceitual,profundidadeMax,depthClass
from funcoes.funcoes_ic import *
import math

def sim_hasdj(classe1,classe2,n_conceitos):
    
    term_prof = (2*depthClass(encontraLCS(classe1,classe2)))/(depthClass(classe1)+depthClass(classe2))
    term_hypo = (2*information_content_seco(encontraLCS(classe1,classe2),n_conceitos))/(information_content_seco(classe1,n_conceitos)+information_content_seco(classe2,n_conceitos))
    
    return term_prof*term_hypo

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
    
def sim_zhou(classe1, classe2, profundidade,max_nodes,k = 0.5, ic = ic_temp):

    x = k*(math.log(distancia_conceitual(classe1,classe2)+1)/math.log(2*(profundidade-1)))
    y = (1-k)*((ic(classe1,profundidade,max_nodes)+ic(classe2,profundidade,max_nodes) - 2*ic(encontraLCS(classe1,classe2),profundidade,max_nodes))/2)
    return 1-x-y