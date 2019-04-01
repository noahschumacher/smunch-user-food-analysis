'''
This file:
	- Analyzes the set meal categories:
		1. Animal Protien
		2. Vegetarian
		3. Vegan
	- Used in compliment with the clustering (inspection)
	- 3D plot of:
		- X: Frequency of time user orders Vegan meal
		- Y: Frequency of time user orders Vegetarian meal
		- Z: Frequency of time user orders Animal Protien meal
'''

## Initialization and imports
import pandas as pd 
import numpy as np
from collections import Counter

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

import seaborn as sns

## Changing directory to top folder (All programs run from top)
import os
os.chdir('/Users/nschumacher/docs/galvanize/smunch-user-food-analysis')

## local run sql file
from db.python_db import run_sql_query

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage


## Set random seed
np.random.seed(seed=14)

meal_cat = run_sql_query("SELECT * FROM bi.dish_profiles_static")

q = '''
SELECT contact_sfid as user_id, ARRAY_AGG(product_sfid) as product_sfids
FROM bi.executed_order_employee
WHERE order_type = 'single'
GROUP BY contact_sfid'''

user_meals_df = run_sql_query(q)


meal_cat.set_index('product_sfid', inplace=True)
user_meals_df.set_index('user_id', inplace=True)


## Dictionary with meal id as key and type as value
meal_dict = meal_cat['type'].to_dict()

## Adding a meal count column so cann drop users with not enough meals
user_meals_df['meal_count'] = user_meals_df['product_sfids'].str.len()

## Drop customers with less than x orders
user_meals_df = user_meals_df[user_meals_df['meal_count'] > 30]

print("Left with {0} users.".format(user_meals_df.shape[0]))


## Convert meal_ids to their categories
def convert_product_ids(ids, meal_dict):
	categories = []
	for idd in ids:
		if idd in meal_dict.keys():
			categories.append(meal_dict[idd])
	
	counts = Counter(categories)
	return (counts['Vegan'], counts['Vegetarian'], counts['Animal protein'])


user_cat_counts = user_meals_df['product_sfids'].apply(convert_product_ids, args=(meal_dict,))
user_cat_counts = pd.DataFrame(user_cat_counts)

## expand df.tags into its own dataframe
tags = user_cat_counts['product_sfids'].apply(pd.Series)
tags.rename(columns={0:'vegan', 1:'vegetarian', 2:'animal'}, inplace=True)

## This drop drops customers who have never ordered a classified meal
tags.dropna(axis=0, inplace=True)

## Add a total categorized meals column
tags['total'] = tags.sum(axis=1)

## Print out some stats
print("Only meat eaters: {0:2.2f}%".format(np.mean((tags.vegan == 0) & (tags.vegetarian==0))*100))
print("Only Vegan: {0:2.2f}%".format(np.mean((tags.animal == 0) & (tags.vegetarian==0))*100))
print("Vegan or Vegatarian: {0:2.2f}%".format(np.mean((tags.animal == 0))*100))

## Getting frequency of each category
cols = ['vegan', 'vegetarian', 'animal']
for col in cols:
	tags[col] = (tags[col] / tags['total'])

## Scatter Matrix
tags.dropna(axis=0, inplace=True)
sns_plot = sns.pairplot(tags)
sns_plot.savefig("images/user_categories.jpg")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(tags.vegan, tags.vegetarian, tags.animal, c='b', marker='o')

ax.set_title("User Meal Category")
ax.set_xlabel('Vegan Frequency')
ax.set_ylabel('Vegetarian Frequency')
ax.set_zlabel('Animal Frequency')
plt.savefig("images/user_cat_3d.jpg")
plt.show()













