from funcoes.funcoes_ic import *
from funcoes.funcoes_similarity import encontraLCS
import math

def sim_resnik(classe1, classe2,arg_ic, ic_measure = information_content_seco):
    
    if classe1 == classe2:
        return 1
    
    return ic_measure(encontraLCS(classe1,classe2),arg_ic)
    
def sim_jiang(classe1, classe2,arg_ic, ic_measure = information_content_seco):
    
    if classe1 == classe2:
        return 1
    
    return ic_measure(classe1,arg_ic)+ic_measure(classe2,arg_ic)-2*ic_measure(encontraLCS(classe1,classe2),arg_ic)

def sim_lin(classe1, classe2,arg_ic, ic_measure = information_content_seco):
    
    if classe1 == classe2:
        return 1
    
    return 2*(ic_measure(encontraLCS(classe1,classe2),arg_ic))/(ic_measure(classe1,arg_ic)+ic_measure(classe2,arg_ic))

def sim_jaccard(classe1,classe2,arg_ic, ic_measure = information_content_seco):
    if classe1 == classe2:
        return 1
    
    x = ic_measure(encontraLCS(classe1,classe2),arg_ic)
    y = ic_measure(classe1,arg_ic)+ ic_measure(classe2,arg_ic) - ic_measure(encontraLCS(classe1,classe2),arg_ic)

    return x/y

def sim_meng(classe1,classe2,arg_ic, ic_measure = information_content_seco):
    return math.e**(sim_lin(classe1,classe2,arg_ic,ic_measure))-1