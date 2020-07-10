#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:23:15 2019

@author: Andrea Morales Garzón

Fichero con la implementación del modelo de Word Embedding.
Se utiliza el algoritmo Word2Vec (Mikolov, 2013) con la librería Gensim

También contiene ejemplos de uso y pruebas preliminares para 
comprobar que el modelo entrenado funciona de manera adecuada.
"""

# librerías utilizadas

# Directorio del que se obtienen las recetas
TEXT_DATA_DIR = '../recipes/'

import os
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text


#%%

# Entrenamiento del modelo w2v

texts = []
labels_index = {} 
labels = []
label_text = []

# Se recorren los directorios de recetas para encontrar 
print('Obteniendo el texto de las recetas...')
for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)
    print(name)
    if os.path.isdir(path):
        label_id = len(labels_index)
        # asignamos numero a cada directorio
        labels_index[name] = label_id
        for fname in sorted(os.listdir(path)):
            fpath = os.path.join(path, fname)
            f = open(fpath, encoding='latin-1')
            t = f.read()
            texts.append(t)
            f.close()
            labels.append(label_id)
            label_text.append(name)
print('Se han encontrado %s textos.' % len(texts))

# -----------------------------------------------------------------------------


#1. Obtención de los tokens de los textos
print('Obtención de los tokens de los textos')
tokens = [list(gensim.utils.tokenize(doc, lower=True)) for doc in texts]

#2. Entrenamiento del modelo de bigramas
print('Entrenamiento del modelo de bigramas')
bigram_mdl = gensim.models.phrases.Phrases(tokens, min_count=1, threshold=2)

# 3, Aplicamos preprocesamiento a los textos
CUSTOM_FILTERS = [remove_stopwords, stem_text]
tokens = [preprocess_string(" ".join(doc), CUSTOM_FILTERS) for doc in tokens]

print('Aplicamos el modelo de bigramas para obtener los bigramas del texto')
bigrams = bigram_mdl[tokens]
# Guardamos el modelo de bigramas
bigram_mdl.save("../models/v2/my_bigram_model.pkl")


# -----------------------------------------------------------------------------

# PARÁMETROS
    # min_count: ignora las palabras que aparecen menos de 3 veces en el corpus
    # size: tamaño de los vectores para la representación numérica de las palabras
    # window: tamaño de ventana para saber cuántas palabras del contexto se van a utilizar
    # workers: número de procesos (para parelización)
    # número de épocas para el entrenamiento
    
all_sentences = list(bigrams)
print('Entrenamiento del modelo w2v...')
model = Word2Vec(all_sentences, min_count=3, size=300, workers=4, window=5, iter=30)       

# -----------------------------------------------------------------------------

print('Guardando modelo w2v...')
model.save("../models/v2/modelo3")

# -----------------------------------------------------------------------------

#%%

# Algunas pruebas con el modelo

# https://radimrehurek.com/gensim/models/keyedvectors.html
modelo_guardado = KeyedVectors.load("../models/v2/modelo3")

# Obtenemos la representación de un alimento
vector_prueba = modelo_guardado.wv['potato']

# -----------------------------------------------------------------------------
#Pruebas con el vocabulario 

vocab = model.wv.vocab #vocabulario
print(len(vocab)) # tam vocabulario

# Encontrar los elementos más similares para CAKE
modelo_guardado.wv.most_similar('cake')

# Encontrar los elementos más similares para MAYONESA
modelo_guardado.wv.most_similar('custard')

# Cálculo de similitudes entre palabras del vocabulario
modelo_guardado.wv.similarity('biscuit','cake')
modelo_guardado.wv.similarity('pizza','lasagna')


# -----------------------------------------------------------------------------
# Algunas pruebas preliminares con distancia Word Mover
# Realizadas para comprobar que el modelo funciona correctamente

sentence_1 = 'potatoes fried oil'.lower().split()

# con el preprocesamiento se queda igual que la anterior
sentence_2 = 'potato, fried, oil'.lower().split()

# Otros ejemplos para comparar medidas de distancia 
sentence_3 = 'potato, fried, butter'.lower().split()
sentence_4 = 'potato, roasted, salt'.lower().split()

# Aplicamos Word Mover Distance para calcular distancias entre descripciones
# https://tedboy.github.io/nlps/generated/generated/gensim.models.Word2Vec.wmdistance.html 
 
similarity_1 = modelo_guardado.wv.wmdistance(sentence_1, sentence_2)
# valor similarity; 0.0

similarity_2 = modelo_guardado.wv.wmdistance(sentence_1, sentence_3)
# valor similarity; 40.613792419433594

similarity_3 = modelo_guardado.wv.wmdistance(sentence_1, sentence_4)
# valor similarity; 51.771560668945305



