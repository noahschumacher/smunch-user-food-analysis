'''
File:
	- Will allow for testing new meal, ingredients.
'''

import numpy as np
import pandas as pd
import pickle

## local run sql file
from db.python_db import connect, run_sql_query



def get_rows(meals, ing_ids):

	## Getting list of list of ingredients in meal
	ingr_l = []
	for meal in meals:

		Q = '''
		SELECT ingredient_ids
		FROM noah.meal_rating_ingredients
		WHERE meal_id='%s' '''%meal[0]

		df = run_sql_query(Q, conn )
		ingr_l.append(df.values[0][0])

	## converting each meal to feature space row
	rows  = []
	for ings in ingr_l:
		rows.append( np.array([ing in ings for ing in ing_ids]).astype(int) )

	return np.vstack(rows)


## Predicting meal consistency for all users
def get_preds(objs, rows):

	rf_preds = []
	gb_preds = []
	for key in objs.keys():
		u = objs[key]

		rf_preds.append(u.rf_model.predict(rows))
		gb_preds.append(u.gb_model.predict(rows))

	return (rf_preds, gb_preds)


## Getting user base breakdown
def user_percent(preds, n_m):
	counts = np.zeros(n_m)
	for i in range(len(preds)):
		sorts = np.argsort(preds[i])
		counts[sorts[-1]] += 1
	return np.round(np.array(counts)/sum(counts), 3)


if __name__ == '__main__':
	conn = connect()

	ing_df = pd.read_csv('data/ingrds.csv')
	user_objs = pickle.load(open('order_prediction/user_objects_dict.p', 'rb'))

	ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
	ing_ids = list(ing_dict.keys())
	ing_names = list(ing_dict.values())
		
	real = np.array([26,23,16,10])

	meals = [('a050N00000zZg6AQAS',5,'0010N00004DQyrXQAT'),
		 	 ('a050N00000zZg6BQAS',8,'0010N00004DQyrXQAT'),
		 	 ('a050N00000zZgH1QAK',4,'0010N00004DQyrXQAT'),
		 	 ('a050N00000zZgH5QAK',3,'0010N00004DQyrXQAT')]

	rows = get_rows(meals, ing_ids)
	rf_preds, gb_preds = get_preds(user_objs, rows)

	rf_percents = user_percent(rf_preds, 4)
	gb_percents = user_percent(gb_preds, 4)
	real_p = np.round(real/real.sum(), 3)

	print("RF Meal Percents:", rf_percents)
	print("GB Meal Percents:", gb_percents)
	print("\nAc Meal Percents:", real_p)

	rf_error = np.mean(np.abs((rf_percents - real_p)))
	gb_error = np.mean(np.abs((gb_percents - real_p)))
	print("\nRF error:", rf_error, "GB error:", gb_error)


