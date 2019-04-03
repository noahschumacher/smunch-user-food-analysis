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
		WHERE meal_id='%s' '''%meal

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


def get_score(meals, user_objs, ing_ids, real):
	rows = get_rows(meals, ing_ids)
	rf_preds, gb_preds = get_preds(user_objs, rows)

	rf_percents = user_percent(rf_preds, 4)
	gb_percents = user_percent(gb_preds, 4)
	real_p = np.round(real/real.sum(), 3)

	print("RF Meal Percents:", rf_percents)
	print("GB Meal Percents:", gb_percents)
	print("\nAc Meal Percents:", real_p)

	rf_error = np.round(np.mean(np.abs((rf_percents - real_p))),3)
	gb_error = np.round(np.mean(np.abs((gb_percents - real_p))),3)
	avg_error = np.round(np.mean(np.abs((.25 - real_p))),3)
	print("\nRF error: ", rf_error)
	print("GB error: ", gb_error)
	print("Avg error:", avg_error)

	return rf_error, gb_error, avg_error


if __name__ == '__main__':
	conn = connect()

	ing_df = pd.read_csv('data/ingrds.csv')
	user_objs = pickle.load(open('order_prediction/user_objects_dict.p', 'rb'))

	ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
	ing_ids = list(ing_dict.keys())
	ing_names = list(ing_dict.values())
	
	avg_rf_perror = []
	avg_gb_perror = []
	avg_perror = []

	real = np.array([26,23,16,10])
	meals = ['a050N00000zZg6AQAS','a050N00000zZg6BQAS',
			 'a050N00000zZgH1QAK','a050N00000zZgH5QAK']

	print("Set 1:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])


	real = np.array([14,39,23,22])
	meals = ['a050N00000za4nlQAA','a050N00000za4nqQAA',
			 'a050N00000za4nvQAA','a050N00000za4o5QAA']
	
	print("\nSet 2:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])



	real = np.array([42,26,47,71])
	meals = ['a050N000010W5ezQAC','a050N00000zZfyqQAC',
			 'a050N00000zZfyrQAC','a050N000010W5eyQAC']
	
	print("\nSet 3:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])


	real = np.array([49,50,77,23])
	meals = ['a050N00000zbFdeQAE','a050N00000zbGCDQA2',
			 'a050N00000zbFdjQAE','a050N00000zbFdZQAU']
	
	print("\nSet 4:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])


	real = np.array([25,6,14,30])
	meals = ['a050N00000zZgH2QAK','a050N00000zZgH4QAK',
			 'a050N00000zZgH3QAK','a050N00000zZgH7QAK']
	
	print("\nSet 5:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])



	real = np.array([19,26,33,81])
	meals = ['a050N00000zbES4QAM','a050N00000zbESJQA2',
			 'a050N00000zZfz8QAC','a050N00000zbESEQA2']
	
	print("\nSet 6:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])


	real = np.array([71,21,13,5])
	meals = ['a050N00000zZg5LQAS','a050N00000zZg5MQAS',
			 'a050N000010W5f1QAC','a050N000010W5f2QAC']
	
	print("\nSet 7:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])


	real = np.array([11,30,18,23])
	meals = ['a050N000010XxrMQAS','a050N000010XxrgQAC',
			 'a050N000010XxrvQAC','a050N000010XxfVQAS']
	
	print("\nSet 8:")
	ers = get_score(meals, user_objs, ing_ids, real)
	avg_rf_perror.append(ers[0])
	avg_gb_perror.append(ers[1])
	avg_perror.append(ers[2])

	print("\n----------------\nFINAL AVG ERRORS:")
	print("RF error:", np.round(np.mean(avg_rf_perror), 3))
	print("GB error:", np.round(np.mean(avg_gb_perror), 3))
	print("Avg error:", np.round(np.mean(avg_perror), 3))






