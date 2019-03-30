## This file creates a user object and get relevant
## for creating a model.

import numpy as np
import pandas as pd

from db.python_db import run_sql_query


class User():

	## Build the user class with just the ID
	def __init__(self, user_id):
		self.user_id = user_id


	def build_table(self):
		'''
		Function: Creates several object attributes:
			- meal_dict: dictionary with meal count and ingredient info
			- y: np array of the target values
			- ingredients: list of all ingredient ID's
			- ingredient_names: list of ingredient names
			- X: 2d numpy array (feature matrix)
		'''

		self.build_dictionary()	## Create meal_id: meal_count dict attribute
		self._ingredients()  	## Create ingredients set attribute, Ingredient category set
		
		## Iterating through every meal and every ingredient.
		meals = list(self.meal_dict.keys())
		rows = []
		for meal in meals:

			row = []
			for ing in self.ingredients:

				if ing in self.meal_dict[meal]['ingredient_ids']:
					row.append(1)
				else:
					row.append(0)

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


	def build_dictionary(self):
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
		Q = '''
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

		df = run_sql_query(Q)
		df.set_index('meal_id', inplace=True)
		self.y = df.meal_count.values
		self.meal_dict =  df.to_dict('index')




user_id = '0030N00002LQqB9QAL'
u1 = User(user_id)
u1.build_table()


