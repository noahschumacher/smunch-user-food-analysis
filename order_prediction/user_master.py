'''
File:
	- Pulls in user information from pickled df.
	- Goes through and sequentially creates user objects.
	- Stores user objects in dictionary with key as user_id.
	- Pickles this dictionary.

Note:
	- Attempts to do this in || but sql querry limitations.
'''

import numpy as np
import pandas as pd
import pickle


## local files annd user class
from order_prediction.user_class import User
from db.python_db import connect, run_sql_query



def sequential(user_acc_table, conn, sl=200):
	'''
	Function: Sequentially goes through users and creates their objects
	Params:
	------
	- user_acc_table: pandas df, with cols user_id, account_id, tot_meal_count
	- conn: Smunch DB connection

	Returns:
	-------
	- user_objects: dictionary with key as user_id and User object as value
	- test: string idicating is test or deploy
	'''

	test = input("Test Model of Deploy (test/deploy): ")
	sliced_users = user_acc_table.loc[user_acc_table.order_count > sl, :]

	user_objects = {}
	for i, user in enumerate(sliced_users.values):

		print(user, "Building class...")
		user_id, account_id, count = user

		user = User(user_id, account_id)	## Create the object
		user.build_table(conn, drop_tests=False)  ## Create user dictionary (targets and features)

		if test == 'test':
			user.build_model_test()			## Build RF and GB model for testing
		else:
			user.build_model_deploy()		## Build Deployable RF (no train/test)

		user_objects[user_id] = user
		print("Added", i+1)

	return user_objects, test


if __name__ == '__main__':
	
	conn = connect()
	user_acc_table = pickle.load(open('order_prediction/pickles/user_account_order.p', 'rb'))

	thresh = int(input("Set order threshold: "))
	objs, test = sequential(user_acc_table, conn, thresh)

	file = 'order_prediction/pickles/user_objects_'+test+'_dict.p'
	pickle.dump(objs, open(file, 'wb'))








