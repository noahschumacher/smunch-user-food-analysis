'''
File:
	- Used for testing and building tree models to predict
	the probability a particular user will order a meal
	given the meal was offered. 

'''



## Initialization and imports
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt

## sklearn models and validation
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

## Changing directory to top folder (All programs run from top)
import os
os.chdir('/Users/nschumacher/docs/galvanize/smunch-user-food-analysis')

## local run sql file
from db.python_db import connect, run_sql_query
from run2.models.user_class import User

conn = connect()


## Function gives list of ingredients user as has seen (remove never seen ingrds)
def seen_ingredients(user):
    rows, cols = user.X.shape
    keeps = []
    for i in range(cols):
        if (user.X[:,i] == 1).sum() != 0:
            keeps.append(i)
            
    return keeps

## Gets cross validated accuracy and AUC for different models
def cross_val(X_train, y_train, func):

    mse = -sum(cross_val_score(func, X_train, y_train, cv=4, scoring='neg_mean_squared_error'))/4
    func_name = str(func.__class__.__name__)
    print("{0:27} Train CV | Mean Square Error: {1:5.4}".format(func_name, mse))
    return mse


## Grid Search for the Random Forrest
def rf_grid(X_train, y_train, X_test, y_test):
	random_forest_grid = {'max_depth': [10, 40, 100, 150],
					  'max_features': ['sqrt', 'log2'],
					  'min_samples_split': [2, 4],
					  'min_samples_leaf': [1, 2],
					  'bootstrap': [True, False],
					  'n_estimators': [20, 100, 200],
					  'random_state': [1]}

	rf_gridsearch = GridSearchCV(RandomForestRegressor(),
								 random_forest_grid,
								 n_jobs=-1,
								 verbose=True,
								 cv=4,
								 scoring='neg_mean_squared_error')
	rf_gridsearch.fit(X_train, y_train)

	print( "\nbest parameters:\n", rf_gridsearch.best_params_ )
	best_rf_model = rf_gridsearch.best_estimator_

	## Dumping the best model to a pickle file
	#pickle.dump(best_rf_model, open('run1/pickle/rf_model.p', 'wb'))

	return best_rf_model

## Performing grid search on gradient boost to find best params
def gb_grid(X_train, y_train, X_test, y_test):
	gb_grid = {'max_depth': [3, 5, 10],
			  'learning_rate': [.05, .01],
              'min_samples_split': [2, 3],
              'max_depth': [3, 5],
              'min_samples_leaf': [1, 2, 4],
              'n_estimators': [20, 50, 100],
              'random_state': [1]}

	gb_gridsearch = GridSearchCV(GradientBoostingRegressor(),
	                             gb_grid,
	                             n_jobs=-1,
	                             verbose=True,
	                             cv=4,
	                             scoring='neg_mean_squared_error')
	gb_gridsearch.fit(X_train, y_train)

	print( "\nbest parameters:\n", gb_gridsearch.best_params_ )
	best_gb_model = gb_gridsearch.best_estimator_

	## Dumping the best model to a pickle file
	#pickle.dump(best_gb_model, open('run1/pickle/gb_model.p', 'wb'))

	return best_gb_model


if __name__ == '__main__':
	user_id = '0030N00002LQq8gQAD'
	account_id = '0010N00004IaEsqQAF'
	u = User(user_id, account_id, conn)
	u.build_table()


	keeps = seen_ingredients(u)
	X = u.X[:,keeps]
	y = u.y

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15)

	#rf_model = rf_grid(X_train, y_train, X_test, y_test)
	rf_model = RandomForestRegressor(bootstrap = False,
									 max_depth = 10,
									 max_features = 'sqrt',
									 min_samples_leaf = 2,
									 min_samples_split = 2,
									 n_estimators = 150,
									 random_state = 1)


	#gb_model = gb_grid(X_train, y_train, X_test, y_test)
	gb_model = GradientBoostingRegressor(max_depth = 3,
										 min_samples_leaf = 2,
										 learning_rate = .01,
										 min_samples_split = 2,
										 n_estimators = 40)

	#print("Cross Val ME RF:", cross_val(X_train, y_train, rf_model)**.5)
	#print("Cross Val ME GB:", cross_val(X_train, y_train, gb_model)**.5)

	rf_model.fit(X_train, y_train)
	gb_model.fit(X_train, y_train)

	rf_preds = rf_model.predict(X_test)
	gb_preds = gb_model.predict(X_test)

	rf_me_test = np.mean( (rf_preds-y_test)**2 )**.5
	gb_me_test = np.mean( (gb_preds-y_test)**2 )**.5
	avg_me_test = np.mean( (np.mean(y_train)-y_test)**2 )**.5

	print("RF Model Test Error: {0:3.4f}  |  GB Model Test Error: {1:3.4f}".format(rf_me_test, gb_me_test)  )
	print("Avg Test Error:", avg_me_test)

	print("Model {0:2.3}% better than guessing avg.".format(100-(rf_me_test/avg_me_test)*100))


