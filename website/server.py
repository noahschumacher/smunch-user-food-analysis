## Server Flask File

from flask import Flask, render_template, request, jsonify, Response
import pickle
import numpy as np
import pandas as pd


## Create the app object that will route our calls
app = Flask(__name__)


## Rendering the home page HTML
@app.route('/', methods = ['GET'])
def home():
	return render_template('home.html')


#########################################################
########## CLUSTERING ########################
@app.route('/clustering', methods = ['GET'])
def clustering():
	return render_template('clustering.html')


## Rending the user cluster table
@app.route('/renderClusters', methods = ['POST'])
def renderClusters():
	req = request.get_json()
	print(req)

	## Getting params from request
	n = req['n_clusters']

	## Returning json formatted output (.js file grabs 'prediction')
	return jsonify({'n':n})


#########################################################
########## PROBABILITY OF ORDER ########################
@app.route('/probability', methods = ['GET'])
def probability():
	return render_template('probability.html')


## Getting predicted probability of order based on ingredients.
@app.route('/predictProba', methods = ['POST'])
def predictProba():
	req = request.get_json()
	print(req)

	## Getting params from request
	u_id, a_id = req['user_id'], req['account_id']
	print(u_id)

	## Returning json formatted output (.js file grabs 'prediction')
	return jsonify({'user_id':u_id, 'account_id':a_id})



#########################################################
########## AVG RATING PREDICTION ########################
@app.route('/rating-prediction', methods = ['GET'])
def rating_prediction():
	return render_template('rating-prediction.html')



#########################################################
############### RECOMMENDER ########################
@app.route('/recommender', methods = ['GET'])
def recommender():
	return render_template('recommender.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3333, debug=True)

