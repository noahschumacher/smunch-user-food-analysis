## Server Flask File

from flask import Flask, render_template, request, jsonify, Response

import pickle
import numpy as np
import pandas as pd
import os

from order_prediction.meal_pred_deploy import *


## Create the app object that will route our calls
app = Flask(__name__)


## Rendering the home page HTML
@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')



## File uploader
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		target = 'temp_files'

		file = request.files['file']
		filename = file.filename
		destination = '/'.join([target, 'meal_pred.csv'])
		file.save(destination)

		meals = pd.read_csv(destination)
		meals.drop(['Unnamed: 0', 'Meals'], axis=1, inplace=True)
		meals_d = meals.to_dict(orient='list')
		preds = list(get_customer_percents(meals_d, ing_ids, user_objs))


		labels = ['Meal 1', 'Meal 2', 'Meal 3', 'Meal 4']
		colors = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"]


		return render_template('prediction.html', predictions=preds, set=zip(preds, labels, colors))



if __name__ == '__main__':

	#######################################################
	######## LOADING IN USER & INGREDIENT DATA ############
	print("Loading in user and ingredient data...")
	ing_df = pd.read_csv('data/ingrds.csv')
	ing_dict = dict(zip(ing_df.ingredient_id, ing_df.name))
	ing_ids = list(ing_dict.keys())
	ing_names = list(ing_dict.values())

	## Getting the user objects
	user_objs = pickle.load(open('order_prediction/pickles/user_objects_deployable_dict.p', 'rb'))



	print("Starting server...")
	app.run(host='0.0.0.0', port=3333, debug=True, use_reloader=False)
	print("\nApp closed.")

