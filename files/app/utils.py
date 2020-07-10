#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:18:34 2020

@author: andrea



utils


"""
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text
import gensim
import numpy as np

import pandas as pd


#%%
# preprocesar texto para ser coherente con el preprocesamiento en el word embedding
def preprocess_recipe(text_recipe, create_tokens = True,bg=None):
        
    if create_tokens:
        tokens = list(gensim.utils.tokenize(text_recipe, lower=True))
        
    else:
        tokens = text_recipe
        
    tokens = preprocess_string(" ".join(tokens), [remove_stopwords, stem_text]) 
    sentenc = list(bg[tokens])
    
    return sentenc

#%%
# para obtener las palabras más similares en el vocabulario a partir de una dada
def get_similar(model,word):
    x = model.most_similar(word, topn=5)
    processed_x = [{'name':i[0],'value':i[1]} for i in x]
    return processed_x


#%%
# fuzzy jaccard extended 
import math

# -----------------------------------------------------------------------------
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# -----------------------------------------------------------------------------
  
# Distancia de similitud
# Primero realiza la distancia euclídea entre las representaciones vectoriales 
# de dos palabras. Devuelve la sigmoide de la similitud, para obtener dicho 
# valor en el rango (0,1)
  
# Se utiliza la similitud y no la distancia porque la primera es la utilizada en 
# la función de pertenencia de la medida difusa. 
def similarity(word1,word2,modelo_guardado):
    dist = np.sqrt(np.sum((modelo_guardado[word1] - modelo_guardado[word2])**2))
    if dist == 0:
        return 1
    elif dist == np.inf:
        return 0
    else:
        return sigmoid(1/dist)

# -----------------------------------------------------------------------------
# para ver si una palabra pertenece o no a una descripción calculamos su similitud
# respecto a todas las palabras en ese documento, y nos quedamos con el valor máximo

# Si la palabra pertenece al documento, tendrá similitud máxima (1) consigo 
# misma, consigo misma, y la función devolverá valor 1
        
def pertenencia_doc(document,word,model):
    dists = np.zeros(len(document))
    for idx,d in enumerate(document):
        dists[idx] = similarity(word,d,model)
    return np.max(dists)
#%%
    
# Medida difusa entre documentos
def fjaccard_extended(document1, document2,model):

    # si una de las descripciones no tiene ninguna palabra dentro del vocabulario
    # del modelo consideramos que la distancia no podemos calcularla y 
    # devolvemos infinito
    document1 = [token for token in document1 if token in list(model.wv.vocab.keys())]
    document2 = [token for token in document2 if token in list(model.wv.vocab.keys())]

    if len(document1) == 0 or len(document2) == 0:

        return float('inf')

    
    # calculamos la intersección difusa entre los documentos, pero teniendo en cuenta
    # esta vez el parecido de esa palabra respecto a los documentos     
    union = set()
    for word1 in document1:
        union.add(word1)
    for word2 in document2:
        union.add(word2)

    pertenencia_union = 0.0
    pertenencia_cj1 = 0.0
    pertenencia_cj2 = 0.0
    
    for i in list(union):
        pertenencia_union += pertenencia_doc(document1,i,model)*pertenencia_doc(document2,i,model)
        pertenencia_cj1 += pertenencia_doc(document1,i,model)
        pertenencia_cj2 += pertenencia_doc(document2,i,model)
    
    # de esta forma favorecemos la similitud entre los conjuntos en sí que entre
    # las palabras sueltas    
    res = pertenencia_union/(pertenencia_cj1+pertenencia_cj2-pertenencia_union)
    return 1-res
     


#fjaccard_extended(['tomate','oil'],['oliv','beef'])  
    
#%%
    

def fuzzyjaccard_euclidean(document1,document2,modelo_guardado):

    num = 0.0
    document1 = [token for token in document1 if token in list(modelo_guardado.wv.vocab.keys())]
    document2 = [token for token in document2 if token in list(modelo_guardado.wv.vocab.keys())]

    if len(document1) == 0 or len(document2) == 0:

        return float('inf')

    for i, t1 in enumerate(document1):

        for j, t2 in enumerate(document2):

            sim = similarity(t1,t2,modelo_guardado)
            
            if sim >= 0.8:
                num += sim
        

    res = num/(len(document1)+len(document2)-num)

    # devolvemos la distancia para mantener la sincronía con los resultados que teníamos
    return 1 - res

#%%    
def get_DB_equivalent(idiet_item_list, bd_names_ , bd_names_mapping , model, number_instances = False):
    
    vector_similarity = np.zeros(len(bd_names_mapping))

    for i,item in enumerate(bd_names_mapping):
        s = fjaccard_extended(idiet_item_list, item,model)
        vector_similarity[i] = s

    sorted_list = np.argsort(vector_similarity)


    if number_instances == True:
        most_similar = [ bd_names_[sorted_list[i]] for i in range(10) ]
        value_most_similar = [ vector_similarity[sorted_list[i]] for i in range(10) ]
        
        for i,value in enumerate(value_most_similar):
            if value == np.Infinity:
                most_similar[i] = 'No matches'
            if value > 44.0:
                most_similar[i]  = 'No matches'
    else:
        most_similar = bd_names_[sorted_list[0]]
        value_most_similar = vector_similarity[sorted_list[0]]    
        if value_most_similar == np.Infinity:
            most_similar = 'No matches'


    alternatives = [ bd_names_[sorted_list[i]] for i in range(10) ]

    return most_similar, value_most_similar, alternatives
    


#%%
def get_accurate_mapping(i,model,bigram,db,db_translated,nutritional_data,bd_names_processed,bd_names_processed_translate_andrea):
    ingredient_processed = preprocess_recipe(i,bg=bigram)
     
    mapping_idiet, value_mapping, alternatives_  = get_DB_equivalent(ingredient_processed,bd_names_=db,bd_names_mapping=bd_names_processed,model=model,number_instances=False)
    
    # Si el valor del mapping no sale aceptable buscamos la otra opcion (la traducida de google)
    if value_mapping > 0.5:

        mapping_idiet_translate2, value_mapping_translate2, alternatives_  = get_DB_equivalent(ingredient_processed,bd_names_=db_translated,bd_names_mapping=bd_names_processed_translate_andrea,model=model,number_instances=False)
        # Si lo mejora... 

        if value_mapping_translate2 < value_mapping:
            mapping_idiet = mapping_idiet_translate2
            
            value_mapping = value_mapping_translate2
            if mapping_idiet != 'No matches':
                mapping = nutritional_data[nutritional_data['translate_andrea'] == mapping_idiet_translate2]

            value_mapping = value_mapping_translate2
        else:
            mapping = nutritional_data[nutritional_data['food_name_eng'] == mapping_idiet]


    else:
        mapping = nutritional_data[nutritional_data['food_name_eng'] == mapping_idiet]

    # devolvemos el alimento de la base de datos cuyo nombre es el que alcanza 
    # mayor similitud con el que pretendemos mapear        
    return mapping, mapping_idiet, value_mapping, alternatives_ 
#%%
def get_adapted_recipe(recipe,model,bigram,db,db_translated,nutritional_data,restriction):
    
    # aplicamos el procesamiento del modelo de word embedding a todos los datos 
    bd_names_processed = [preprocess_recipe(x,bg=bigram) for x in db]
    bd_names_processed_translate_andrea = [preprocess_recipe(x,bg=bigram) for x in db_translated] 
    
    list_recipe_ingredients = []
    

    # obtenemos los ingredientes de la receta
    recipe_ingredients = recipe['ingredients']
    
    for i in recipe_ingredients:
        
        # para cada ingrediente de la receta obtenemos el mapeo óptimo
        mapping, mapping_idiet, value_mapping, others= get_accurate_mapping(i,model,bigram,db,db_translated,nutritional_data,bd_names_processed,bd_names_processed_translate_andrea)

        modified_action = 'no'
        adapted_ing = ""
        
        if mapping_idiet != 'No matches':
            print(mapping_idiet)
            mapping = mapping.iloc[0]
            # en caso de que no cumpla la restriccion, aplicamos otro mapeo al
            # subconjunto de alimentos que si la satisfaga
            if mapping[restriction] == 0 and value_mapping <0.9:
                
                modified_db = nutritional_data[nutritional_data[restriction] == 1]
                bd_names_mod = list(modified_db['food_name_eng'])
                bd_names_translate_mod = list(modified_db['translate_andrea'])
                bd_names_mod_processed = [preprocess_recipe(x,bg=bigram) for x in bd_names_mod]
                bd_names_translate_processed_mod = [preprocess_recipe(x,bg=bigram) for x in bd_names_translate_mod] 
                mapping, adapted_ing, value_mapping, others = get_accurate_mapping(i,model,bigram,bd_names_mod,bd_names_translate_mod,modified_db,bd_names_mod_processed,bd_names_translate_processed_mod)

                modified_action = 'yes'
                
            if value_mapping > 0.9:
                value_mapping = None
        else:

            value_mapping = None


        #devolvemos los ingredientes de la receta con los cambios        
        list_recipe_ingredients.append({'name':i, 'modified':modified_action,'adapted':adapted_ing, 'others':others})
    return list_recipe_ingredients
    


#%%
# Para testear que funciona
    
#from gensim.models import KeyedVectors
#from gensim.models.phrases import Phrases, Phraser
#model = KeyedVectors.load("../../models/v2/modelo3")
#bigram_loaded = Phraser.load("../../models/v2/my_bigram_model.pkl")
#spanish_ingredients = pd.read_excel('../../data/recipes/bd-producto-app.xlsx') 
#bd_names = list(spanish_ingredients['food_name_eng'])
#bd_names_translate_andrea = list(spanish_ingredients['translate_andrea'])
#
#rp = {'name':'receta','ingredients':['butter','lemon, juice of', 'white pepper','egg yolks']}
#x = get_adapted_recipe(recipe=rp,model=model,bigram=bigram_loaded,db=bd_names,db_translated=bd_names_translate_andrea, nutritional_data=spanish_ingredients,restriction='vegan')