## Neural Network Meal Rating Prediction

'''
File:
	- Uses a Neural Network model to predict avg meal rating
	- Hope was that NN hidden layers would uncover meaingful combination
	of ingredients.
	- Model performs worse than RF, GB

Uses:
	- X_features.p: Feature matrix of ingredients (row=meal, cols=ingrds)
	- y_targets.p: Target values, avg rating of the meal.
'''

import numpy as np
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split

import warnings
warnings.simplefilter('ignore')

import tensorflow as tf
from tensorflow import keras


## Get meal rating classification (0,1,2,3,4) based o ingredients:
def rating_class(X_tr, X_te, y_tr, y_te):
	## Creating a sequential neural network model
	model = keras.Sequential()

	## Creating first layer
		# units: nunmber of nodes in layer
		# input_dims: number of features in data (only specified first)
		# activation: activation function to use in layer
	model.add(keras.layers.Dense(units=30, input_dim=858, activation='sigmoid'))
	model.add(keras.layers.Dropout(0.5))		## Dropout layer causes nodes to fail randomly (50%)

	model.add(keras.layers.Dense(20, activation='relu'))	## Adding another layer
	model.add(keras.layers.Dropout(0.5))
	model.add(keras.layers.Dense(10, activation='relu'))

	model.add(keras.layers.Dense(5, activation='sigmoid'))	## Final layer with prediction

	## Compiling model 
		# loss: loss function to use when fitting model.
		# optimizer: algorithm to use to find optimum 
			# values (ie Stochastic GD, etc).
		# metrics: metric to be used in scoring the model.
	model.compile(loss='sparse_categorical_crossentropy',
	              optimizer='adam',
	              metrics=['acc'])

	## Fitting data:
		## epocks: Number of times to go through data set and train values.
		## batch_size: number of data points to feed into model 
			# before parameter update.
	model.fit(X_tr, y_tr, epochs=10, batch_size=30)
	score = model.evaluate(X_te, y_te, batch_size=30)
	print("Accuracy", score[1])

	return model.predict_classes(X_te)


def rating_regress(X_tr, X_te, y_tr, y_te):
	## Creating a sequential neural network model
	model = keras.Sequential()

	model.add(keras.layers.Dense(units=30, input_dim=89, activation='sigmoid'))
	model.add(keras.layers.Dropout(0.5))		## Dropout layer causes nodes to fail randomly (50%)

	model.add(keras.layers.Dense(50, activation='tanh'))	## Adding another layer
	model.add(keras.layers.Dropout(0.2))

	model.add(keras.layers.Dense(20, activation='sigmoid'))
	model.add(keras.layers.Dropout(0.5))

	model.add(keras.layers.Dense(1, activation='relu'))	## Final layer with prediction


	model.compile(loss='mean_squared_error', optimizer='sgd')

	model.fit(X_tr, y_tr, epochs=50, batch_size=3)
	score = model.evaluate(X_te, y_te, batch_size=3)
	print("Mean Error", score**.5)



if __name__ == '__main__':

	X = pickle.load(open('rating_prediction/X_features.p', 'rb'))
	y = pickle.load(open('rating_prediction/y_target.p', 'rb'))
	
	X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.25, random_state=32)

	## Adjusting y to get rating from 0-4
	y_tr_c = np.round(y_tr) - 1
	y_te_c = np.round(y_te) - 1

	#preds_class = rating_class(X_tr, X_te, y_tr_c, y_te_c )
	preds_rating = rating_regress(X_tr, X_te, y_tr, y_te)





