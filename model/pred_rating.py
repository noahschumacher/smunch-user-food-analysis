## Initialization and imports
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt

## sklearn models and validation
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

## pickle to read in feature matrix and target values
import pickle


## Gets cross validated accuracy and AUC for different models
def cross_val(X_train, y_train, func):

	mse = -sum(cross_val_score(func, X_train, y_train, cv=4, scoring='neg_mean_squared_error'))/4

	func_name = str(func.__class__.__name__)

	print("{0:27} Train CV | Mean Square Error: {1:5.4}".format(func_name, mse))
	return mse


## Grid Search for the Random Forrest
def rf_grid(X_train, y_train, X_test, y_test):
	random_forest_grid = {'max_depth': [100, 500, 750],
					  'max_features': ['sqrt', 'log2'],
					  'min_samples_split': [2, 4],
					  'min_samples_leaf': [1, 2, 4],
					  'bootstrap': [True, False],
					  'n_estimators': [5, 20, 50, 100],
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
	pickle.dump(best_rf_model, open('model/rf_model.p', 'wb'))

	return best_rf_model


## Performing grid search on gradient boost to find best params
def gb_grid(X_train, y_train, X_test, y_test):
	gb_grid = {'max_depth': [3, 5],
			  'learning_rate': [.05, .01],
              'min_samples_split': [2],
              'max_depth': [3, 5],
              'min_samples_leaf': [1, 2, 4],
              'n_estimators': [100, 400],
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
	pickle.dump(best_gb_model, open('model/gb_model.p', 'wb'))

	return best_gb_model



if __name__ == '__main__':
	
	X = pickle.load(open('model/X_features.p', 'rb'))
	y = pickle.load(open('model/y_target.p', 'rb'))

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)


	#########################################################
	##### RANDOM FORREST and GRADIENT BOOSTED REGRESSOR #####
	
	## Getting models from the gridsearch
	rf_model = rf_grid(X_train, y_train, X_test, y_test)
	# gb_model = gb_grid(X_train, y_train, X_test, y_test)

	## cross val score of best model
	rf_mse = cross_val(X_train, y_train, rf_model)
	# gb_mse = cross_val(X_train, y_train, gb_model)

	rf_model.fit(X_train, y_train)
	# gb_model.fit(X_train, y_train)
	
	## Preds on test data for both gridsearched vals
	rf_preds = rf_model.predict(X_test)
	# gb_preds = gb_model.predict(X_test)


	## Print the error of the test
	rf_error = np.round(np.sum((rf_preds - y_test)**2) / len(y_test), 4)
	# gb_error = np.round(np.sum((gb_preds - y_test)**2) / len(y_test), 4)

	print("\nFinal RF MSE:", rf_error)
	# print("Final GB MSE:", gb_error)


