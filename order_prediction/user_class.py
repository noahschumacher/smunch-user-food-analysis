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
from sklearn.ensemble import RandomForestRegressor as RFReg
from sklearn.ensemble import GradientBoostingRegressor as GBReg


class User():

	## Build the user class with just the ID
	def __init__(self, user_id, account_id):
		self.user_id = user_id
		self.account_id = account_id


	######################################################
	#############    PUBLIC     #########################
	def build_table(self, conn, drop_tests=False):
		'''
		Function: Creates several object attributes:
			- meal_dict: dictionary with meal count and ingredient info
			- y: np array of the target values
			- ingredients: list of all ingredient ID's
			- ingredient_names: list of ingredient names
			- X: 2d numpy array (feature matrix)
		'''

		self._build_dictionary(conn, drop_tests)	## Create meal_id: meal_count dict attribute
		self._ingredients()  	## Create ingredients set attribute, Ingredient category set
		
		## Iterating through every meal and every ingredient.
		meals = list(self.meal_dict.keys())
		rows = []
		for meal in meals:

			meal_ings = self.meal_dict[meal]['ingredient_ids']
			row = np.array([ing in meal_ings for ing in self.ingredients]).astype(int)
			rows.append(row)

		self.X = np.vstack(rows)
		

	def build_model_test(self):

		# keeps = self._seen_ingredients()
		# X = self.X[:,keeps]
		X = self.X
		y = self.y

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1)


		
		################# AVG and BASE #############################
		avg_mse_test  = np.mean( (np.mean(y_train)-y_test)**2 )
		base_mse_test = np.mean( (.125-y_test)**2 )
		self.avg_mse = avg_mse_test
		self.base_mse = base_mse_test


		
		############## RANDOM FOREST ################################
		rf_model = RFReg(bootstrap=False, max_depth=10, max_features='sqrt',
						 min_samples_leaf=2, min_samples_split=2,
						 n_estimators=150, random_state=1)

		rf_model.fit(X_train, y_train)
		rf_preds = rf_model.predict(X_test)
		rf_mse_test   = np.mean( (rf_preds-y_test)**2 )

		self.rf_model = rf_model
		self.rf_preds = rf_preds
		self.rf_mse = rf_mse_test
		self.rf_precent_improvement = 100-(rf_mse_test/avg_mse_test)*100


		
		############## GRADIENT BOOST ###############################
		gb_model = GBReg(max_depth=3, min_samples_leaf=2, learning_rate=.01,
						 min_samples_split=2, n_estimators=80)

		gb_model.fit(X_train, y_train)
		gb_preds = gb_model.predict(X_test)
		gb_mse_test   = np.mean( (gb_preds-y_test)**2 )
		
		self.gb_model = gb_model
		self.gb_preds = gb_preds
		self.gb_mse = gb_mse_test
		self.gb_precent_improvement = 100-(gb_mse_test/avg_mse_test)*100


	## Build deployable models for actual use (RF bc better than GB)
	def build_model_deploy(self):
		'''
		Function:
		---------
		- Build deployable user model (no train/test split).
		- Uses Random Forrest model.
		- Assigns model object to self.rf_model
		'''

		X, y = self.X, self.y

		## RANDOM FOREST
		rf_model = RFReg(bootstrap=False, max_depth=10, max_features='sqrt',
						 min_samples_leaf=2, min_samples_split=2,
						 n_estimators=150, random_state=1)

		rf_model.fit(X, y)
		self.rf_model = rf_model


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


	def _build_dictionary(self, conn, drop_tests=True):
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
		SELECT * FROM noah.user_order_count
		WHERE contact_sfid = '%s' '''%self.user_id

		Q2 = '''
		WITH offered AS(
			SELECT product_sfid as meal_id
			FROM bi.executed_order_employee
			WHERE contact_account_sfid = '%s' and delivery_timestamp IN (
				SELECT delivery_timestamp as deliv_tmstmp
				FROM bi.executed_order_employee
				WHERE contact_sfid = '%s' and order_type = 'single')
			GROUP BY product_sfid, delivery_timestamp),

		ingredients AS(
			SELECT meal_id, ingredient_ids
			FROM noah.meal_rating_ingredients)
			
		SELECT offered.meal_id, COUNT(offered.meal_id) as offered_count, ingredients.ingredient_ids
		FROM offered
		LEFT JOIN ingredients
		ON offered.meal_id = ingredients.meal_id
		WHERE ingredients.ingredient_ids IS NOT NULL
		GROUP BY offered.meal_id, ingredients.ingredient_ids'''%(self.account_id, self.user_id)


		df1 = run_sql_query(Q1, conn)	## Table with users order history
		df2 = run_sql_query(Q2, conn)	## Table with count of offered meals
		

		df = pd.merge(df1, df2, how='right', on='meal_id')	## Merging on meal_id
		df['contact_sfid'] = self.user_id					## Filling in user_id
		df.fillna(0, inplace=True)							## Fill NaN's with 0
		df.set_index('meal_id', inplace=True)				## Setting meal_id as index

		## Test_meals
		test_meals = np.array(['a050N00000zZg6AQAS','a050N00000zZg6BQAS','a050N00000zZgH1QAK','a050N00000zZgH5QAK',
				   'a050N00000za4nlQAA','a050N00000za4nqQAA','a050N00000za4nvQAA','a050N00000za4o5QAA',
				   'a050N000010W5ezQAC','a050N00000zZfyqQAC','a050N00000zZfyrQAC','a050N000010W5eyQAC',
				   'a050N00000zbFdeQAE','a050N00000zbGCDQA2','a050N00000zbFdjQAE','a050N00000zbFdZQAU',
				   'a050N00000zZgH2QAK','a050N00000zZgH4QAK','a050N00000zZgH3QAK','a050N00000zZgH7QAK',
				   'a050N00000zbES4QAM','a050N00000zbESJQA2','a050N00000zZfz8QAC','a050N00000zbESEQA2',
				   'a050N00000zZg5LQAS','a050N00000zZg5MQAS','a050N000010W5f1QAC','a050N000010W5f2QAC',
				   'a050N000013OpNUQA0','a050N000010WrWZQA0','a050N000010WrWAQA0','a050N000010WrWKQA0',
				   'a050N000010XyHYQA0','a050N000016uz5iQAA','a050N000010XyHCQA0','a050N000016uz5EQAQ',
				   'a050N000014zW24QAE','a050N00001C0K0fQAF','a050N00001C0K7rQAF','a050N000014zW1aQAE',
				   'a050N000010W5f8QAC','a050N000010W5f7QAC','a050N000010W5fAQAS','a050N000010W5f9QAC',
				   'a050N00000zbES4QAM','a050N00000zbESJQA2','a050N00000zZfz8QAC','a050N00000zbESEQA2',
				   'a050N00000zZg8AQAS','a050N000010WMcmQAG','a050N00000zZg8BQAS','a050N000010WMcrQAG'])

		## Drop tests meals paramters
		if drop_tests:
			## Checking if test meal has been seen by user (removing if not)
			test_meals = test_meals[[meal in df.index.values for meal in test_meals]]
			df.drop(test_meals, inplace=True)

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


