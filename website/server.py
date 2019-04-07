## Server Flask File

from flask import Flask, render_template, request, jsonify, Response

import pickle
import numpy as np
import pandas as pd
import os


## Create the app object that will route our calls
app = Flask(__name__)


## Rendering the home page HTML
@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')


## File uploader
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		target = os.path.join(APP_ROOT, 'temp_files/')

		file = request.files['file']
		filename = file.filename
		destination = '/'.join([target, filename])
		file.save(destination)

		return "File Saved to Temp"




# #########################################################
# ########## PROBABILITY OF ORDER ########################

# @app.route('/probability', methods=['GET'])
# def probability():
# 	return render_template('probability.html')


# ## Getting predicted probability of order based on ingredients.
# @app.route('/addMealCol', methods=['POST'])
# def predictProba():
# 	req = request.get_json()
# 	print(req)

# 	## Getting params from request
# 	u_id, a_id = req['user_id'], req['account_id']
# 	print(u_id)

# 	## Returning json formatted output (.js file grabs 'prediction')
# 	return jsonify({'user_id':u_id, 'account_id':a_id})



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3333, debug=True)

