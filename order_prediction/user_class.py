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


class User():

	## Build the user class with just the ID
	def __init__(self, user_id, account_id, connection):
		self.user_id = user_id
		self.account_id = account_id
		self.connection = connection


	def build_table(self):
		'''
		Function: Creates several object attributes:
			- meal_dict: dictionary with meal count and ingredient info
			- y: np array of the target values
			- ingredients: list of all ingredient ID's
			- ingredient_names: list of ingredient names
			- X: 2d numpy array (feature matrix)
		'''

		self._build_dictionary()	## Create meal_id: meal_count dict attribute
		self._ingredients()  	## Create ingredients set attribute, Ingredient category set
		
		## Iterating through every meal and every ingredient.
		meals = list(self.meal_dict.keys())
		rows = []
		for meal in meals:

			meal_ings = self.meal_dict[meal]['ingredient_ids']
			row = np.array([ing in meal_ings for ing in self.ingredients]).astype(int)
			rows.append(row)

		self.X = np.vstack(rows)
		

	def _ingredients(self):
		'''
		Function: Gets the unique ingredients shown
		to a user.
		'''
		df = pd.read_csv('run1/data/ingrds.csv')
	
		self.ingredients = list(df.ingredient_id.values)
		self.ingredient_name = list(set(df.name.values))


	def _build_dictionary(self):
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
		WITH t1 as
			(SELECT product_sfid as meal_id, COUNT(product_sfid) as meal_count
			FROM bi.executed_order_employee
			WHERE contact_sfid = '%s'
			GROUP BY product_sfid),
				
		t2 as
			(SELECT product__c as meal_id, ARRAY_AGG(ingredient__c) as ingredient_ids
			FROM salesforce.product_ingredient__c
			GROUP BY product__c)

		SELECT t1.meal_id, t1.meal_count, t2.ingredient_ids FROM t1
		LEFT JOIN t2
		ON t1.meal_id = t2.meal_id
		WHERE t2.ingredient_ids IS NOT NULL'''%self.user_id

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


		df1 = run_sql_query(Q1, self.connection)	## Table with users order history
		df2 = run_sql_query(Q2, self.connection)	## Table with count of offered meals

		df = pd.merge(df1, df2, how='left', on='meal_id')
		df.set_index('meal_id', inplace=True)

		df.dropna(inplace=True)

		df['order_f'] = df['meal_count']/df['offered_count']

		self.y = df.order_f.values
		self.meal_dict =  df.to_dict('index')



# conn = connect()
# print("Connected")
# user_id = '0030N00002LQqB9QAL'
# account_id = '0010N00004IaGG6QAN'
# u1 = User(user_id, account_id, conn)
# u1.build_table()


