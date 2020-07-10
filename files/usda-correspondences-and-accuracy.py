#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 11:50:20 2020

@author: andrea
"""

from nltk.util import ngrams
from gensim.models.phrases import Phrases, Phraser

from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text
import gensim
import pandas as pd
from gensim.models import KeyedVectors
import numpy as np
import os
import distance
import ast
import matplotlib.pyplot as plt

#from vocabulary_model_info import wmdistance_versionAndrea
from fjaccard import fuzzyjaccard, fjaccard_extended, fuzzyjaccard_euclidean
#%%

# Cargamos los modelos que necesitamos
CUSTOM_FILTERS = [remove_stopwords, stem_text]
CUSTOM_FILTERS_2 = [remove_stopwords]
modelo_guardado = KeyedVectors.load("../models/v2/modelo3")
bigram_loaded = Phraser.load("../models/v2/my_bigram_model.pkl")

#Cargamos las bases de datos utilizadas
df_idiet = pd.read_excel("../data/i-diet-database.xlsx")
df_USDA = pd.read_excel("../data/names_USDA.xlsx")
bd_names = list(df_USDA['Main food description'])



from gensim.models import KeyedVectors
# Cargamos el modelo de Google en caso que queramos utilizarlo
# De momento está comentado para que la ejecución de este fichero sea más ligera
#model = KeyedVectors.load_word2vec_format('/home/andrea/Escritorio/GoogleNews-vectors-negative300.bin', binary=True)
#%%
# preprocesar texto
def preprocess_recipe(text_recipe, create_tokens = True):

            
    if create_tokens:
        tokens = list(gensim.utils.tokenize(text_recipe, lower=True))
        
    else:
        tokens = text_recipe
        
    tokens = preprocess_string(" ".join(tokens), CUSTOM_FILTERS) 
    sentenc = list(bigram_loaded[tokens])
    
    return sentenc


#%%
bd_names_processed = [preprocess_recipe(x) for x in bd_names]
idiet_names = list(df_idiet['NOMBRE_ING'])
df_idiet['NOMBRE_ING_PROCESSED'] = df_idiet['NOMBRE_ING'].apply(preprocess_recipe,create_tokens = True)
#%%
def get_DB_equivalent(idiet_item_list, mode = "word-embedding", number_instances = False):
    print(idiet_item_list)
    print(mode)
    vector_similarity = np.zeros(len(bd_names_processed))

    for i,item in enumerate(bd_names_processed):
        if mode == 'word-embedding':
            s = modelo_guardado.wv.wmdistance(idiet_item_list,item)
        if mode == 'word-embedding-andrea':
            s = wmdistance_versionAndrea(idiet_item_list,item)
        elif mode == 'word-embedding-google':
            s = model.wv.wmdistance(idiet_item_list.split(' '),bd_names[i].split(' '))
        elif mode == 'jaccard':
            s = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
        elif mode == "fjaccard":
            s = fuzzyjaccard(idiet_item_list, item)
        elif mode == "fjaccard_extended":
            s = fjaccard_extended(idiet_item_list, item)
        elif mode == "fjaccard_euclidean":
            s = fuzzyjaccard_euclidean(idiet_item_list, item)
        elif mode == 'levenshtein':
            s = distance.levenshtein(' '.join(idiet_item_list), ' '.join(item))
        elif mode == 'medida-nueva':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.45*(s1*100)+0.55*s2
        elif mode == 'medida-nueva2':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.50*(s1*100)+0.50*s2
        elif mode == 'medida-nueva3':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.55*(s1*100)+0.45*s2
        elif mode == 'medida-nueva4':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.40*(s1*100)+0.60*s2
        elif mode == 'medida-nueva5':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.35*(s1*100)+0.65*s2
        elif mode == 'medida-nueva6':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.60*(s1*100)+0.40*s2
        elif mode == 'medida-nueva7':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.30*(s1*100)+0.70*s2 
        elif mode == 'medida-nueva8':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.25*(s1*100)+0.75*s2   
        elif mode == 'medida-nueva9':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.20*(s1*100)+0.80*s2 
        elif mode == 'medida-nueva10':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.15*(s1*100)+0.85*s2  
        elif mode == 'fuzzy-mix':
            s1 = fuzzyjaccard(idiet_item_list, item)
            s2 = fjaccard_extended(idiet_item_list, item)
            s = 0.20*(s1*100)+0.80*s2 
            
        vector_similarity[i] = s


    # Primero voy a ordenar y luego a normalizar, porque así pierdo el menor número
    # posible de info (puede que dos valores distintos se reduzcan al mismo valor dentro
    # del intervalo [0.1], así podemos evitarlo.)
    
    # ordenar índices de menor a mayor
    sorted_list = np.argsort(vector_similarity)
    
    # normalizar 
    
    if number_instances == True:
        most_similar = [ bd_names[sorted_list[i]] for i in range(10) ]
        value_most_similar = [ vector_similarity[sorted_list[i]] for i in range(10) ]
        
        for i,value in enumerate(value_most_similar):
            if value == np.Infinity:
                most_similar[i] = 'No matches'
            if value > 44.0:
                most_similar[i]  = 'No matches'
    else:
        most_similar = bd_names[sorted_list[0]]
        value_most_similar = vector_similarity[sorted_list[0]]    
        if value_most_similar == np.Infinity:
            most_similar = 'No matches'

    print(most_similar)
            
    return most_similar

#%%
def get_DB_equivalent_value_similarity(idiet_item_list, mode = 'word-embedding', number_instances = False):
    print(idiet_item_list)
    print(mode)
    vector_similarity = np.zeros(len(bd_names_processed))

    #calculamos los mapeos con la opción escogida
    for i,item in enumerate(bd_names_processed):
        
        if mode == 'word-embedding':
            s = modelo_guardado.wv.wmdistance(idiet_item_list,item)
        elif mode == 'word-embedding-google':
            s = model.wv.wmdistance(idiet_item_list.split(' '),bd_names[i].split(' '))
        elif mode == 'jaccard':
            s = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
        elif mode == "fjaccard":
            s = fuzzyjaccard(idiet_item_list, item)
        elif mode == "fjaccard_extended":
            s = fjaccard_extended(idiet_item_list, item)
        elif mode == "fjaccard_euclidean":
            s = fuzzyjaccard_euclidean(idiet_item_list, item)
        elif mode == 'levenshtein':
            s = distance.levenshtein(' '.join(idiet_item_list), ' '.join(item))
        elif mode == 'medida-nueva':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.45*(s1*100)+0.55*s2
        elif mode == 'medida-nueva2':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.50*(s1*100)+0.50*s2
        elif mode == 'medida-nueva3':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.55*(s1*100)+0.45*s2
        elif mode == 'medida-nueva4':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.40*(s1*100)+0.60*s2
        elif mode == 'medida-nueva5':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.35*(s1*100)+0.65*s2
        elif mode == 'medida-nueva6':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.60*(s1*100)+0.40*s2
        elif mode == 'medida-nueva7':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.30*(s1*100)+0.70*s2 
        elif mode == 'medida-nueva8':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.25*(s1*100)+0.75*s2   
        elif mode == 'medida-nueva9':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.20*(s1*100)+0.80*s2  
        elif mode == 'medida-nueva10':
            s1 = distance.jaccard(' '.join(idiet_item_list), ' '.join(item))
            s2 = modelo_guardado.wv.wmdistance(idiet_item_list,item)
            s = 0.15*(s1*100)+0.85*s2 
        elif mode == 'fuzzy-mix':
            s1 = fuzzyjaccard(idiet_item_list, item)
            s2 = fjaccard_extended(idiet_item_list, item)
            s = 0.20*(s1*100)+0.80*s2 
        vector_similarity[i] = s
        
    #ordenamos lista de mayor a menor similitud
    sorted_list = np.argsort(vector_similarity)
    
    # devolvemos los x mejores mapeos posibles
    if number_instances:
        most_similar = [ vector_similarity[sorted_list[i]] for i in range(10) ]
    else:
        most_similar = vector_similarity[sorted_list[0]] 
        

    return most_similar

#%%

# Función para evaluar resultados cuando permitimos devolver hasta los 10
# mejores resultados
def evaluate_multiple(item,number_values=1,testing='USDA_equivalent'):   
    r = False
    for i in range (number_values):
        if ast.literal_eval(item[testing])[i] in item['results']:
            r = True    
    return  r

#%%
#Ejemplo de uso: obtenemos correspondencias con la medida final escogida
#df_idiet['USDA_equivalent'] = df_idiet['NOMBRE_ING_PROCESSED'].apply(get_DB_equivalent,number_instances=True)
##Obtenemos valores de esas correspondencias
#df_idiet['USDA_equivalent_value'] = df_idiet['NOMBRE_ING_PROCESSED'].apply(get_DB_equivalent_value_similarity,number_instances=True)
## Guardamos
#df_idiet.to_excel("../excels/idiet-mapping/resultados-traduccion-ampliado.xlsx", index=False)
#%%

# Funciones para pintar resultados en gráficas


def get_usda_accuracy(filename_USDA='USDA-labeled.xlsx',filename_we_results='resultados-traduccion-ampliado.xlsx'):
    
    df_results = pd.read_excel("../data/"+filename_USDA)
    # Accuracy de la versión 2 de la italiana, que sí devuelve los 10 primeros mejores resultados
    df_correspondences_obtained = pd.read_excel("../excels/idiet-mapping/"+filename_we_results)
    df_correspondences_obtained['results'] = df_results['results']
    
    
    percent_results = []
    # obtenemos el porcentaje de acierto con los distintos niveles de flexibilidad proporcionados
    for i in range(10):
    
        name = 'evaluation_level'+str(i+1)
        df_correspondences_obtained[name] = df_correspondences_obtained.apply(evaluate_multiple,number_values=i+1,testing='USDA_equivalent',axis=1) 
        #obtenemos el número de aciertos
        aciertos = df_correspondences_obtained[df_correspondences_obtained[name] == True]
     
        #calculamos porcentaje
        print( "Teniendo en cuenta "+str(i+1) + "--> " + str((aciertos.shape[0]/df_correspondences_obtained.shape[0])*100))
        percent_results.append((aciertos.shape[0]/df_correspondences_obtained.shape[0])*100)
    
    #guardar resultados
    df_correspondences_obtained.to_excel("../excels/accuracy/"+filename_we_results)
    return percent_results


# -----------------------------------------------------------------------------
    
def plot_accuracy(vector_results,title="Resultados validación (BD USDA)",filename_fig="figura-USDA.png")  :
    plt.style.use('ggplot')
    x = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, vector_results, color='green')
    plt.xlabel("Número de resultados considerados")
    plt.ylabel("Aciertos (%)")
    plt.title(title)
    plt.xticks(x_pos, x)
    plt.savefig(filename_fig)


# -----------------------------------------------------------------------------
def plot_results(titulo, nombres_ficheros, labels):
    x = np.array([0,1,2,3,4,5,6,7,8,9])

    #https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
    with plt.style.context('default'): 
    
        # Tenemos que obtener los valores de precisión de cada uno de los
        # ficheros proporcionados
        for i,nombre in enumerate(nombres_ficheros):
            plt.plot(get_usda_accuracy(filename_we_results=nombre),label=labels[i])

        plt.title(titulo)
        plt.xticks(x, [x for x in range(1,11)])
        
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.legend.html
        plt.legend(loc='best')
        plt.grid(alpha=0.3)
        plt.xlabel('Primeros x resultados', fontsize=14)
        plt.ylabel('Acierto en los mapeos (%)', fontsize=14)
        plt.show()



#%%

# Función que se encarga de realizar el mapping con una medida dada
def mapping(distance_metric,idiet_mapping_filename):
    #obtenemos mapping
    df_idiet['USDA_equivalent'] = df_idiet['NOMBRE_ING_PROCESSED'].apply(get_DB_equivalent,mode=distance_metric,number_instances=True)
    # obtenemos valores asociados al mapping
    df_idiet['USDA_equivalent_value'] = df_idiet['NOMBRE_ING_PROCESSED'].apply(get_DB_equivalent_value_similarity,mode=distance_metric,number_instances=True)
    # guardamos los resultados
    df_idiet.to_excel("../excels/idiet-mapping/resultados-traduccion-ampliado-"+idiet_mapping_filename, index=False)
    # calculamos los porcentajes de acierto y finalmente los presentamos en forma de gráfica
    plot_accuracy(get_usda_accuracy(filename_we_results='resultados-traduccion-ampliado-'+idiet_mapping_filename))
    
#mapping('jaccard','prueba.xlsx')
#%%

# Automatizamos la ejecución de todos los ficheros

medidas = ['jaccard','levenshtein','medida-nueva','medida-nueva2',
           'medida-nueva3','medida-nueva4','medida-nueva5','medida-nueva6',
           'medida-nueva7','medida-nueva8','medida-nueva9','medida-nueva10',
           'medida-nueva11','medida-nueva12','word-embedding-google','fuzzy-mix',
           "fjaccard","fjaccard_extended","fjaccard_euclidean"]

ficheros = ["jaccard.xlsx","levenshtein.xlsx","medida-nueva.xlsx","medida-nueva2.xlsx",
            "medida-nueva3.xlsx","medida-nueva4.xlsx","medida-nueva5.xlsx","medida-nueva6.xlsx","medida-nueva7.xlsx",
            "medida-nueva8.xlsx","medida-nueva9.xlsx","medida-nueva10.xlsx","medida-nueva11.xlsx", "medida-nueva12.xlsx",
            'we-google-sin-stem.xlsx','fjaccard.xlsx','fjaccard_extended.xlsx','fjaccard_euclidean.xlsx','fuzzy_mix.xlsx']


for i,medida in enumerate(medidas):
    print(medida)
    print(ficheros[i])
    mapping(medida,ficheros[i])



#%%
# -----------------------------------------------------------------------------

# Para obtener la gráfica de la precisión de alguno de los resultados
plot_accuracy(get_usda_accuracy(filename_we_results="resultados-traduccion-ampliado-fjaccard_extended.xlsx"))
plot_accuracy(get_usda_accuracy(filename_we_results='resultados-traduccion-ampliado-we-google-2.xlsx'))


# Para representar los resutlados en una gráfica 
resultados_mapeos = ['resultados-traduccion-ampliado-we-google-sin-stem.xlsx', 'resultados-traduccion-ampliado-fjaccard_extended.xlsx']
etiquetas = ["w.e. Google","w.e. recetas"]

plot_results('Comparación entre modelos de Word Embedding',resultados_mapeos,etiquetas)