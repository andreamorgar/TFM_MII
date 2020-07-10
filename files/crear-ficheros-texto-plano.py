#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 10:15:59 2019

@author: andrea

Script para generar ficheros con el texto de las recetas. 

"""
import os
import json
import string
#%%
# bbc
for (dirpath, dirnames, filenames) in os.walk('/home/andrea/Escritorio/Stance4Health-priv/data/RECIPES/BBC-Recipe-Web-Scraper-master/Recipes/'):
    for f in filenames:
        print(f)
        with open(os.path.join(dirpath, f), 'r') as myfile:
            data=myfile.read()
        json_resultante = json.loads(data)
        with open('data/bbc/'+json_resultante['ID Name'], 'w') as file2:
            file2.write(json_resultante['Preparation'])
        
        
#%%
# epicurious
 

def generate_id(name_recipe,num):
    name_recipe.translate(str.maketrans('', '', string.punctuation)) 
    name_recipe = name_recipe.replace("/","-")
    return name_recipe.replace(" ","-")[:-1] + "-" + str(num)
            
       
with open('../recipe_sources/epirecipes/full_format_recipes.json', 'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)


for num,i in enumerate(data):
    if 'directions' in i.keys():
        
        directions = ""
        for step in i['directions']: 
            directions += step + " "
        id_name = generate_id(i['title'],num)
       
        with open('data/epicurious/'+id_name, 'w') as file2:
            file2.write(directions[:-1]) #quitamos el ultimo espacio que añade el for
            
            
#%%
doc = []
with open('../recipe_sources/epicurious-recipes.json', 'r') as data_file:
    json_data = data_file.readlines()
    for line in json_data:
        doc.append(json.loads(line))
        
set1 = set()
for i in doc:
    if i['title'] in set1:
        print(i['title'])
    set1.add(i['title'])
    
    
for num, recipe in enumerate(doc):
    if 'instructions' in recipe.keys():
    
        id_name = recipe['url'][32:]
        directions = ""
        for step in recipe['instructions']: 
            directions += step + " "
        
        with open('data/cookstr/'+id_name, 'w') as file2:
            file2.write(directions[:-1]) #quitamos el ultimo espacio que añade el for
#%%
# cerooriginals  --> allrecipes
doc = []
with open('../recipe_sources/allrecipes-recipes.json', 'r') as data_file:
    json_data = data_file.readlines()
    for line in json_data:
        doc.append(json.loads(line))
        


diccionario = {}


def generate_id_wo_number(name_recipe):
    name_recipe.translate(str.maketrans('', '', string.punctuation)) 
    name_recipe = name_recipe.replace("/","-")
    return name_recipe.replace(" ","-")[:-1]

for num, recipe in enumerate(doc):
    if 'instructions' in recipe.keys():
    
        id_name = generate_id_wo_number(recipe['title'])
        print(recipe['title'])
#        if id_name in diccionario:
#            diccionario[recipe['title']].append(recipe)
#        else:
#            diccionario[recipe['title']] = [recipe]
        directions = ""
        for step in recipe['instructions']: 
            directions += step + " "
        
        with open('data/allrecipes/'+id_name, 'w') as file2:
            file2.write(directions[:-1]) #quitamos el ultimo espacio que añade el for
                
#%%

doc = []
with open('../recipe_sources/cookstr-recipes.json', 'r') as data_file:
    json_data = data_file.readlines()
    for line in json_data:
        doc.append(json.loads(line))
        
set1 = set()
for i in doc:
    if i['title'] in set1:
        print(i['title'])
    set1.add(i['title'])
    
    
for num, recipe in enumerate(doc):
    if 'instructions' in recipe.keys():
    
        id_name = recipe['url'][32:]
        directions = ""
        for step in recipe['instructions']: 
            directions += step + " "
        
        with open('data/cookstr/'+id_name, 'w') as file2:
            file2.write(directions[:-1]) #quitamos el ultimo espacio que añade el for
                