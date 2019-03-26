## Notes as I work through Capstone

### data:
   - Where local csv files will love for eda and model training.


### eda:
##### - initial-sql.sql:
- File contains all used SQL queries
- Should make queries handle more of the work than they do (In pandas two groupbys could be converted in sql)

##### - python_db.py:
- File contains a function for querying Smunch DB and three base queries to get save data to CSV file locally.

##### - eda1.ipyb:
- Inital exploration of users, meals, ingredients
  - Total Users = 9838
  - Total Meals = 980
  - Total Ingredients = 1414 (unique sf ids but some are the same)
  - Total Meal Count = 256886

- Large portion of users have ordered only few times:
  - 21% have ordered 2 or less times
  - Might be beneficial to only look at users who have ordered over x amount of times

- Some ingredients are duplicated (have two or more sfids which are account for minor changes to the name of the ingredient).
  - Ex: "fried onion" and "friend onions" have different ids and counts associated with them.
- Some ingredients are very similar and should maybe be grouped together.
  - Ex: "lime" and "lime juice" , "pepper" and "pepper sauce"

##### - eda2_clustering.py:
- Initial exploration of clustering users based on ingredient frequency.
- Reading in pickled_df with customer_id and ingredients as features
	- vals are the frequency of presence in customers meals
- Two methods:
	1. kmeans:
		- Need standardized data.
		- Printing our food associated with each topic gives some insight into user clusters but still hard to define.
		- Sil score gives optimal number of clusters to be right around 5 depending on the data.
		- Only selecting some ingredients. Currently selecting ingredients to use as features based on how large the variance is. Idea here is that ingredients with larger variance will have more signal in food preferences.
	2. Hierarchial:
		- Not as easy to understand as Kmeans.
		- Need to explore different thresholds.
- Need to figure out how to utilize cluster information in next steps.


### model:
##### data-prep.py:
- Rudementary attempt to create ingredient frequency dataframe.
- File groups base tables customer_id and meal_id and then uses loops to go through every ingredient in every meal for each customer.
- Due to looping process ingredients with the same spelling and different capitalization are grouped together which is good.
- Runs very slowly (only using for a subset of data right now)
- Saves the dataframe as a pickle file

##### 