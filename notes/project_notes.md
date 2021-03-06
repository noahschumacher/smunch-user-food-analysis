## Notes as I work through Capstone


### data:
   - Where local csv files will love for eda and model training.


### db:
##### python_db.py:
- File contains a function for querying Smunch DB and three base queries to get save data to CSV file locally.

##### initial-sql.sql:
- File contains all used SQL queries
- Should make queries handle more of the work than they do (In pandas two groupbys could be converted in sql)


### eda:
##### eda1.ipyb:
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

##### eda2_clustering.py:
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
- Second iteration:
	- Converted specific igredients to more generalized categories by hand. File in data folder (private).
	- This allows for clearer insight into the clusters.
	- Identifiable clusters include:
		- Vegan
		- Lighter Meals (seafood, asian)
		- Heavyer / Unhealthier meals (meat, cheese, egg, mayo, etc)
	- kmeans clusters seem more reasonable than hierarchial clustering.

##### eda3_rating.ipynb:
- Initial exploration of predicting meal rating based on ingredients ang general meal ratig breakdown.
- Avg Meal Rating: 3.73
- Meal Rating broken down by category (not significant differeces):
	- Chefchoice: 3.73
	- Livinglight: 3.67
	- Powerpick: 3.79
	- Freakyfit: 3.72

##### feature_analysis.ipynb:
- Notebook for viewing and exploring feature importances (permutation importances) and partial depedencies.
- Imports all function from model/feature_importance.py which contains functionality to create plots.

##### meal_rec.ipynb
- Exploring meal recommendation system using collaborative filtering.
- Model uses ALS with missing values entered with meal avg to create predicted satisfaction.
- Want to explore annd understand hidden topics of ALS.
- Need to do a test train split to gauge how it is performing.

### images:
- Folder for holding used images


### model:
##### data-prep.py:
- Rudimentary attempt to create ingredient frequency dataframe.
- File groups base tables customer_id and meal_id and then uses loops to go through every ingredient in every meal for each customer.
- Due to looping process ingredients with the same spelling and different capitalization are grouped together which is good.
- Runs very slowly (only using for a subset of data right now)
- Saves the dataframe as a pickle file

##### tree_pred_cleaning.py:
- File reads in meal andn avg rating dataframe.
- Converts meal ID's to meal names
- combines small number of ingredients that are similar:
	1. If spelled the same with different capitalization combines them
	2. Uses stemming to combine same root
- Outputs:
	1. pickled feature matrix X (in models folder)
	2. pickled target values y (in models folder)

##### tree_rating.py:
- General file which does a grid search for both a Random Forrest and Gradient Boost Regressor Models. Best models are saved as pickle files.
- Models are comparable but the Random Forest is much faster at fitting.
- Results:
	- Final RF MSE: 0.1581
	- Final GB MSE: 0.1682
- Random forrest model is slightly superior
- MSE of .158 means that on average the predicted rating is +- .397 stars from the true.
- Areas of possible concern:
	- For some runs the Test MSE is equal to or less than the Train MSE
	- Not a lot of data for fitting (only 657 meals with more than 5 ratings)

##### feature_importance.py:
- File contains functions for calculating the permutation importance of a feature in a Random Forrest model and Partial Dependence of a feature given its name.
- Two main function which call other helper functions are:
	- plot_partial_dependence(model, X_train, features, name)
	- plot_perm_import(f_imps, names, n)
- Needs to have:
	- Fitted model
	- Split data
	- list of feature names

##### rec.py:
- nmf factorization model.

##### rec_pickle_data.py:
- two sql querries that return the information needed for the recommendation:
	- One gets all user ratings.
	- Another gets the avg rating for a particular meal.
	- Should look into using the avg user rating not the avg meal rating.

### pickle:
* feature_cols: list of ingredient names as they appear in the feature matrix X_features
* gb_model: sklearn gradient boosted regressor model (unfit)
* rf_model: sklearn random forest regressor model (unfit)
* user_f_df: pandas dataframe with each row as customer and cols as ingredients. Values in each cell are frequency that ingredient is in users dishes
* X_features: np 2d array (meals = rows, cols = ingredients)
* y_target: np 1d array of avg meal ratings. Used with X_features
* avg_meal_ratingDF: pandas df with meals and their avg rating
* cust_ratingsDF: pandas df with customer ratings of meals





