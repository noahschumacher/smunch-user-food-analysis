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

##### - eda3_rating.ipynb:
- Initial exploration of predicting meal rating based on ingredients ang general meal ratig breakdown.
- Avg Meal Rating: 3.73
- Meal Rating broken down by category (not significant differeces):
	- Chefchoice: 3.73
	- Livinglight: 3.67
	- Powerpick: 3.79
	- Freakyfit: 3.72


### model:
##### data-prep.py:
- Rudementary attempt to create ingredient frequency dataframe.
- File groups base tables customer_id and meal_id and then uses loops to go through every ingredient in every meal for each customer.
- Due to looping process ingredients with the same spelling and different capitalization are grouped together which is good.
- Runs very slowly (only using for a subset of data right now)
- Saves the dataframe as a pickle file

##### pred_cleaning.py:
- File reads in meal andn avg rating dataframe.
- Converts meal ID's to meal names
- combines small number of ingredients that are similar:
	1. If spelled the same with different capitalization combines them
	2. Uses stemming to combine same root
- Outputs:
	1. pickled feature matrix X (in models folder)
	2. pickled target values y (in models folder)

##### pred_rating.py:
- General file which does a grid search for both a Random Forrest and Gradient Boost Regressor Models. Best models are saved as pickle files.
- Models are comparable but the Random Forrest is much faster at fitting.
- Results:
	- Final RF MSE: 0.1581
	- Final GB MSE: 0.1682
- Random forrest model is slightly superior
- MSE of .158 means that on average the predicted rating is +- .397 stars from the true.
- Areas of possible concern:
	- For some runs the Test MSE is equal to or less than the Train MSE
	- Not a lot of data for fitting (only 657 meals with more than 5 ratings)



