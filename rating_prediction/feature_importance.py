## Noah Schumacher

'''
File:
	- Used for plotting permutation importances
	and partial depedence plots.
	- Does not use sklearns functionality
	of feature importance.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from sklearn.ensemble.partial_dependence import plot_partial_dependence
from sklearn.ensemble.partial_dependence import partial_dependence


def permutation_importance(model, X_test, y_test, scorer=mean_squared_error):
	''' Calculates permutation feature importance for a fitted model
	
	Parameters
	----------
	model: anything with a predict() method
	X_test, y_test: numpy arrays of data
		unseen by model
	scorer: function. Should be a "higher is better" scoring function,
		meaning that if you want to use an error metric, you should
		multiply it by -1 first.
		ex: >> neg_mse = lambda y1, y2: -mean_squared_error(y1, y2)
			>> permutation_importance(mod, X, y, scorer=neg_mse)
	
	Returns
	-------
	feat_importances: numpy array of permutation importance
		for each feature
	
	'''
	
	feat_importances = np.zeros(X_test.shape[1])
	test_score = scorer(model.predict(X_test), y_test)
	for i in range(X_test.shape[1]):
		X_test_shuffled = shuffle_column(X_test, i)
		test_score_permuted = -scorer(y_test, model.predict(X_test_shuffled))
		feat_importances[i] = test_score - test_score_permuted
	return feat_importances


def shuffle_column(X, feature_index):
	''' 
	Parameters
	----------
	X: numpy array
	feature_index: int
	
	Returns
	-------
	X_new: numpy array
	
	Returns a new array identical to X but
	with all the values in column feature_index
	shuffled
	'''   
	
	X_new = X.copy()
	np.random.shuffle(X_new[:,feature_index])
	return X_new


def partial_dependence(model, X, feature_index, classification=True):
	'''
	Parameters
	----------
	model: fitted model
		anything with .predict()
	X: numpy array
		data the model was trained on.
	feature_index: int
		feature to calculate partial dependence for
	classification: boolean. 
		True if the model is a classifier
		   (in which case, it must have .predict_proba()
		False if the model is a regressor
		
	Returns
	-------
	x_values: numpy array
		x values to plot partial dependence over
	pdp: numpy array
		partial dependence values
		
	example:
	>> x, pdp = partial_dependence(model, X_train, 3, classification=False)
	>> plt.plot(x, pdp)
	'''
	
	x_values = np.unique(X[:,feature_index])
	pdp = np.zeros(x_values.shape)
	for i, value in enumerate(x_values):
		X_new = replace_column(X, feature_index, value)
		if classification:
			y_pred_prob = model.predict_proba(X_new)[:,1]
			y_pred_prob = np.clip(y_pred_prob, 0.001, 0.999)
			y_pred = np.log(y_pred_prob / (1 - y_pred_prob))
		else:
			y_pred = model.predict(X_new)
		pdp[i] = y_pred.mean()
	return (x_values, pdp)


def replace_column(X, feature_index, value):
	'''
	Parameters
	----------
	X: numpy array
	feature_index: int
	value: float
	
	Returns
	-------
	X_new: numpy array
	
	Returns a new array identical to X but
	with all the values in column feature_index
	replaced with value
	'''  
	X_new = X.copy()
	X_new[:,feature_index] = value
	return X_new


## Plot of feature importances
def plot_perm_import(f_imps, names, n):
	'''
	Parameters
	----------
	f_imps: numpy array
	names: list
	n: int
	
	Returns
	-------
	None
	
	Plots the permutation importances for n top features.
	''' 
	sorts = np.argsort(f_imps)
	
	last_x = f_imps[sorts[-n:]]
	last_x_names = names[sorts[-n:]]

	idx = np.arange(len(names))

	plt.barh(idx[-n:], last_x, align='center')
	plt.yticks(idx[-n:], last_x_names)

	plt.title("Permutation Importances in Random Forrest")
	plt.xlabel('Relative Importance of Feature')
	plt.ylabel('Feature Name')
	plt.show()


## Partial dependence indnicates which food help/hurt rating
def plot_partial_dependence(model, X_train, features, name):
	'''
	Parameters
	----------
	model: model with .predict
	X_train: numpy 2d array
	features: list
	names: string
	
	Returns
	-------
	None
	
	Plots the partial depedence for feature name for a RF Regressor
	''' 
	feat_ind = features.index(name)
	xx, pdp = partial_dependence(model, X_train, feat_ind, False)
	plt.plot(xx, pdp)
	plt.title(name)
	plt.show()
	



