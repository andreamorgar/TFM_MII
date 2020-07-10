#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 11:41:09 2019

@author: andrea



Estudio de ocurrencias de palabras en nuestro modelo
"""

from nltk.util import ngrams
from gensim.models.phrases import Phrases, Phraser
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords, stem_text
import gensim
import pandas as pd
from gensim.models import KeyedVectors
import numpy as np
import os



from gensim.corpora.dictionary import Dictionary
#%%

# Cargamos los modelos que necesitamos
CUSTOM_FILTERS = [remove_stopwords, stem_text]
CUSTOM_FILTERS_2 = [remove_stopwords]
w2v_model = KeyedVectors.load("../models/v2/modelo3")
bigram_loaded = Phraser.load("../models/v2/my_bigram_model.pkl")






from gensim.models import KeyedVectors
# Load vectors directly from the file
model = KeyedVectors.load_word2vec_format('/home/andrea/Escritorio/GoogleNews-vectors-negative300.bin', binary=True)
#%%
model.wv.most_similar('garlic')
w2v_model.wv.most_similar('garlic')



#%%

model_vocabulary = w2v_model.wv.vocab

print(len(model_vocabulary))

#%%
# necesarias para la función
total_ocurrencias = 12383335
count_words_vocab = {}

for word in list(model_vocabulary.keys()):
    count_words_vocab[str(word)] = model_vocabulary[word].count
    
    
    

df = pd.DataFrame.from_dict(count_words_vocab, orient='index', columns=[ 'n'])
df['word'] = count_words_vocab.keys()
df['total'] = df['n'].sum()

#%%

ax = df.plot.hist(bins=12, alpha=0.5)


df.hist(column='n')



#%%
from gensim import corpora,models
texts = [['human', 'interface', 'computer'],
 ['survey', 'user', 'computer', 'system', 'response', 'time'],
 ['eps', 'user', 'interface', 'system'],
 ['system', 'human', 'system', 'eps'],
 ['user', 'response', 'time'],
 ['trees'],
 ['graph', 'trees'],
 ['graph', 'minors', 'trees'],
 ['graph', 'minors', 'survey']]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
#%%
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)
    
    
#%%
#Term Frequency (TF)
#
#The number of times a word appears in a document divded by the total number of words in the document. 
#Every document has its own term frequency.
#
#
#
#Inverse Data Frequency (IDF)
#
#The log of the number of documents divided by the number of documents that contain the word w. 
#Inverse data frequency determines the weight of rare words across all documents in the corpus.
document1 = ['walnut', 'oil']


document2 = ['celeri', 'raw']

dictionary = Dictionary(documents=[document1, document2])

dictionary.doc2bow(document2) 
doc_len = len(document1)
vocab_len = len(dictionary)



d = np.zeros(vocab_len, dtype=np.double)
nbow = dictionary.doc2bow(document1)  # Word frequencies.
doc_len = len(document1)
for idx, freq in nbow:
    d[idx] = freq / float(doc_len)  # Normalized word frequencies.
    
    
    
    
#%%
try:
    from pyemd import emd
    PYEMD_EXT = True
except ImportError:
    PYEMD_EXT = False
    
import logging
logger = logging.getLogger(__name__)

import numpy as np
    
count_words_vocab = {}
for word in list(model_vocabulary.keys()):
    count_words_vocab[str(word)] = model_vocabulary[word].count
                
def wmdistance_versionAndrea(document1, document2):
        """
        Compute the Word Mover's Distance between two documents. When using this
        code, please consider citing the following papers:

        .. Ofir Pele and Michael Werman, "A linear time histogram metric for improved SIFT matching".
        .. Ofir Pele and Michael Werman, "Fast and robust earth mover's distances".
        .. Matt Kusner et al. "From Word Embeddings To Document Distances".

        Note that if one of the documents have no words that exist in the
        Word2Vec vocab, `float('inf')` (i.e. infinity) will be returned.

        This method only works if `pyemd` is installed (can be installed via pip, but requires a C compiler).

        Example:
            >>> # Train word2vec model.
            >>> model = Word2Vec(sentences)

            >>> # Some sentences to test.
            >>> sentence_obama = 'Obama speaks to the media in Illinois'.lower().split()
            >>> sentence_president = 'The president greets the press in Chicago'.lower().split()

            >>> # Remove their stopwords.
            >>> from nltk.corpus import stopwords
            >>> stopwords = nltk.corpus.stopwords.words('english')
            >>> sentence_obama = [w for w in sentence_obama if w not in stopwords]
            >>> sentence_president = [w for w in sentence_president if w not in stopwords]

            >>> # Compute WMD.
            >>> distance = model.wmdistance(sentence_obama, sentence_president)
        """

        if not PYEMD_EXT:
            raise ImportError("Please install pyemd Python package to compute WMD.")

        # Remove out-of-vocabulary words
        len_pre_oov1 = len(document1)
        len_pre_oov2 = len(document2)
        document1 = [token for token in document1 if token in list(w2v_model.wv.vocab.keys())]
        document2 = [token for token in document2 if token in list(w2v_model.wv.vocab.keys())]
        
#        print(document1)
#        print(document2)
        diff1 = len_pre_oov1 - len(document1)
        diff2 = len_pre_oov2 - len(document2)
        if diff1 > 0 or diff2 > 0:
            logger.info('Removed %d and %d OOV words from document 1 and 2 (respectively).',
                        diff1, diff2)

        if len(document1) == 0 or len(document2) == 0:
            logger.info('At least one of the documents had no words that were'
                        'in the vocabulary. Aborting (returning inf).')
            return float('inf')

        dictionary = Dictionary(documents=[document1, document2])
        vocab_len = len(dictionary)

        
        # Sets for faster look-up.
        docset1 = set(document1)
        docset2 = set(document2)

        # ------------------------ ADDED --------------------------------------
        freqs = np.zeros(vocab_len, dtype=np.double)
        freq_normalized = {}
        for idx,word in dictionary.items(): 
            freqs[idx] = count_words_vocab[word]
             
       # 2. Le añadimos la ponderación en función del vocabulario
        max_value = np.max(freqs)
        min_value = np.min(freqs)
        for idx,word in dictionary.items():
#            freq_normalized[word] = (freqs[idx]-min_value)/(max_value-min_value)
            freq_normalized[word] = (freqs[idx])/(max_value)

        # ------------------------ ADDED --------------------------------------
                
        # Compute distance matrix.
        distance_matrix = np.zeros((vocab_len, vocab_len), dtype=np.double)
        for i, t1 in dictionary.items():
            for j, t2 in dictionary.items():
                if not t1 in docset1 or not t2 in docset2:
                    continue
                # Compute Euclidean distance between word vectors.
                rate = freq_normalized[t1] * freq_normalized[t2]
                distance_matrix[i, j] = rate * (np.sqrt(np.sum((w2v_model[t1] - w2v_model[t2])**2)))

                 
        if np.sum(distance_matrix) == 0.0:
            # `emd` gets stuck if the distance matrix contains only zeros.
            logger.info('The distance matrix is all zeros. Aborting (returning inf).')
            return float('inf')

        def nbow(document):
            d = np.zeros(vocab_len, dtype=np.double)
            nbow = dictionary.doc2bow(document)  # Word frequencies.
            doc_len = len(document)

            for idx, freq in nbow:
                d[idx] = freq / float(doc_len)  # Normalized word frequencies.
            return d
        
        def tf(document):
            d = np.zeros(vocab_len, dtype=np.double)
            freqs = np.zeros(vocab_len, dtype=np.double)

            nbow = dictionary.doc2bow(document)  # Word frequencies.
            doc_len = len(document)

            # 1. primero obtenemos el TF (numero de veces que sale el término/total palabras)
            for idx, freq in nbow:
                d[idx] = freq / float(doc_len)  # Normalized word frequencies.
                  
            # Obteemos frecuencas de cada palabra
            for idx,word in dictionary.items(): 
                freqs[idx] = count_words_vocab[word]
             
            # 2. Le añadimos la ponderación en función del vocabulario
#            for idx,word in dictionary.items():
#                d[idx] = d[idx]*(freqs[idx)/total_ocurrencias)
#                
                
            max_value = np.max(freqs)
            min_value = np.min(freqs)

            
#            # 2. Le añadimos la ponderación en función del vocabulario
            for idx,word in dictionary.items():
                rate = (freqs[idx]-min_value)/(max_value-min_value)

                d[idx] = d[idx]*rate
                
                
            # ----------------------------------------------------------------
            # Para hacer TF-IDF
            # 2 Ahora añadimos el idf
#            for idx,word in dictionary.items():
#                d[idx] = d[idx] * np.log(264310/count_words_vocab[word])
#             
           


            return d

        # Compute nBOW representation of documents.
        d1 = nbow(document1)
        d2 = nbow(document2)

        print(distance_matrix)


        return emd(d1, d2, distance_matrix)
    
    
wmdistance_versionAndrea(document1,document2)
#w2v_model.wmdistance(document1,document2)







#%%

model= KeyedVectors.load("../models/v2/modelo3")
keys= ['ketchup', 'lemon', 'chicken', 'biscuit', 'pasta','walnut','banana','oyster','tuna']
#keys=['milk', 'rice', 'cake', 'sugar', 'pepper']
embedding_clusters = []
word_clusters = []
for word in keys:
    embeddings = []
    words = []
    for similar_word, _ in model.most_similar(word, topn=5):
        words.append(similar_word)
        embeddings.append(model[similar_word])
    embedding_clusters.append(embeddings)
    word_clusters.append(words)
    
#%%
    
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#% matplotlib inline
        
from sklearn.manifold import TSNE
import numpy as np
words_ak = []
embeddings_ak = []
for word in list(model.wv.vocab):
    embeddings_ak.append(model.wv[word])
    words_ak.append(word)
    
tsne_ak_2d = TSNE(perplexity=30, n_components=2, init='pca', n_iter=3500, random_state=32)
embeddings_ak_2d = tsne_ak_2d.fit_transform(embeddings_ak)

def tsne_plot_2d(label, embeddings, words=[], a=1):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, 1))
    x = embeddings[:,0]
    y = embeddings[:,1]
    plt.scatter(x, y, c=colors, alpha=a, label=label)
    for i, word in enumerate(words):
        plt.annotate(word, alpha=0.3, xy=(x[i], y[i]), xytext=(5, 2), 
                     textcoords='offset points', ha='right', va='bottom', size=10)
    plt.legend(loc=4)
    plt.grid(True)
#    plt.savefig("hhh.png", format='png', dpi=150, bbox_inches='tight')
    plt.show()

tsne_plot_2d('Recipes', embeddings_ak_2d, a=0.1)

#%%
embedding_clusters = np.array(embedding_clusters)
n, m, k = embedding_clusters.shape
tsne_model_en_2d = TSNE(perplexity=15, n_components=2, init='pca', n_iter=5000, random_state=32)
embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)



def tsne_plot_similar_words(title, labels, embedding_clusters, word_clusters, a, filename=None):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
    for label, embeddings, words, color in zip(labels, embedding_clusters, word_clusters, colors):
        x = embeddings[:, 0]
        y = embeddings[:, 1]
        plt.scatter(x, y, c=color, alpha=a, label=label, s=80)
        for i, word in enumerate(words):
            plt.annotate(word, alpha=1.0, xy=(x[i], y[i]), xytext=(5, 2),
                         textcoords='offset points', ha='center', va='bottom',size=18)
    plt.legend(loc=4,prop={'size': 15})
    plt.title(title, fontsize=20 )
    plt.grid(True)
    if filename:
        plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')
    plt.show()


tsne_plot_similar_words('Palabras similares en el vocabulario del modelo', keys, embeddings_en_2d, word_clusters, 0.7,
                        'similar_words.png')