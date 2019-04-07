'''
File:
	- Will allow for testing new meal, ingredients.
'''

import numpy as np
import pandas as pd
import pickle
import math

import time

def create_rows(meals, ing_ids):
	'''
	Function:
	- creates the feature rows to be used in the model

	Params:
	------
	- meals: list of lists where each inner list is a meal
	and the values are the ingredients in the meal
	- ing_ids: total list of ingredients in Smunch DB

	Returns:
	-------
	- numpy 2D array of the feature rows (rows = n meals, cols = n tot ings)
	'''

	rows = []
	for meal in meals.keys():
		meal_ings = meals[meal]

		## Removing missing values caused by different length ingredients
		meal_ings = [ing for ing in meal_ings if type(ing)==type('a')]

		row = np.array([ing in meal_ings for ing in ing_ids]).astype(int)
		rows.append(row)

	## converting each meal to feature space row
	return np.vstack(rows)


## Predicting meal consistency for all users
def get_preds(objs, rows):

	rf_preds = []
	for key in objs.keys():
		u = objs[key]
		rf_preds.append(u.rf_model.predict(rows))

	return rf_preds


## Getting user base breakdown
def user_percent(preds, n_m):
	'''
	Function:
	- Breaks down customer choices in % of total customers

	Params:
	------
	- preds: 2d list of C-Score for each meal for each user
	- n_m: int, number of meals

	Returns:
	------
	- numpy 1d array with customer percents for each meal.
	'''

	counts = np.zeros(n_m)
	for i in range(len(preds)):
		sorts = np.argsort(preds[i])
		counts[sorts[-1]] += 1

	return np.round(np.array(counts)/sum(counts), 3)


## Run the functions
def get_customer_percents(meal_ings_dict, tot_ingredient_ids, user_objs):
	'''
	Params:
	-------
	- meal_ingredients_l: dictionary of meal_id as key and values=list of ingrs
	- tot_ingredient_ids: list of all ingredient ids in Smunch DB
	- user_objs: dictionary with (key=user_id, val=user_object)

	Returns:
	------
	- Numpy array with len n number of meals being compared
	'''

	rows = create_rows(meal_ings_dict, tot_ingredient_ids)
	preds = get_preds(user_objs, rows)
	user_percents = user_percent(preds, len(meal_ings_dict))

	return user_percents



def run():
	## Smunch Ingredient Info
	ing_df = pd.read_csv('data/ingrds.csv')
	ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
	ing_ids = list(ing_dict.keys())
	ing_names = list(ing_dict.values())

	## Getting the user objects
	user_objs = pickle.load(open('order_prediction/user_objects_test_dict.p', 'rb'))

	start = time.time()
	## Reading in meals to compare to
	meals = pd.read_csv('website/test_csvs/meal_comp1.csv')
	meals.drop(['Unnamed: 0', 'Meals'], axis=1, inplace=True)
	meals_d = meals.to_dict(orient='list')


	print(get_customer_percents(meals_d, ing_ids, user_objs))
	end = time.time()
	print("Tot Time:", end-start)


run()





