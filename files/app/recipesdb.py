#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:56:15 2020

@author: andrea

# Working with mongoDB
"""

from pymongo import *
import os


# Depending on the enviroment variable, we will run or application with a local
# MongoDB database or mLab
MONGODB_URI = ""
direccion = str(os.environ.get("IP", "10.0.0.5"))
localhost = "localhost"
MONGODB_URI = "mongodb://"+ localhost + ":27017/recipesdb"


client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("recipesdb")
mongo_recipes = db.recipesdb
mongo_tags = db.tags # tags collection
mongo_adapted_recipes = db.adaptedrecipes

#-------------------------------------------------------------------------------
# Function if we want to get a prediction from the Database
# This function has only one parameter: ID from the prediction that we want to
# get
def getDocument(document_id):

    print("Request to query to the database...")
    print(document_id)
    recipe_document = mongo_recipes.find_one({"id_recipe":str(document_id)})
    print("Succesfully got document from collection")
    return recipe_document

def getAdaptedDocument(document_id):
    print("Request to query to the database...")
    print(document_id)
    recipe_document = mongo_adapted_recipes.find_one({"id_recipe":str(document_id)})
    print("Succesfully got document from collection")
    return recipe_document
##-------------------------------------------------------------------------------
# Function pushDocument
# With this function, we can add a new document in the collection
def pushDocument(document):
    print("Request to access to the database...")
    mongo_recipes.insert_one(document)
#    logger.info("Succesfully pushed document to the collection")
    pass

def pushAdaptedDocument(document):
    print("Request to access to the database...")
    mongo_adapted_recipes.insert_one(document)
#    logger.info("Succesfully pushed document to the collection")
    pass
#-------------------------------------------------------------------------------
# Function updateDocument
# With this function, we can update an existent document from the database
def updateDocument(document, updates):
    print("Request to access to the database...")
    mongo_recipes.update_one({'_id': document['_id']},{'$set': updates}, upsert=False)
    print("Succesfully updated document in the collection")
    pass
##-------------------------------------------------------------------------------
# Function to get a cursor with the whole content of the Database
def get_all_recipes_by_tag(tag):  
    print("Get all recipes with the tag "+tag)
    return mongo_recipes.find({'tags': tag })


##-------------------------------------------------------------------------------
# Function to get a cursor with the whole content of the Database
def get_all_recipes():  
    print("Get all recipes...")
    return mongo_recipes.find({})

def get_all_adapted_recipes():  
    print("Get all adapted recipes...")
    return mongo_adapted_recipes.find({})


#------------------------------------------------------------------------------
def get_all_tags():  
    print("Get all tags...")
    return mongo_tags.find({})

#-------------------------------------------------------------------------------
# With this function we can delete from the database the document in the parameter
def delete_document(document,adapted=False):
    print("Request to access to the database...")
    if adapted:
        mongo_adapted_recipes.delete_one(document)
    
    else:
        mongo_recipes.delete_one(document)
    print("Succesfully deleted document from collection")
    pass
#-------------------------------------------------------------------------------
# With this function we can get the size of the database in terms of the number
# of documents in the database
def get_number_documents():
    print("Request to query to the database...")
    return mongo_recipes.estimated_document_count()
    print("Succesfully processed size of the collection")

##-------------------------------------------------------------------------------
## Function to delete all the documents in the database. Util when we want to test
## the functionality of the database with not real params
#def delete_all_documents():
#    logger.info("Request to query to the database...")
#    mongoPrediction.delete_many({})
#    logger.info("Succesfully deleted all the content of the collection")
#    pass