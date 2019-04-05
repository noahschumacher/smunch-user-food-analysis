'''
File:
	- Will allow for testing new meal, ingredients.
'''

import numpy as np
import pandas as pd
import pickle

def create_rows(meals, ing_ids):

	rows = []
	for meal in meals:
		ings = meal.ingredients
		rows.append( np.array([ing in new_ings for ing in ing_ids]).astype(int) )

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
	counts = np.zeros(n_m)
	for i in range(len(preds)):
		sorts = np.argsort(preds[i])
		counts[sorts[-1]] += 1
	return np.round(np.array(counts)/sum(counts), 3)


## Run the functions
def get_customer_percents(ing_dict, ing_ids, ing_names, user_objs, meals):
	rows = create_rows(meals, ing_ids)
	preds = get_preds(user_objs, rows)
	user_percents = user_percent(preds, len(meals))

	return user_percent


# ing_df = pd.read_csv('data/ingrds.csv')
# ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
# ing_ids = list(ing_dict.keys())
# ing_names = list(ing_dict.values())

# user_objs = pickle.load(open('order_prediction/user_objects_deployable_dict.p', 'rb'))





