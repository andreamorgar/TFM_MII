#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:45:09 2019

@author: andrea
"""
import numpy
from nltk.util import ngrams
from gensim.models.phrases import Phrases, Phraser
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text
import gensim
import pandas as pd
import itertools
from gensim.models import KeyedVectors
import numpy as np

#%%
# Cargamos los modelos que necesitamos
CUSTOM_FILTERS = [remove_stopwords, stem_text]
modelo_guardado = KeyedVectors.load("../models/v2/modelo3")
bigram_loaded = Phraser.load("../models/v2/my_bigram_model.pkl")

#%%



list_similarity = []

bd_names = ["Egg, whole, raw",
"Egg, whole, cooked, NS as to cooking method",
"Egg, whole, boiled or poached",
"Egg, whole, fried, NS as to fat added in cooking",
"Egg, whole, fried without fat",
"Egg, whole, fried with margarine",
"Egg, whole, fried with oil",
"Egg, whole, fried with butter",
"Sweet potato fries, NFS",
"Sweet potato fries, NS as to fresh or frozen",
"Sweet potato fries, frozen, fried",
"Sweet potato fries, frozen, baked",
"Sweet potato fries, from fresh, fried",
"Sweet potato fries, from fresh, baked",
"Sweet potato fries, fast food / restaurant",
"Sweet potato fries, school",
"Potato tots, from fresh, fried or baked",
"Potato tots, frozen, baked",
"Potato tots, frozen, fried",
"Potato, french fries, NFS",
"Potato, french fries, NS as to fresh or frozen",
"Potato, french fries, from fresh, fried",
"Potato, french fries, from fresh, baked",
"Potato, french fries, from frozen, baked",
"Potato, french fries, fast food",
"Potato, french fries, restaurant",
"Potato, french fries, from frozen, fried",
"Potato, french fries, school",
"Potato, french fries, with cheese, fast food / restaurant",
"Potato, french fries, with cheese, school",
"Potato, french fries, with chili, fast food / restaurant",
"Potato, french fries, with chili and cheese, fast food / restaurant",
"Potato, french fries, with cheese",
"Potato, french fries, with chili and cheese",
"Potato, french fries, with chili",
"Potato, home fries, NFS",
"Potato, home fries, from restaurant / fast food",
"Potato, home fries, from fresh",
"Potato, home fries, ready-to-heat",
"Potato, home fries, with vegetables",
"Potato, hash brown, from fast food",
"Potato chips, fat free",
"Potato chips, restructured, fat free",
"Potato sticks, fry shaped",
"Sweet potato, baked, peel eaten, NS as to fat added in cooking",
"Sweet potato, baked, peel eaten, fat not added in cooking",
"Sweet potato, baked, peel eaten, fat added in cooking, NS as to type of fat",
"Sweet potato, baked, peel not eaten, NS as to fat added in cooking",
"Sweet potato, baked, peel not eaten, fat not added in cooking",
"Sweet potato, baked, peel not eaten, fat added in cooking, NS as to type of fat",
"Sweet potato, boiled, NS as to fat added in cooking",
"Sweet potato, boiled, fat not added in cooking",
"Sweet potato, boiled, fat added in cooking, NS as to type of fat",
"Sweet potato, canned, NS as to fat added in cooking",
"Sweet potato, canned, fat not added in cooking",
"Sweet potato, canned, fat added in cooking",
"Potato, canned, NS as to fat added in cooking",
"Potato, canned, fat added in cooking, NS as to type of fat",
"Potato, canned, fat not added in cooking",
]

names_usda_df = pd.read_excel("../data/names_USDA.xlsx")
bd_names = list(names_usda_df['Main food description'])

#%%



# Vamos a coger manualmente una receta y obtener sus ngramas


recipe_steps = "Cut the potatoes into slices and fry them into the hot olive oil. When the potatoes are crispy and slightly brown, place them over a towel and keep them warm. Fry the eggs in the same oil that you use for the potatoes. Cover with a lid while frying. In a deep big plate place the potatoes in the base. Cover with serrano ham and top with the fry eggs. Sprinkle with salt, pepper, and paprika"


# 1. Primero aplicar el mismo preprocesamiento a los textos que el que utilizamos para crear el wordembedding. Es decir, quitar stopwords, quitar puntuación, stemming.... etc. 
def preprocess_recipe(text_recipe, create_tokens = True):
    
    if create_tokens:
        tokens = list(gensim.utils.tokenize(text_recipe, lower=True))
        
    else:
        tokens = text_recipe
        
    tokens = preprocess_string(" ".join(tokens), CUSTOM_FILTERS) 
    sentenc = list(bigram_loaded[tokens])
    
    return sentenc


bd_names_processed = [preprocess_recipe(x) for x in bd_names]

# Ahora vamos a filtrar por los ngramas que tengan algun tipo de cocinado + ingrediente (minimo 1)
def get_ingredients_from_ngram(ngram):    
    possible_ingredients = list(ingredients_df.preprocessed)
    found_ing = [x for x in ngram.split(" ") if x in possible_ingredients ]
    return found_ing


def get_ctype_from_ngram(ngram):
    possible_cooking_types = list(cooking_types_df.preprocessed)
    found_ctypes = [x for x in ngram.split(" ") if x in possible_cooking_types ]
    return found_ctypes

def get_processed_ngram(ngram):
#    print(ngram)
    res = ngram[0] + ngram[1]
    return " ".join(res)


def get_USDA_equivalent(ngram):
    
    vector_similarity = np.zeros(len(bd_names_processed))
#    list_similarity = []
    # iteramos para encontrar la similitud con los elementos de la bd
    for i,item in enumerate(bd_names_processed):
        s = modelo_guardado.wv.wmdistance(ngram.split(" "), item)
        vector_similarity[i] = s
#        list_similarity.append(s)


    sorted_list = np.argsort(vector_similarity)
    if vector_similarity[sorted_list[0]] <= 15:
        most_similar = bd_names[sorted_list[0]]
    else:
        most_similar = "No matches"
    
    return most_similar





#%%



ingredients_df = pd.read_csv("../data/ingredients.csv")
cooking_types_df = pd.read_csv("../data/cooking.csv")


ingredients_df['preprocessed'] = ingredients_df['ingredients'].apply(preprocess_recipe, False)
ingredients_df['preprocessed'] = ingredients_df['preprocessed'].apply(" ".join) 
ingredients_df = ingredients_df.drop_duplicates(subset=['preprocessed'])



cooking_types_df['preprocessed'] = cooking_types_df['cooking_type'].apply(preprocess_recipe, False)
cooking_types_df['preprocessed'] = cooking_types_df['preprocessed'].apply(" ".join) 
cooking_types_df = cooking_types_df.drop_duplicates(subset=['preprocessed'])
#cooking_types_df['preprocessed'] = preprocess_recipe(list(cooking_types_df['cooking_type']), create_tokens=False)
#%%
# 2. obtenemos ngramas, quitando stopwords y de tamaño 5 máximo
# http://www.albertauyeung.com/post/generating-ngrams-python/
def get_equivalent_from_ngram(text_rcp,calculate_equivalences = True):
    
    recipe_steps_preprocessed = preprocess_recipe(text_rcp)
    ngramas = []
    for n in range (1,6):
        ngramas += list(ngrams(recipe_steps_preprocessed, n))
    ngramas = [" ".join(x) for x in ngramas]
    
    ngramas_df = pd.DataFrame(ngramas)
    ngramas_df.columns = ["ngram"]
    # ingredients_common = ngramas_df.merge(ingredients_df, left_on='ngram', right_on='preprocessed')
    # Nos quedaremos con los ngramas que tengan ingredientes o cooking types que nos interesen    
    ngramas_df['ingredients'] = ngramas_df['ngram'].apply(get_ingredients_from_ngram)
    ngramas_df['number_ingredients'] = ngramas_df['ingredients'].apply(len) 
    ngramas_df['cooking_types'] = ngramas_df['ngram'].apply(get_ctype_from_ngram)
    ngramas_df['number_cooking_types'] = ngramas_df['cooking_types'].apply(len)
    #filtramos por aquellas que minimo tienen dos ingredientes
    ngramas_df_relevant = ngramas_df[ngramas_df['number_ingredients'] <= 2]

    ngramas_df_relevant = ngramas_df_relevant[ngramas_df_relevant['number_ingredients'] >= 1]
    # ademas tiene que tener algun tipo de cocinado
    ngramas_df_relevant = ngramas_df_relevant[ngramas_df_relevant['number_cooking_types'] == 1]
    
    ngramas_df_relevant['result'] = ngramas_df_relevant[['ingredients','cooking_types']].apply(get_processed_ngram, axis=1)
    # ngrams_final = list(set(ngramas_df_relevant['result']))
    
    ngramas_df_relevant = ngramas_df_relevant.drop_duplicates(subset=['result'])
    
    if calculate_equivalences:
        ngramas_df_relevant['USDA_equivalent'] = ngramas_df_relevant['result'].apply(get_USDA_equivalent)
        return ngramas_df_relevant

#    return pd.DataFrame({'recipe_steps':[text_rcp],'ngrams': [str(ngramas_df_relevant.shape[0])]},columns=['recipe_steps', 'ngrams'])
    return {'recipe_steps':text_rcp, 'ngrams':ngramas_df_relevant.shape[0], 'values':list(set(ngramas_df_relevant.result))}
        
    #calculamos numero de ngramas que realmente tienen un


#%%
    
df_res = get_equivalent_from_ngram(recipe_steps)


#%%
df_res["recipe_step"] = recipe_steps

df_res2 = get_equivalent_from_ngram(recipe_steps,False)




