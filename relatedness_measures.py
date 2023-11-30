from funcoes.funcoes_relatedness import *

def rel_zhang(classe1, classe2, dict_prop, dict_is_a):
    
    listaX = []
    listaX.append(sim_noun(classe1,classe2,dict_is_a))
    listaX.append(calc_rel_other(classe1,classe2,dict_prop))

    return max(listaX)

def rel_mazuel(classe1, classe2, dict_is_a, dict_union, max_ic = 1):
    if classe1 == classe2:
        return 1
    caminho = menor_caminho(classe1,classe2,dict_union)
    peso = calcula_peso(caminho,dict_is_a)

    return 2*max_ic-peso