'''
File:
	- Will allow for testing new meal, ingredients.
'''

import numpy as np
import pandas as pd
import pickle

ing_df = pd.read_csv('data/ingrds.csv')

ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
ing_ids = list(ing_dict.keys())
ing_names = list(ing_dict.values())


meal_ing_ids1 = np.random.choice(ing_ids, size=10, replace=False)
meal_ing_ids2 = np.random.choice(ing_ids, size=10, replace=False)

meal_ing_names1 = [ing_dict[key] for key in meal_ing_ids1]
meal_ing_names2 = [ing_dict[key] for key in meal_ing_ids2]

print(meal_ing_names1)
print(meal_ing_names2)

## New Meal Rows
row1 = np.array([ing in meal_ing_ids1 for ing in ing_ids]).astype(int)
row2 = np.array([ing in meal_ing_ids2 for ing in ing_ids]).astype(int)

rows = np.row_stack((row1,row2))

user_objs = pickle.load(open('order_prediction/user_objects_dict.p', 'rb'))

rf_preds = []
gb_preds = []
for key in user_objs.keys():
	u = user_objs[key]

	rf_preds.append(u.rf_model.predict(rows))
	gb_preds.append(u.gb_model.predict(rows))

pref1, pref2 = 0, 0
for i in range(len(rf_preds)):
	rfp = rf_preds[i]
	gbp = gb_preds[i]

	if rfp[0] > rfp[1]:
		pref1 += 1
	else:
		pref2 += 1

	print("       Meal 1  |  Meal 2")
	print("RF:", rf_preds[i])
	print("GB:", gb_preds[i])
	print()

print("{0:2.2f}% for Meal1, {1:2.2f}% for Meal2".format((pref1/len(rf_preds))*100, (pref2/len(rf_preds))*100))

rf_preds = np.matrix(rf_preds)
gb_preds = np.matrix(gb_preds)

print("RF Avg Scores:", np.mean(rf_preds, axis=0))
print("GB Avg Scores:", np.mean(gb_preds, axis=0))
