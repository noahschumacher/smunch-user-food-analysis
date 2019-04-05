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

import multiprocessing

from order_prediction.user_class import User

## local run sql file
from db.python_db import connect, run_sql_query


def create_obj(u):
	user_id, account_id, count = u
	if count > 100:
		print(u)
		user = User(user_id, account_id, conn)
		user.build_table()
		return True, user
		print('Added in obj')

	else:
		return False, None


def run_users_p(users):
	pool  = multiprocessing.Pool(4)

	results = pool.map(create_obj, users)
	user_objects = []

	print("Here?")
	for i, value in enumerate(results, start=users[0]):

		if value[0]:
			print("Added")
			user_objects.append(value[1])

	return user_objects



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
	'''

	sliced_users = user_acc_table.loc[user_acc_table.order_count > sl, :]

	user_objects = {}

	for i, user in enumerate(sliced_users.values):

		print(user, "Building class...")
		user_id, account_id, count = user

		user = User(user_id, account_id)	## Create the object
		user.build_table(conn, drop_tests=True)  ## Create user dictionary (targets and features)
		user.build_model_test()			## Build RF and GB model for testing
		#user.build_model_deploy()		## Build Deployable RF (no train/test)

		user_objects[user_id] = user
		print("Added", i+1)

	return user_objects


if __name__ == '__main__':
	
	conn = connect()
	user_acc_table = pickle.load(open('order_prediction/user_account_order.p', 'rb'))

	objs = sequential(user_acc_table, conn, 220)
	pickle.dump(objs, open('order_prediction/user_objects_test_dict.p', 'wb'))

	#run_users_p(sliced_users.values)






