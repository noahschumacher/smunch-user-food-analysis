'''
File:
	- Defines a Smunch User class.
	- build_table method:
		- builds the user class with all info required for
		predicting prob a user will order a dish given the
		ingredients present in the dish.
'''

import numpy as np
import pandas as pd

## local run sql file
from db.python_db import connect, run_sql_query

## sklearn models and validation
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


class User():

	## Build the user class with just the ID
	def __init__(self, user_id, account_id):
		self.user_id = user_id
		self.account_id = account_id


	######################################################
	#############    PUBLIC     #########################
	def build_table(self, conn):
		'''
		Function: Creates several object attributes:
			- meal_dict: dictionary with meal count and ingredient info
			- y: np array of the target values
			- ingredients: list of all ingredient ID's
			- ingredient_names: list of ingredient names
			- X: 2d numpy array (feature matrix)
		'''

		self._build_dictionary(conn)	## Create meal_id: meal_count dict attribute
		self._ingredients()  	## Create ingredients set attribute, Ingredient category set
		
		## Iterating through every meal and every ingredient.
		meals = list(self.meal_dict.keys())
		rows = []
		for meal in meals:

			meal_ings = self.meal_dict[meal]['ingredient_ids']
			row = np.array([ing in meal_ings for ing in self.ingredients]).astype(int)
			rows.append(row)

		self.X = np.vstack(rows)
		

	def build_model(self):

		keeps = self._seen_ingredients()
		X = self.X[:,keeps]
		y = self.y

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

		rf_model = RandomForestRegressor(bootstrap = False,
										 max_depth = 10,
										 max_features = 'sqrt',
										 min_samples_leaf = 2,
										 min_samples_split = 2,
										 n_estimators = 150,
										 random_state = 1)

		rf_model.fit(X_train, y_train)
		rf_preds = rf_model.predict(X_test)
		rf_mse_test = np.mean( (rf_preds-y_test)**2 )
		avg_mse_test = np.mean( (np.mean(y_train)-y_test)**2 )
		base_mse_test = np.mean( (.25-y_test)**2 )

		self.model = rf_model
		self.preds = rf_preds
		self.mse = rf_mse_test
		self.avg_mse = avg_mse_test
		self.base_mse = base_mse_test
		self.precent_improvement = percent = 100-(rf_mse_test/avg_mse_test)*100


	######################################################
	#############    PRIVATE     #########################

	def _ingredients(self):
		'''
		Function: Gets the unique ingredients shown
		to a user.
		'''
		df = pd.read_csv('data/ingrds.csv')
	
		self.ingredients = list(df.ingredient_id.values)
		self.ingredient_name = list(set(df.name.values))


	def _build_dictionary(self, conn):
		'''
		Function: Builds the users meal dictionary.
		- Format:
			{meal1:
				{
					count: n,
					ingredients: [ing1, ing2, ..., ingn],
					ingredient_cats: [cat1, cat2, ..., catn]
				 }
			meal2: ...
			}

		Return:
		-------
		- 2D numpy array with data
		'''
		Q1 = '''
		SELECT * FROM noah.user_order_ingredients
		WHERE contact_sfid = '%s' '''%self.user_id

		Q2 = '''
		WITH t1 AS(
			SELECT product_sfid as meal_id
			FROM bi.executed_order_employee
			WHERE contact_account_sfid = '%s' and delivery_timestamp IN (
				SELECT delivery_timestamp as deliv_tmstmp
				FROM bi.executed_order_employee
				WHERE contact_sfid = '%s' and order_type = 'single')
			GROUP BY product_sfid, delivery_timestamp)

		SELECT meal_id, COUNT(meal_id) as offered_count
		FROM t1
		GROUP BY meal_id'''%(self.account_id, self.user_id)


		df1 = run_sql_query(Q1, conn)	## Table with users order history
		df2 = run_sql_query(Q2, conn)	## Table with count of offered meals

		df = pd.merge(df1, df2, how='left', on='meal_id')	## Merging on meal_id
		df.set_index('meal_id', inplace=True)				## Setting meal_id as index
		df.dropna(inplace=True)								## Drop rare NaN rows


		## Creating target with smoothing factor of .25
		df['order_f'] = np.round(df['meal_count']/ (df['offered_count']+.25), 3)

		## Drop row where ordered>offered (issue with db accounts)
		df = df.loc[df.order_f < 1, :]

		self.y = df.order_f.values
		self.meal_dict = df.to_dict('index')



	## Function gives list of ingredients user as has seen (remove never seen ingrds)
	def _seen_ingredients(self):
	    rows, cols = self.X.shape
	    keeps = []
	    for i in range(cols):
	        if (self.X[:,i] == 1).sum() != 0:
	            keeps.append(i)
	            
	    return keeps



# conn = connect()
# print("Connected")
# user_id = '0030N00002LQqB9QAL'
# account_id = '0010N00004IaGG6QAN'
# u1 = User(user_id, account_id, conn)
# u1.build_table()


