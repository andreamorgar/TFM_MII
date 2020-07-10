#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 17:29:00 2020

@author: andrea

Adaptación de recetas vegetariana y vegana
Este fichero preprocesa los ingredientes de la receta, y busca un mapeo a la base de datos.
Se consultan las propiedades de los alimentos para ver si existe una incompatibilidad
con la restricción, y se realiza un nuevo mapeo que permite mapear el ingrediente
a uno de los que sí estén permitidos.
 
"""

from gensim.models import KeyedVectors
from gensim.models.phrases import Phraser
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text
import gensim
import pandas as pd
import numpy as np
from fjaccard import fjaccard_extended

# Cargamos los modelos que necesitamos
CUSTOM_FILTERS = [remove_stopwords, stem_text]
CUSTOM_FILTERS_2 = [remove_stopwords]
modelo_guardado = KeyedVectors.load("../models/v2/modelo3")
bigram_loaded = Phraser.load("../models/v2/my_bigram_model.pkl")
df_idiet = pd.read_excel("../data/i-diet-database.xlsx")


# -----------------------------------------------------------------------------
# preprocesar texto de igual forma que en el modelo de word embedding
def preprocess_recipe(text_recipe, create_tokens = True, main_ingredient = False):
    if main_ingredient:
        pos = text_recipe.find(',')
        if pos != -1:
            text_recipe = text_recipe[0:(pos+1)]
            
    if create_tokens:
        tokens = list(gensim.utils.tokenize(text_recipe, lower=True))
        
    else:
        tokens = text_recipe
        
    tokens = preprocess_string(" ".join(tokens), [remove_stopwords, stem_text]) 
    sentenc = list(bigram_loaded[tokens])
    
    return sentenc
#%%

# -----------------------------------------------------------------------------
# Función para mapear los equivalentes a la base de datos (proporcionada)
def get_DB_equivalent(idiet_item_list, bd_names_ , bd_names_mapping , model, number_instances = False):
    
    # Obtenemos la similitud entre todos los elementos en la base de datos
    vector_similarity = np.zeros(len(bd_names_mapping))
    for i,item in enumerate(bd_names_mapping):
        s = fjaccard_extended(idiet_item_list, item)
        vector_similarity[i] = s

    # identificamos el elemento más similar 
    sorted_list = np.argsort(vector_similarity)


    # podemos devolver el mejor mapeo o los diez mejores, dependiendo de lo que
    # nos interese valorar
    if number_instances == True:
        most_similar = [ bd_names_[sorted_list[i]] for i in range(10) ]
        value_most_similar = [ vector_similarity[sorted_list[i]] for i in range(10) ]
        
        # si el valor de distancia es infinito no hay mapeo posible
        # si la distancia es muy alta, consideramos que tampoco hay mapeo posible
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
    ingredient_processed = preprocess_recipe(i)
     
    mapping_idiet, value_mapping, alternatives_  = get_DB_equivalent(ingredient_processed,bd_names_=db,bd_names_mapping=bd_names_processed,model=model,number_instances=False)
    
    # Si el valor del mapping no sale aceptable buscamos la otra opcion (para intentar evitar problemas de la traducción)
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
    bd_names_processed = [preprocess_recipe(x) for x in db]
    bd_names_processed_translate_andrea = [preprocess_recipe(x) for x in db_translated] 
    
    
    list_recipe_ingredients = []

    # obtenemos los ingredientes de la receta
    recipe_ingredients = recipe['ingredients']
    
    for i in recipe_ingredients:
        # para cada ingrediente de la receta obtenemos el mapeo óptimo
        mapping, mapping_idiet, value_mapping, others= get_accurate_mapping(i,model,bigram,db,db_translated,nutritional_data,bd_names_processed,bd_names_processed_translate_andrea)

        modified_action = 'no'
        adapted_ing = ""
        
        if mapping_idiet != 'No matches':

            mapping = mapping.iloc[0]
            # en caso de que no cumpla la restriccion, aplicamos otro mapeo al
            # subconjunto de alimentos que si la satisfaga.
            if mapping[restriction] == 0 and value_mapping <0.9:
                
                modified_db = nutritional_data[nutritional_data[restriction] == 1]
                bd_names_mod = list(modified_db['food_name_eng'])
                bd_names_translate_mod = list(modified_db['translate_andrea'])
                bd_names_mod_processed = [preprocess_recipe(x) for x in bd_names_mod]
                bd_names_translate_processed_mod = [preprocess_recipe(x) for x in bd_names_translate_mod] 
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
    

# ejemplo
spanish_ingredients = pd.read_excel('../data/recipes/bd-producto-app.xlsx') 
bd_names = list(spanish_ingredients['food_name_eng'])
bd_names_translate_andrea = list(spanish_ingredients['translate_andrea'])

rp = {'name':'receta','ingredients':['butter','lemon, juice of', 'white pepper','egg yolks']}
x = get_adapted_recipe(recipe=rp,model=modelo_guardado,bigram=bigram_loaded,db=bd_names,db_translated=bd_names_translate_andrea, nutritional_data=spanish_ingredients,restriction='vegan')