#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:01:30 2020

@author: andrea
"""


import pandas as pd
import matplotlib.pyplot as plt
#%%

df = pd.read_excel('../data/res-hybrid.xlsx')


with plt.style.context('seaborn-poster'): #https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html seaborn-poster default

    ax = plt.gca()
    df.plot(kind='line',x='w',y='Top 1',ax=ax)
    df.plot(kind='line',x='w',y='Top 2', ax=ax)
    df.plot(kind='line',x='w',y='Top 3',ax=ax)
    df.plot(kind='line',x='w',y='Top 5',ax=ax)
    df.plot(kind='line',x='w',y='Top 10',ax=ax)
    
#    plt.plot(get_usda_accuracy(filename_we_results='resultados-traduccion-ampliado-we-google-sin-stem.xlsx'),label="w.e. Google")
#    plt.plot(get_usda_accuracy(filename_we_results='resultados-traduccion-ampliado.xlsx'),label="w.e. recetas")
    # Number of accent colors in the color scheme
    plt.title('Mapeo con la distancia híbrida')
    
#    plt.xticks(x, [x for x in range(1,11)])
    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.legend.html
    # enlace con tipos de leyendas
    
    # https://matplotlib.org/3.1.1/gallery/pyplots/whats_new_98_4_legend.html#sphx-glr-gallery-pyplots-whats-new-98-4-legend-py
    # enlace para poner la legenda así
#    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
#    leg.get_frame().set_alpha(0.5)
    plt.grid(alpha=0.3)
    plt.legend(loc='best')
    plt.xlabel('w', fontsize=14)
    plt.ylabel('Precisión de los mapeos (%)', fontsize=14)

plt.show()