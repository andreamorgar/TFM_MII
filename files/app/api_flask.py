#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:07:21 2020

@author: andrea
"""

#%%
from gensim.models import KeyedVectors
from gensim.models.phrases import Phrases, Phraser
from utils import get_similar, get_adapted_recipe
import pandas as pd
#%%

#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
import recipe_class as recipe_class

from recipesdb import getDocument, pushDocument, updateDocument, getAdaptedDocument
from recipesdb import get_all_recipes, get_all_recipes_by_tag, get_all_tags, delete_document
from recipesdb import get_all_adapted_recipes,pushAdaptedDocument

app = Flask(__name__)



predictions = []
predictions_objects = []


@app.route('/')
def get_home():
    return jsonify(status='OK')

# Ruta status (devolverá OK)
@app.route('/status')
def get_status():
    return jsonify(status='OK')
 # ------------------------------------------------------------------------------

# Acceder a una receta concreta por su ID
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    if request.method == 'GET':

        # Buscamos en la colección de recetas la que se corresponde con ese ID
        result = getDocument(recipe_id)
        if result is None:
            abort(404)

        # eliminamos el valor _id de la info a devolver puesto que no da 
        # información útil
        result.pop('_id')
        
        return jsonify(result)
# ------------------------------------------------------------------------------

# Consultar las recetas que se corresponden con una etiqueta concreta     
@app.route('/recipes/tag/<recipe_tag>', methods=['GET'])
def get_recipe_by_tag(recipe_tag):
    if request.method == 'GET':
       
        # Realizamos una búsqueda por la etiqueta
        return get_recipes_by_tag(recipe_tag)

#------------------------------------------------------------------------------
        
def get_recipes(option="normal"):

    if option == 'normal':
    
        # Obtenemos la lista completa de recetas de la colección
        cursor = get_all_recipes()
    else:
        cursor = get_all_adapted_recipes()
        
    actual_list_of_recipes = []

    # Adaptamos cada receta al formato que nos interesa
    for document in cursor:
        next_dict = document
        # Borramos el campo _id puesto que no es relevante para la visualización
        # de la receta
        next_dict.pop('_id')
        actual_list_of_recipes.append(next_dict)

    # devolvemos lista entera de recetas
    return jsonify({'recipes': actual_list_of_recipes })

#------------------------------------------------------------------------------
def get_tags():

    # Obtenemos todas las etiquetas en la colección
    cursor = get_all_tags()
    actual_list_of_tags = []

    # Adaptamos el formato para devolver un .json
    for document in cursor:
        next_dict = document
         # Borramos el campo _id puesto que no es relevante para la visualización
        next_dict.pop('_id')

        actual_list_of_tags.append(next_dict)


    return jsonify({'tags': actual_list_of_tags })

#------------------------------------------------------------------------------
def get_recipes_by_tag(recipe_tag):
    print(recipe_tag)
    #first we get all the documents of the database by an empty search
    cursor = get_all_recipes_by_tag(recipe_tag)
    actual_list_of_recipes = []

    # We have to look in every document to the cursor to get a list of the
    # documents (we can't just print a cursor type)
    for document in cursor:
        print(document)
        next_dict = document
        next_dict.pop('_id')
        # we add the next document to the list of documents that we are
        # going to print
        actual_list_of_recipes.append(next_dict)


    return jsonify({'recipes': actual_list_of_recipes })


#------------------------------------------------------------------------------
# Método GET para consultar todas las etiquetas almacenadas en la colección
@app.route('/tags', methods=['GET'])
def obtain_tags():
    if request.method == 'GET':
        return get_tags()

# ------------------------------------------------------------------------------
# Ruta para gestionar las recetas
@app.route('/recipes', methods=['GET','PUT', 'POST', 'DELETE'])
def create_recipes():

    # Método get para consultar todas las recetas en la colección
    if request.method == 'GET':
        return get_recipes()
    # --------------------------------------------------------------------------

    # Método post para insertar la receta a la colección en la base de datos
    elif request.method == 'POST':
        # Create an object from class Prediction with the information inserted
        # in the curl
        print(request.json)
        r = recipe_class.Recipe(request.json['id_recipe'],request.json['name'],request.json['minutes'],
                                   request.json['tags'],request.json['nutrients'],request.json['n_steps'],
                                   request.json['steps'],request.json['description'],request.json['n_ingredients'],
                                   request.json['ingredients'],request.json['image'])

        # We push the new prediction to the Database
        record = {
            "id_recipe": str(r['id_recipe']),
            "name": r['name'],
            "minutes": str(r['minutes']),
            "tags": r['tags'],
            "nutrients": r['nutrients'],
            "n_steps": r['n_steps'],
            "steps": r['steps'],
            "description": r['description'],
            "n_ingredients": r['n_ingredients'],
            "ingredients": r['ingredients'],
            "image": r['image']
        }
        pushDocument(record)

        return jsonify(r.__dict__)

    # --------------------------------------------------------------------------
    # Método put para modificar una receta
    elif request.method == 'PUT':

        # We get from the request the value of the attributes we want to update
        id_rp = request.json['id_recipe']

        recipe = getDocument(id_rp)
        # If the document we are looking for doesn't exist, we abort the update
        if recipe is None:
            return abort(404)

        # We have to build a dictionary with the changes we want to submit: ONLY ONE
        record = {
            "id_recipe": request.json['id_recipe'],
            request.json['attribute']: request.json['value']
        }

        # We update the document of the database
        updateDocument(recipe,record)

        # We access to the database to get the updated document
        updated_rp = getDocument(id_rp)

        # We are going to show the content of the query, so we have to ommit the
        # id that the database add to our query
        updated_rp.pop('_id')

        return jsonify({'recipe': updated_rp}),201


    # -------------------------------------------------------------------------
    
    # Método delete para eliminar una receta
    elif request.method == 'DELETE':
        # Search for the prediction with the ID introduced
        id_rp = request.json['id_recipe']
        print(id_rp)
        not_wanted_query = getDocument(id_rp)
        print(not_wanted_query)
        # If the document we are looking for doesn't exist, we do nothing
        
        if not_wanted_query is None:
            return jsonify({'msg': "Deleted"})

        # If the document we are looking for exists, we can delete it with the
        # function delete_document.
        delete_document(not_wanted_query)

        return jsonify({'msg': "Deleted"})


# -------------------------------------------------------------------------
@app.route('/model/similar/<word>', methods=['GET'])
def similar_words_from_model(word):
    global model
    if request.method == 'GET':

        similar_words = get_similar(model,word)
        return jsonify({'similar': similar_words})
        
# -------------------------------------------------------------------------
@app.route('/model/adapt/<restriction>/<id_recipe>', methods=['GET'])
def adapt_recipe(restriction,id_recipe):
    global model, bigram_loaded, spanish_ingredients, bd_names, bd_names_translate_andrea
    rp = getDocument(id_recipe)

    rp['ingredients'] = get_adapted_recipe(recipe=rp,model=model,bigram=bigram_loaded,db=bd_names,db_translated=bd_names_translate_andrea, nutritional_data=spanish_ingredients,restriction=restriction)
    

    rp.pop('_id')

    return jsonify(rp)
# ------------------------------------------------------------------------------
@app.route('/model/adapt/steps', methods=['POST'])
def adapt_recipe_steps():
    print(request.json['name'])
    rp = {'ingredients': request.json['ingredients'] ,'steps': request.json['steps']}
    steps = get_adapted_steps(rp)
    print(steps)
    return jsonify({'steps': steps})


# -------------------------------------------------------------------------
def get_adapted_steps(recipe):
    ingr_mod = []
    
    adapted_steps = [{'step':s,'modified':'no'} for s in recipe['steps']]
    for i in recipe['ingredients']:
        if i['modified'] == 'yes':
            ingr_mod.append(i['name'])

    for number,i in enumerate(adapted_steps):
        if any(ext in i['step'] for ext in ingr_mod):
            adapted_steps[number]['modified'] ='yes'
            

    return adapted_steps 


# -----------------------------------------------------------------------------
# Ruta para gestionar recetas adaptadas
@app.route('/adapted_recipes', methods=['GET','PUT', 'POST', 'DELETE'])
def create_adapted_recipes():

    # Método para consultar todas las recetas adaptadas almacenadas
    if request.method == 'GET':
        return get_recipes(option='adapted')
    # --------------------------------------------------------------------------

    # Método para insertar una receta adaptada
    elif request.method == 'POST':
        # Creamos un objeto de la clase Receta y lo insertamos en la base de datos
        
        r = recipe_class.Recipe(request.json['id_recipe'],request.json['name'],request.json['minutes'],
                                   request.json['tags'],request.json['nutrients'],request.json['n_steps'],
                                   request.json['steps'],request.json['description'],request.json['n_ingredients'],
                                   request.json['ingredients'],request.json['image'])

        # We push the new prediction to the Database
        record = {
            "id_recipe": str(r['id_recipe']),
            "name": r['name'],
            "minutes": str(r['minutes']),
            "tags": r['tags'],
            "nutrients": r['nutrients'],
            "n_steps": r['n_steps'],
            "steps": r['steps'],
            "description": r['description'],
            "n_ingredients": r['n_ingredients'],
            "ingredients": r['ingredients'],
            "image": r['image']
        }

        pushAdaptedDocument(record)
        print(record)
        return jsonify({'msg': "ok"})



    # --------------------------------------------------------------------------
    elif request.method == 'DELETE':
        
        id_rp = request.json['id_recipe']
        print(id_rp)
        not_wanted_query = getAdaptedDocument(id_rp)
        print(not_wanted_query)
        # If the document we are looking for doesn't exist, we do nothing
        
        if not_wanted_query is None:
            return jsonify({'msg': "Deleted"})

        # If the document we are looking for exists, we can delete it with the
        # function delete_document.
        delete_document(not_wanted_query,adapted=True)


        return jsonify({'msg': "Deleted"})

# -----------------------------------------------------------------------------        

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # cargamos los modelos y las bases de datos al inicio de la ejecución de 
    # la API para acceder a ellos en cualquier momento
    model = KeyedVectors.load("../../models/v2/modelo3")
    bigram_loaded = Phraser.load("../../models/v2/my_bigram_model.pkl")
    spanish_ingredients = pd.read_excel('../../data/recipes/bd-producto-app.xlsx') 
    bd_names = list(spanish_ingredients['food_name_eng'])
    bd_names_translate_andrea = list(spanish_ingredients['translate_andrea'])
    
    app.run(host="0.0.0.0",debug=True)
