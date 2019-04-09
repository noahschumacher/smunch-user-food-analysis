'''
File:
	- Will allow for testing new meal, ingredients.
'''

import numpy as np
import pandas as pd
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

import multiprocessing
from functools import partial

import time

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
	"""
	obj: dict of userid->user class
	rows: iterable of dummy-encoded recipes
	"""

	rf_preds = []
	for key in objs.keys():
		u = objs[key]

		rf_preds.append(u.rf_model.predict(rows))

	return (rf_preds, len(objs.keys()))



## Getting user base breakdown
def user_percent(preds, n_m):
	counts = np.zeros(n_m)
	for i in range(len(preds)):
		sorts = np.argsort(preds[i])
		counts[sorts[-1]] += 1
	return np.round(np.array(counts)/sum(counts), 3)



def get_score(meals, user_objs, ing_ids, real):
	rows = get_rows(meals, ing_ids)

	start = time.time()
	rf_preds, num = get_preds(user_objs, rows)
	end = time.time()
	print("Time to get", num, "preds:", end-start)

	rf_percents = user_percent(rf_preds, 4)
	real_p = np.round(real/real.sum(), 3)

	print("RF Meal Percents:", rf_percents)
	print("\nAc Meal Percents:", real_p)

	rf_error = np.round(np.mean(np.abs((rf_percents - real_p))),3)
	avg_error = np.round(np.mean(np.abs((.25 - real_p))),3)

	print("\nRF error: ", rf_error)
	print("Avg error:", avg_error)

	return ([rf_error, avg_error], [rf_percents, real_p])


def plot_swarm(rf_resids, base_resids):
	## Converting residual information into dictionary for Swarm Plot
	length = len(rf_resids*4)
	models = ['Random Forest']*length + ['Base (.25)']*length
	meals = [1,2,3,4]*(len(rf_resids)*2)


	## Flattening and converting all residuals into lists
	rf_rs = list(np.array(np.matrix(rf_resids).ravel())[0])
	base_rs = list(np.array(np.matrix(base_resids).ravel())[0])

	rs = rf_rs + base_rs

	d = {'Model':models, 'Residual':rs, 'Meal':meals}
	df = pd.DataFrame(d)

	plt.figure(figsize=(8,4))
	sns.set_context("talk")
	sns.swarmplot(x="Residual", y="Model", data=df, size=6)

	plt.vlines(np.mean(rf_rs), .2, 1.8, linestyles='--', color='steelblue', label="Mean {0:.3f}".format(np.mean(rf_rs)))
	plt.vlines(np.mean(base_rs), .2, 1.8, linestyles='--', color='indianred', label="Mean {0:.3f}".format(np.mean(base_rs)))
	plt.vlines(0, -.25, 2.25, linestyles='--', color='darkorange', label="Perfect")

	plt.title("% Of Customer Base Residuals")
	plt.legend()
	plt.show()
	


if __name__ == '__main__':
	conn = connect()

	ing_df = pd.read_csv('data/ingrds.csv')

	start = time.time()
	user_objs = pickle.load(open('order_prediction/pickles/user_objects_deployable_dict.p', 'rb'))
	end = time.time()
	print("Time to read in user objs:", end-start)

	ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
	ing_ids = list(ing_dict.keys())
	ing_names = list(ing_dict.values())
	

	meal_groups = [['a050N00000zZg6AQAS','a050N00000zZg6BQAS','a050N00000zZgH1QAK','a050N00000zZgH5QAK'],
				   ['a050N00000za4nlQAA','a050N00000za4nqQAA','a050N00000za4nvQAA','a050N00000za4o5QAA'],
				   ['a050N000010W5ezQAC','a050N00000zZfyqQAC','a050N00000zZfyrQAC','a050N000010W5eyQAC'],
				   ['a050N00000zbFdeQAE','a050N00000zbGCDQA2','a050N00000zbFdjQAE','a050N00000zbFdZQAU'],
				   ['a050N00000zZgH2QAK','a050N00000zZgH4QAK','a050N00000zZgH3QAK','a050N00000zZgH7QAK'],
				   ['a050N00000zbES4QAM','a050N00000zbESJQA2','a050N00000zZfz8QAC','a050N00000zbESEQA2'],
				   ['a050N00000zZg5LQAS','a050N00000zZg5MQAS','a050N000010W5f1QAC','a050N000010W5f2QAC'],
				   ['a050N000013OpNUQA0','a050N000010WrWZQA0','a050N000010WrWAQA0','a050N000010WrWKQA0'],
				   ['a050N000010XyHYQA0','a050N000016uz5iQAA','a050N000010XyHCQA0','a050N000016uz5EQAQ'],
				   ['a050N000014zW24QAE','a050N00001C0K0fQAF','a050N00001C0K7rQAF','a050N000014zW1aQAE'],
				   ['a050N000010W5f8QAC','a050N000010W5f7QAC','a050N000010W5fAQAS','a050N000010W5f9QAC'],
				   ['a050N00000zbES4QAM','a050N00000zbESJQA2','a050N00000zZfz8QAC','a050N00000zbESEQA2'],
				   ['a050N00000zZg8AQAS','a050N000010WMcmQAG','a050N00000zZg8BQAS','a050N000010WMcrQAG']]

	real_ps_group = [np.array([26,23,16,10]), np.array([14,39,23,22]), np.array([42,26,47,71]),
					 np.array([49,50,77,23]), np.array([25,6,14,30]), np.array([19,26,33,81]),
					 np.array([71,21,13,5]), np.array([16,31,20,34]), np.array([25,38,43,15]),
					 np.array([41,47,18,15]), np.array([40,28,10,8]), np.array([21,56,54,104]),
					 np.array([71,40,56,28])]


	avg_rf_perror, avg_perror = [],[]
	rf_resids, base_resids = [], []
	for i in range(len(meal_groups)):
		print("\nSet:", i)
		ers, ps = get_score(meal_groups[i], user_objs, ing_ids, real_ps_group[i])

		avg_rf_perror.append(ers[0])
		avg_perror.append(ers[1])

		rf_resids.append(np.abs(ps[0]-ps[1]))
		base_resids.append(np.abs(.25-ps[1]))



	print("\n----------------\nFINAL AVG ERRORS:")
	means = [np.round(np.mean(avg_rf_perror), 3),
			 np.round(np.mean(avg_perror), 3)]

	print("RF error:", means[0])
	print("Avg error:", means[1])


	plot_swarm(rf_resids, base_resids)






