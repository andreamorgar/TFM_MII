#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 19:21:53 2020

@author: andrea


Code to fuzzy jaccard distance
"""


from gensim.models.phrases import Phraser
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text
import gensim
import pandas as pd
from gensim.models import KeyedVectors
import numpy as np

import distance

#from sklearn.metrics.pairwise import cosine_similarity
#%%

# Cargamos los modelos que necesitamos
CUSTOM_FILTERS = [remove_stopwords, stem_text]

modelo_guardado = KeyedVectors.load("../models/v2/modelo3")
bigram_loaded = Phraser.load("../models/v2/my_bigram_model.pkl")


#%%

# Función para aplicar el preprocesamiento realizado al modelo de lenguaje 
# a las medidas de distancia
def preprocess_recipe(text_recipe, create_tokens = True, main_ingredient = False):
    if main_ingredient:
        pos = text_recipe.find(',')
        if pos != -1:
            text_recipe = text_recipe[0:(pos+1)]
            
            
    if create_tokens:
        tokens = list(gensim.utils.tokenize(text_recipe, lower=True))
        
    else:
        tokens = text_recipe
        
    tokens = preprocess_string(" ".join(tokens), CUSTOM_FILTERS) 
    sentenc = list(bigram_loaded[tokens])
    
    return sentenc

#%%
    
# Distancia difusa de Jaccard
def fuzzyjaccard(document1,document2):

    num = 0.0
    for i, t1 in enumerate(document1):
        
        for j, t2 in enumerate(document2):

            jaccard_similarity = 1- distance.jaccard(t1, t2)

            #si la similitud entre las dos palabras es >= que 0.8, consideramos
            # que forma parte de la intersección difusa entre ambas descripciones
            if jaccard_similarity >= 0.8:
                num += jaccard_similarity
        
    # obtenemos el valor de la interseccion difusa    
    res = num/(len(document1)+len(document2)-num)

    # devolvemos la distancia para mantener la sincronía con los resultados que teníamos
    return 1 - res


# ejemplos
#x_f = fuzzyjaccard(preprocess_recipe('peanut roast'),preprocess_recipe('peanut honey roasted'))
#y_f = fuzzyjaccard(preprocess_recipe('peanut roast'),preprocess_recipe('peanut unroasted'))


#%%

# Medida difusa entre documentos
import math

# -----------------------------------------------------------------------------
# Función sigmoide
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# -----------------------------------------------------------------------------
  
# Distancia de similitud
# Primero realiza la distancia euclídea entre las representaciones vectoriales 
# de dos palabras. Devuelve la sigmoide de la similitud, para obtener dicho 
# valor en el rango (0,1)
  
# Se utiliza la similitud y no la distancia porque la primera es la utilizada en 
# la función de pertenencia de la medida difusa.
def similarity(word1,word2):
    dist = np.sqrt(np.sum((modelo_guardado.wv[word1] - modelo_guardado.wv[word2])**2))
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
def pertenencia_doc(document,word):
    dists = np.zeros(len(document))
    for idx,d in enumerate(document):
        dists[idx] = similarity(word,d)
    return np.max(dists)


# -----------------------------------------------------------------------------


# Medida difusa entre documentos
def fjaccard_extended(document1, document2):
    
    # omitimos palabras fuera del vocabulario
    document1 = [token for token in document1 if token in list(modelo_guardado.wv.vocab.keys())]
    document2 = [token for token in document2 if token in list(modelo_guardado.wv.vocab.keys())]

    # si una de las descripciones no tiene ninguna palabra dentro del vocabulario
    # del modelo consideramos que la distancia no podemos calcularla y 
    # devolvemos infinito
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
        pertenencia_union += pertenencia_doc(document1,i)*pertenencia_doc(document2,i)
        pertenencia_cj1 += pertenencia_doc(document1,i)
        pertenencia_cj2 += pertenencia_doc(document2,i)
    
    # de esta forma favorecemos la similitud entre los conjuntos en sí que entre
    # las palabras sueltas    
    res = pertenencia_union/(pertenencia_cj1+pertenencia_cj2-pertenencia_union)
    return 1-res
     
#fjaccard_extended(['raw','tomato'],['raw','tomate'])  

#%%


# Otra versión fuzzificada implementada (no nos permitió obtener buenos resultados)
def fuzzyjaccard_euclidean(document1,document2):

    num = 0.0
    
    # omitimos palabras fuera del vocabulario
    document1 = [token for token in document1 if token in list(modelo_guardado.wv.vocab.keys())]
    document2 = [token for token in document2 if token in list(modelo_guardado.wv.vocab.keys())]

    # si una de las descripciones no tiene ninguna palabra dentro del vocabulario
    # del modelo consideramos que la distancia no podemos calcularla y 
    # devolvemos infinito
    
    if len(document1) == 0 or len(document2) == 0:
        return float('inf')

    # En caso de que podamos obtener representación de la desccripción obtenemos
    # la similitud entre cada dos palabras de las descripciones a través de la
    # distancia euclídea entre sus representacones vectoriales
    for i, t1 in enumerate(document1):

        for j, t2 in enumerate(document2):
            sim = similarity(t1,t2)
            fjaccard_extended
            
            # acumulamos los valores de similitudes de aquellos elementos que 
            # sean más similares
            if sim >= 0.8:
                num += sim
        
        
    # finalmente devolvemos la división del total de similitudes de elementos que
    # pertenecen a la unión de las dos descripciones
    res = num/(len(document1)+len(document2)-num)

    # devolvemos la distancia para mantener la sincronía con los resultados
    return 1 - res

# -----------------------------------------------------------------------------
# ejemplo
#fuzzyjaccard_euclidean(['raw','tomato'],['raw','tomate'])    
