from owlready2 import *
from funcoes_aux import *
import math

def information_content_sanchez(classeX, n_folhas = 905):

    subsumers = len(classeX.ancestors())
    folhas = num_folhas_classe(classeX)
    x = (folhas/subsumers) + 1
    y = n_folhas + 1

    return -math.log10(x/y)

def information_content_seco(classeX, n_conceitos = 990):

    hiponimos = len(classeX.descendants())
    log_hiponimos = math.log10(hiponimos)
    log_conceitos = math.log10(n_conceitos)

    return (1-(log_hiponimos/log_conceitos))