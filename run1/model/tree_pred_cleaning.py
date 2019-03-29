## Initialization and imports
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt

import pickle

## Function to run SQL query
from db.python_db import run_sql_query

## Lemmatizing to merge similar ingredients
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

wordnet = WordNetLemmatizer()
snowball = SnowballStemmer('english')

## Set random seed
np.random.seed(seed=14)


## Mapping ingredients to names:
def map_name(ll):
	'''
	Function: Maps ingredient ID column in DF to
	ingredient names. Lemmatizes names to combine similar
	ingredients.

	Params:
	-------
	- ll: list of ingredient ids

	Returns:
	-------
	- set of unique ingredients names in meal
	'''

	l = [ingrds.loc[ingrds.ingredient_id == id].name for id in ll]
	l = [wordnet.lemmatize(val.values[0].lower()) for val in l if len(val) != 0]  ## few ids dont have names
	return set(l)


## Get set of all ingredients used in meal
def get_ingredients(meal_ratings):
	'''
	Params:
	-------
	- meal_ratings: pandas df with meal_id, name, rating, ingredients

	Returns:
	-------
	- list of unique ingredients present in meals
	'''

	## Getting all the ingredients used in meals
	ingredient_sets = meal_ratings.ingredient_names.tolist()

	## Getting set of all the ingredients present in meal
	ings = []
	for s in ingredient_sets:
		for ing in s:
			ings.append(ing)
	return list(set(ings))


## Create feature matrix and target values
def create_fandt(meal_ratings, ingredient_sets, ings):
	'''
	Params:
	-------
	- meal_ratings: pandas df with meal_id, name, rating, ingredients
	- ingredients_sets: list of sets (each set is inngredients present in meal)
	- ings: list of unique ingredients

	Returns:
	-------
	- X: 2d numpy feature matrix (row=meal, cols=ingredients)
	- y: 1d numpy array of target values (meal ratigs)
	'''

	## Creating the feature matrix and target
	X = np.zeros((len(ingredient_sets), len(ings)))		# (num meals x num ingredients)
	y = np.array(meal_ratings.avg_meal_rating.tolist())

	for i, ingredients in enumerate(ingredient_sets):
	    row = np.array([col in ingredients for col in ings]).astype(int)
	    X[i] = row

	return X, y


## Create feature matrix and target values
def create_fandt_mapped(meal_ratings, num_meals, num_ings, cat_map):
	'''
	Params:
	-------
	- meal_ratings: pandas df with meal_id, name, rating, ingredients
	- num_meals: number of meals in training data
	- num_ings: number of ingredient categories
	- cat_map: dictionary with categories as keys and list of foods as values

	Returns:
	-------
	- X: 2d numpy feature matrix (row=meal, cols=ingredients)
	- y: 1d numpy array of target values (meal ratigs)
	'''

	categories = list(cat_map.keys())

	## Creating the feature matrix and target
	X = np.zeros((num_meals, num_ings))
	y = np.array(meal_ratings.avg_meal_rating.tolist())

	## Going through set of ingredients in each meal
	for i, ingredients in enumerate(meal_ratings.ingredient_names.tolist()):
		row = []	## single meal inngredients row
		
		## it through ing cat:
		##  	- append 1 if a ingredient in the meal is part of cat
		## 		- append 0 if no ingredients in meal are in cat
		for cat in categories:

			## Going through meals ingredients
			for ing in ingredients:

				inside = False	## False if not in cat
				if ing in cat_map[cat]:
					row.append(1)
					inside = True
					break		## If found in cat break out

			if not inside: row.append(0)

		## Done with that meal and append the row
		X[i] = np.array(row)

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
	ings = get_ingredients(meal_ratings)

	## Getting dictionary of ingredient groups
	cats = pd.read_csv('data/ing_to_cat.csv')
	cat_map = cats.groupby('category')['ing'].apply(list).to_dict()
	ing_map = cats.groupby('ing')['category'].apply(list).to_dict()


	all = input("Use all ingredients? (y/n)")

	if all=='y':
		## USE ENTIRE INGREDIENT LIST (NO MAPPING)
		X, y = create_fandt(meal_ratings,
						 	ingredient_sets,
							ings)

	else:
		## USE MAPPED INGREDIENTS LIST
		X, y = create_fandt_mapped(meal_ratings,
								   len(ingredient_sets),
								   len(cat_map.keys()),
								   cat_map)


	pickle.dump(list(ing_map.keys()), open('run1/pickle/feature_cols.p', 'wb'))
	pickle.dump(X, open('run1/pickle/X_features.p', 'wb'))
	pickle.dump(y, open('run1/pickle/y_target.p', 'wb'))







