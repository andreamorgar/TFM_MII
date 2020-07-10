#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:37:19 2020

@author: andrea
"""


import json
# Definimos métodos porque nos conviene que se comporte como un dict
# https://gist.github.com/turicas/1510860


# Para documentar una clase:
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

class Recipe:
    """Common base class for recipes taken from food.com kaggle's dataset
    Attributes:
        name(str):              refers to the name of the recipe
        id(int):                identificator of the object recipe
        minutes(int):           refers to the preparation time of the recipe
        tags(list(str)):        list of tags related to the recipes
        nutrients:              recipe nutrient info
        n_steps(int):           number of preparation steps
        steps(list(str)):       list of prepreparation steps
        description(str):       recipes' description 
        n_ingredients(int):     number of ingredients of the recipe
        ingredients(list(str)): list of recipes' ingredients
        image:                  image 
    """
    ID = 0

    def __init__(self, id_recipe, name, minutes, tags, nutrients,n_steps, steps,description, n_ingredients, ingredients, image):

        """ Args:
            name(str):              refers to the name of the recipe
            id(int):                identificator of the object recipe
            minutes(int):           refers to the preparation time of the recipe
            tags(list(str)):        list of tags related to the recipes
            nutrients:              recipe nutrient info
            n_steps(int):           number of preparation steps
            steps(list(str)):       list of prepreparation steps
            description(str):       recipes' description 
            n_ingredients(int):     number of ingredients of the recipe
            ingredients(list(str)): list of recipes' ingredient        
            image:                  image 
        """
        self.id_recipe = id_recipe
        self.name = name
        self.minutes = minutes
        self.tags = tags
        self.nutrients = nutrients
        self.n_steps = n_steps
        self.steps = steps
        self.description = description
        self.n_ingredients = n_ingredients
        self.ingredients = ingredients
        self.image = image
        

    def __getitem__(self, key):
        """ Method to get the value of an attribute of the class. For this
        functionality, it works in the same way than  a dict object.
            Args:
            key (str): refers to the name of the attribute we want to know
            the value
            Returns:
            Value associated to the attribute called 'key'
        """
        return self.__dict__[key]

    def __len__(self):
        """ Method to get the value of the number of attribute in the class.
            Args:
            No args
            Returns:
            An int value that represents the number of attributes in the class
        """
        return len(self.__dict__)

    def __repr__(self):

        """ Method to get a string representation with the information in class.
            Args:
            No args
            Returns:
            A str with all the content of the attributes and their values.
        """
        return repr(self.__dict__) # pragma: no cover
#%%

# Testear su funcionamiento
# ------------------------------------------------------------------------------
#if __name__ == '__main__':
#     
#     tags_list = ['30-minutes-or-less',  'time-to-make', 'course', 'main-ingredient', 'preparation', 'very-low-carbs', 
#     'sauces', 'condiments-etc', 'eggs-dairy', 'eggs', 'stove-top', 'dietary',
#     'low-carb', 'savory-sauces', 'low-in-something', 'equipment', 'number-of-servings']
#     
#     step_list = ['cut the butter into several pieces and bring to room temperature', 'in the top of a double boiler , combine egg yolks , lemon juice , salt and pepper', 'add a piece of butter', 'cook , stirring steadily with a wooden spoon or wire whisk , over , but not touching , boiling water', 'when butter melts and sauce begins to thicken , add remaining butter , stirring constantly until melted', 'continue cooking as sauce thickens , about 2 more minutes', 'immediately remove from heat']	
#     description = 'the secret to this easy hollandaise sauce is in separating the egg yolks. remove all the egg whites, as they can thin the sauce. also, it is best prepared in a double boiler to prevent overheating. serve over cooked asparagus, broccoli, or broiled tomatoes.	'
#     
#     ingredient_list = ['butter', 'lemon, juice of', 'salt', 'white pepper', 'egg yolks']
#     
#     nutrient_list = [1290.4, 213.0, 4.0, 53.0, 22.0, 417.0, 1.0]
#    
#     my_recipe = Recipe('49262','easiest ever hollandaise sauce','25',tags_list,nutrient_list,7,step_list,description,5,ingredient_list)
#    
#    
#     recipes = [my_recipe.__dict__]
#    
#    
#     json_recipes = json.dumps(recipes)
#    
#     print(my_recipe.__doc__)