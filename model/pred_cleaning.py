## Initialization and imports
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt

import pickle

## Function to run SQL query
from eda.python_db import run_sql_query

## Lemmatizing to merge similar ingredients
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

wordnet = WordNetLemmatizer()
snowball = SnowballStemmer('english')

## Set random seed
np.random.seed(seed=14)


## Mapping ingredients to names:
def map_name(ll):
    l = [ingrds.loc[ingrds.ingredient_id == id].name for id in ll]
    l = [wordnet.lemmatize(val.values[0].lower()) for val in l if len(val) != 0]  ## few ids dont have names
    return set(l)


## Get set of all ingredients used in meal
def get_ingredients(meal_ratings, ingredients_sets):
	## Getting all the ingredients used in meals
	ingredient_sets = meal_ratings.ingredient_names.tolist()

	## Getting set of all the ingredients present in meal
	ings = []
	for s in ingredient_sets:
	    for ing in s:
	        ings.append(ing)
	return set(ings)


## Create feature matrix and target values
def create_fandt(meal_ratings, ingredient_sets):

	## Creating the feature matrix and target
	X = np.zeros((len(ingredient_sets), len(ings)))
	y = np.array(meal_ratings.avg_meal_rating.tolist())

	for i, ingredients in enumerate(meal_ratings.ingredient_names.tolist()):
	    row = np.array([col in ingredients for col in ings]).astype(int)
	    X[i] = row

	return X, y



if __name__ == '__main__':

	## Getting tables from DB
	meal_ratings = run_sql_query("Select * from noah.meal_rating_ingredients")
	ingrds = run_sql_query("Select * from noah.ingredients")


	## Creating ingredient name column
	meal_ratings['ingredient_names'] = meal_ratings.ingredient_ids.apply(map_name)


	## Getting list of sets where each set is the ingredients used in meal meal
	ingredient_sets = meal_ratings.ingredient_names.tolist()

	## Set of all ingredients present
	ings = get_ingredients(meal_ratings, ingredient_sets)

	## Getting feature matrix and target values
	X, y = create_fandt(meal_ratings, ingredient_sets)
	pickle.dump(X, open('model/X_features.p', 'wb'))
	pickle.dump(y, open('model/y_target.p', 'wb'))







