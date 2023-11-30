from owlready2 import *
from funcoes.funcoes_aux import numeroDeConceitos, num_folhas_classe
from funcoes.funcoes_similarity import profundidadeMax
from funcoes.funcoes_relatedness import faz_dicionario_is_a, faz_dicionario_obj_prop, dict_union
from sim_caminhos import *
from sim_info_content import *
from sim_hibrid import *
from relatedness_measures import *
import pandas as pd

class SimilarityOnto:

    def __init__(self, caminho:str) -> None:
        self.onto = get_ontology(caminho).load()

        self.n_conceitos = numeroDeConceitos(self.onto)
        self.n_folhas = num_folhas_classe(Thing)
        self.profundidade = profundidadeMax(self.onto)

    def cria_df(self):
        values = []
        listaIndex = []
        listaX = list(self.onto.classes()) 

        for elem in listaX:
            listaIndex.append(elem.name)
        
        return pd.DataFrame(values,columns = listaIndex,index = listaIndex)

    # Medidas de caminho 
    def sim_path_df(self):
        
        df = self.cria_df()
        listaX = list(self.onto.classes()) 

        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_path(classeX, classeY), 4)
    
        return df
    
    def sim_wup_df(self):

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:        
                df.loc[classeX.name, classeY.name] = round(sim_wup(classeX, classeY), 4)
    
        return df

    def sim_li_df(self):

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:        
                df.loc[classeX.name, classeY.name] = round(sim_li(classeX, classeY), 4)

        return df

    def sim_nguyan_df(self):

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:        
                df.loc[classeX.name, classeY.name] = round(sim_nguyan(classeX, classeY, self.profundidade), 4)
    
        return df

    def sim_leacock_df(self):

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:        
                df.loc[classeX.name, classeY.name] = round(sim_leacock(classeX, classeY, self.profundidade), 4)

        return df

    def sim_batet_df(self):

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
    
        for classeX in listaX:
            for classeY in listaX:        
                df.loc[classeX.name, classeY.name] = round(sim_batet(classeX, classeY), 4)
    
        return df

    # Medidas de Information Content
    def sim_meng_df(self,ic:str):
        arg = None

        if ic == "sanchez":
            ic = information_content_sanchez
            arg = self.n_folhas
        else:
            ic = information_content_seco
            arg = self.n_conceitos

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_meng(classeX, classeY,arg,ic), 4)
    
        return df
    def sim_lin_df(self,ic:str):
        arg = None

        if ic == "sanchez":
            ic = information_content_sanchez
            arg = self.n_folhas
        else:
            ic = information_content_seco
            arg = self.n_conceitos

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_lin(classeX, classeY,arg,ic), 4)
    
        return df
    def sim_jaccard_df(self,ic:str):

        arg = None

        if ic == "sanchez":
            ic = information_content_sanchez
            arg = self.n_folhas
        else:
            ic = information_content_seco
            arg = self.n_conceitos

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_jaccard(classeX, classeY,arg,ic), 4)
    
        return df
    def sim_jiang_df(self, ic:str):
        arg = None

        if ic == "sanchez":
            ic = information_content_sanchez
            arg = self.n_folhas
        else:
            ic = information_content_seco
            arg = self.n_conceitos

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_jiang(classeX, classeY,arg,ic), 4)
    
        return df
    
    def sim_resnik_df(self,ic:str):
        
        arg = None

        if ic == "sanchez":
            ic = information_content_sanchez
            arg = self.n_folhas
        else:
            ic = information_content_seco
            arg = self.n_conceitos

        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_resnik(classeX, classeY,arg,ic), 4)
    
        return df

    # Medidas Hibridas
    def sim_zhou_df(self):
        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_zhou(classeX, classeY,self.profundidade,self.n_conceitos), 4)
     
        return df
    
    def sim_hasdj_df(self):
        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(sim_hasdj(classeX, classeY,self.n_conceitos), 4)
    
        return df    

    # Medidas de Relacionalidade
    def rel_zhang_df(self):
        df = self.cria_df()
        listaX = list(self.onto.classes())
        dict_is_a = faz_dicionario_is_a(self.onto)
        dict_obj = faz_dicionario_obj_prop(self.onto)
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(rel_zhang(classeX, classeY,dict_obj,dict_is_a), 4)
    
        return df    
 
    def rel_mazuel_df(self):
        df = self.cria_df()
        listaX = list(self.onto.classes()) 
        dict_is_a = faz_dicionario_is_a(self.onto)
        dict_obj = faz_dicionario_obj_prop(self.onto)
        dict_un = dict_union(dict_obj,dict_is_a,self.onto)
        for classeX in listaX:
            for classeY in listaX:
                df.loc[classeX.name, classeY.name] = round(rel_mazuel(classeX, classeY,dict_is_a,dict_un), 4)
    
        return df    

