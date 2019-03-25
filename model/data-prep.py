## Noah Schumacher

'''
This file is used for:
1. Reading in the data
2. Performing cleaning operations
3. Creating master table in format
	user_id | ing1_id | ing2_id | ... | ingn_id
		n   |   .25   |  .33

4. Saving the fixed data as a pickle dataframe
'''

import numpy as np
import pandas as pd
import eda.python_db as db
import pickle


## Getting frequency for each user
def get_user_frequency(cust_meals_df, meal_ings, ingrds):
	customers = cust_meals_df.index

	master = {}

	count = 0
	## Looping through each customer
	for cust in customers[0:200]:
		## The customer meals they have ordered (with repeats)
		cust_meals = cust_meals_df.loc[cust].values[0]

		tot_meals = len(cust_meals)
		ingr_dic = {}

		## Looping through the meals for that customer
		for meal in cust_meals:

			## Checking if meal has ingredients (very small # of meals missing)
			if meal in meal_ings.index:
				ingrs = meal_ings.loc[meal].values[0]

				## Looping through ingredients and adding value if present
				for ing in ingrs:
					name = ingrds.loc[ingrds.ingredient_id == ing, :].name.values

					## Checking if the ingredient is present in ingredients table
					if len(name) != 0:
						name = name[0].lower()

						if name in ingr_dic:
							ingr_dic[name] += np.round(1/tot_meals,3)

						else:
							ingr_dic[name] = np.round(1/tot_meals,3)

		master[cust] = ingr_dic
		print("Percent Complete:", count/200)
		count += 1

	return customers, master


## Get set of all ingredients
def get_used_ingredients(dic):
	ings = [list(master[cust].keys()) for cust in dic]
	return set([item for sublist in ings for item in sublist])


## Create dataframe from masters and columns
def create_db(dic, cols):

	df = pd.DataFrame(columns=cols)
	for i, cust in enumerate(dic):

		row = []
		for ing in cols:
			if ing in dic[cust].keys():
				row.append(dic[cust][ing])
			else:
				row.append(0)


		df.loc[i] = row

	return df



if __name__ == '__main__':
	## Getting the data
	orders = pd.read_csv('data/orders.csv', index_col=0)
	meal_ingrds = pd.read_csv('data/meal_ingrds.csv', index_col=0)
	ingrds = pd.read_csv('data/ingrds.csv', index_col=0)


	## Creating orders dataframe with userid and list of meals ordered
	orders_grouped = pd.DataFrame(orders.groupby('cust_id')['meal_id'].apply(list))
	orders_grouped.columns = ['meals_ordered']


	## Grouping table for the meal ingredients
	meal_ingrds_grouped = pd.DataFrame(meal_ingrds.groupby('meal_id')['ingredient_id'].apply(list))
	meal_ingrds_grouped.columns = ['ingredients']


	customers, master = get_user_frequency(orders_grouped, meal_ingrds_grouped, ingrds)
	#print("\nMaster:\n", master)
	ingredients = get_used_ingredients(master)
	#print("\nIngredients:\n", ingredients)
	df = create_db(master, ingredients)
	df['cust_id'] = customers[0:200]

	pickle.dump(df, open('model/user_f_df.p', 'wb'))
	df = pickle.load(open('model/user_f_df.p', 'rb'))

	print("\nDF:\n", df)


