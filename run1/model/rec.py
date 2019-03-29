## Noah Schumacher

'''
Reccomendation model for meals. Uses NMF to create
reccomendations for each user.
'''

## Initialization and imports
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pickle

from sklearn.decomposition import NMF

from db.python_db import run_sql_query


## Set random seed
np.random.seed(seed=14)



## Function to assign missing values to avg
def con_avg(x, avg):
	if x == 0:
		return avg
	return x
	

def nmf(X, mi=100, n=3, sol='cd'):
	model = NMF(max_iter=mi, n_components=n, solver=sol)

	W = np.round(model.fit_transform(X), 5) ## W matrix: has n hidden user topics
	H = np.round(model.components_, 5)      ## H matrix: has n hidden meal topics
	preds = np.round(np.dot(W, H), 3)		## Rating prediction matrix

	return (W, H, preds)


def get_mse(pred_df, cust_ratings):
	'''
	Params:
	--------
	- pred_df: pandas df object (cust_id=index, meal=cols)
	- train: pandas df with rows (cust_id, meal, rating)

	Returns:
	-------
	- Float: MSE of the predicted ratings
	'''
	dif = []
	for row_index in range(len(cust_ratings)):
		row = cust_ratings.iloc[row_index].values
		cust, meal, rating = row[0], row[1], row[2]
		pred = pred_df.loc[cust][meal]

		if pred > 5:
			pred = 5
		
		dif.append((rating - pred))


	dif = np.round(np.array(dif), 4)
	return np.mean(dif**2)


if __name__ == '__main__':
	## Selecting pre created table with rating info
	cust_ratings = pickle.load(open('run1/pickle/cust_ratingsDF.p', 'rb'))
	cust_ratings = cust_ratings[['cust_id', 'meal_name', 'meal_rating']]

	## Pivoting the table to get in format for ALS
	table = pd.pivot_table(cust_ratings,
					   values='meal_rating',
					   index=['cust_id'],
					   columns=['meal_name'],
					   fill_value=0)

	print("Pivoted")

	## Get avg ratings for meals
	avg = pickle.load(open('run1/pickle/avg_meal_ratingDF.p', 'rb'))

	## For each column get avg value and assign it to missing info
	for meal in table.columns:
		avg_val = avg.loc[avg['meal_name'] == meal, :].avg_meal_rating.values[0]
		table[meal] = table[meal].apply(con_avg, args=(avg_val,))
	
	X = np.round(table.values, 3)
	print("Got matrix")

	## NMF factorization and preds
	W, H, preds = nmf(X, 3)
	print("Got model, preds")

	## Convert preds back into user, meal dataframe.
	cols, inds = table.columns, table.index
	pred_df = pd.DataFrame(preds, index=inds, columns=cols)

	mse = get_mse(pred_df, cust_ratings)
	print(np.round(mse, 3))



